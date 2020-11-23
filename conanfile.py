from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os
import re


class ZmqTestConan(ConanFile):
    name = "zmqtest"
    description = "Test application for testing zmq"
    topics = ("zmq")
    url = "https://github.com/kasunch/workflow-test"
    homepage = "https://github.com/bincrafters/conan-zmq"
    license = "	Apache-2.0"  # SPDX Identifiers https://spdx.org/licenses/
    exports_sources = ["CMakeLists.txt", "src/*"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"zmqshared": [True, False]}
    default_options = {"zmqshared": False}

    _git_is_dirty = False
    _git_commit = "unknown"
    _cmake = None

    def set_version(self):
        git = tools.Git(folder=self.recipe_folder)
        if not self.version:
            output = git.run("describe --all").splitlines()[0].strip()
            self.version = re.sub("^.*/v?|^v?", "", output)
        output = git.run("diff --stat").splitlines()
        self._git_is_dirty = True if output else False
        self._git_commit = git.run("rev-parse HEAD").splitlines()[0].strip()

        self.output.info("Version: %s, Commit: %s, Is_dirty: %s" %
                         (self.version, self._git_commit, self._git_is_dirty))

    def requirements(self):
        self.requires("zmq/4.3.2@bincrafters/stable")
        if self.options.zmqshared:
            self.options["zmq"].shared = True
        else:
            self.options["zmq"].shared = False

    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.definitions["ZMQ_SHARED"] = "ON" if self.options.zmqshared else "OFF"
            self._cmake.definitions["USE_CONAN_BUILD_INFO"] = "ON"
            del self._cmake.definitions["CMAKE_EXPORT_NO_PACKAGE_REGISTRY"]
            self._cmake.configure()
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
