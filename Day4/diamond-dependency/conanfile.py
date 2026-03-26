from conan import ConanFile
from conan.tools.cmake import cmake_layout

class MyMainApp(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        # We explicitly force the version here
        self.requires("logger/2.0", force=True)
        self.requires("liba/1.0")
        self.requires("libb/1.0")

    def layout(self):
        cmake_layout(self)
