from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.env import Environment

class MyQtAppRecipe(ConanFile):
    name = "my_qt_app"
    version = "1.0"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps", "CMakeToolchain"

    def requirements(self):
        self.requires("qt/6.7.0")

    def configure(self):
        self.options["qt"].shared = True

        self.options["qt"].with_fontconfig = True

        self.options["qt"].with_xcb = True
        self.options["qt"].with_x11 = True

        self.options["qt"].qtwayland = True
        self.options["qt"].with_vulkan = False 
        self.options["qt"].with_fontconfig = True

        self.options["qt"].qttools = True

    def generate(self):
        env = Environment()

        qt_package_folder = self.dependencies["qt"].package_folder

        #qt_plugins = f"{qt_package_folder}/plugins"
        qt_plugins = "/home/jegan/.conan2/p/b/qt63879f3d94806/b/build/Release/qtbase/plugins"
        print(qt_plugins)
        env.define("QT_PLUGIN_PATH", qt_plugins)

        env.define("FONTCONFIG_FILE", "/etc/fonts/fonts.conf")
        env.define("QT_QPA_PLATFORM", "xcb")

        env.vars(self, scope="run").save_script("qt_environment_setup")

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

        
