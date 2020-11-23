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

    def set_version(self):
        version, _, _ = self._get_version_info()
        self.version = version

    def requirements(self):
        self.requires("zmq/4.3.2@bincrafters/stable")
        if self.options.zmqshared:
            self.options["zmq"].shared = True
        else:
            self.options["zmq"].shared = False

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ZMQ_SHARED"] = "ON" if self.options.zmqshared else "OFF"
        cmake.definitions["USE_CONAN_BUILD_INFO"] = "ON"
        del cmake.definitions["CMAKE_EXPORT_NO_PACKAGE_REGISTRY"]
        cmake.configure()

        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def _get_version_info(self):
        git = tools.Git(folder=self.recipe_folder)

        output = git.run("describe --all")
        print(output)

        if not self.version:
            version = git.get_tag() or git.get_branch() or "unknown"
            version = re.sub("^.*/v?|^v?", "", version)
        else:
            version = self.version
        commit = git.get_commit() or "unknown"
        is_dirty = not git.is_pristine()

        print(is_dirty)

        return version, commit, is_dirty
