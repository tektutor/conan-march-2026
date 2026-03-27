from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout

class LibARecipe(ConanFile):
    name = "liba"
    version = "1.0" 
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"
    exports_sources = "CMakeLists.txt", "src/*", "inc/*"

    def layout(self):
        cmake_layout(self)
        self.cpp.source.includedirs = ["inc"]

    def requirements(self):
        self.requires("logger/1.0")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["liba"]
        self.cpp.source.includedirs = ["inc"]
