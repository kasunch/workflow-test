from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os, re, configparser

class ZmqTestConan(ConanFile):
    description = "Test application for testing zmq"
    topics = ("zmq")
    url = "https://github.com/kasunch/workflow-test"
    homepage = "https://github.com/bincrafters/conan-zmq"
    license = "	Apache-2.0"  # SPDX Identifiers https://spdx.org/licenses/
    exports = ["project.conf"]
    exports_sources = ["CMakeLists.txt", "src/*"]
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"
    options = {"zmqshared": [True, False]}
    default_options = {"zmqshared": False}

    def set_name(self):
        parser = self._get_config()
        self.name = parser["conanfile"]["name"]

    def set_version(self):
        if not self.version:
            git = tools.Git(folder=self.recipe_folder)
            version = re.sub(".*/", "", str(git.get_branch()))
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

    def _get_config(self):
        parser = configparser.ConfigParser()
        parser.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "project.conf"))
        return parser