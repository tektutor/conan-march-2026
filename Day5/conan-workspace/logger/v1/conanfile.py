from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout

class LoggerRecipe(ConanFile):
    name = "logger"
    version = "1.0" 
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeToolchain"
    exports_sources = "CMakeLists.txt", "src/*", "inc/*"

    def layout(self):
        cmake_layout(self)
        self.cpp.source.includedirs = ["inc"]

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        self.cpp.source.includedirs = ["inc"]

    def package(self):
        cmake = CMake(self)
        cmake.install()
        self.cpp.source.includedirs = ["inc"]

    def package_info(self):
        self.cpp_info.libs = ["logger"]
        self.cpp.source.includedirs = ["inc"]
