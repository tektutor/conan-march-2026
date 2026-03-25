# Day 3

## Today's Agenda
<pre>
- Understanding Conan Virtual Environments
- Conan Transitive Dependency
- Conan Profiles
  - Overview
  - Debug Profile
  - Release Profile
  
- Hands-on Exercises
  - Managing C++ application dependency with a Python recipe with Conan & CMake
  - Using Conan Virtual Environments
  - Managing Transitive dependency with Conan & CMake
  - Using Conan Default Profile
  - Using Conan Debug Profile
  - Using Conan Release Profile

- Undestanding Conan Cache
- Recommended Folder Layouts
- Using conan 
  - install
  - build
  - create
  - export and
  - upload
  
- Hands-on Lab exercises
  - Fetch a pre-compiled package from ConanCenter and generate build files for it
    - Understand conan install
  - Creating a simple custom package template using Conan
    - Understand conan 
  - Take a local Python recipe and save it into the Local Cache without actually building the C++ code
    - Understand conan exports practically
  - Build the package from scratch inside the Local Cache so other projects on your machine can use it
    - Understand conan create
  - Distributing package to JFrog Artifactory 
    - Understand conan upload
</pre>

## Info - Understanding Python recipe file
<pre>
from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import copy

class MyLibraryRecipe(ConanFile):
    name = "mylibrary"
    version = "1.0"
    license = "MIT"
    description = "A simple C++ library"
    
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Where the source code is located relative to conanfile.py
    exports_sources = "CMakeLists.txt", "src/*", "include/*"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        self.requires("fmt/10.1.1")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["mylibrary"]  
</pre>

Let's understand the conanfile.py recipe 
<pre>
- The recipe is divided into two main parts
  1. Attributes - metadata and configurations 
  2. Methods - the steps of the build/packaging lifecycle

- name & version 
  - the identity of your package (e.g., fmt/10.1.1)
- license, author, url, description 
  - Standard information to help others understand and use your package

- settings 
  - Defines the system configuration that affects the compiled binary
  - Typically, settings = "os", "compiler", "build_type", "arch"
  - Conan uses these to generate a unique ID for the compiled binary
  - A build for Windows/MSVC/Debug will have a different ID than Linux/GCC/Release
  - Conan uses these to generate a unique ID for the compiled binary
  - A build for Windows/MSVC/Debug will have a different ID than Linux/GCC/Release

- options & default_options
  - Defines how the package can be customized.
    - Example
	  options = {"shared": [True, False], "fPIC": [True, False]}
      default_options = {"shared": False, "fPIC": True}
  - fPIC (Position Independent Code) is necessary for static libraries that might be linked into 
	sharedVirtualBuildEnv (The Build Context)

    Purpose: Provides tools needed to compile your code.

    Trigger: Generated when you have tool_requires (e.g., cmake/3.25.0, ninja/1.11.0).

    Files Generated: conanbuildenv-release-x86_64.sh and a wrapper conanbuild.sh.

    Usage: Sourcing this makes tools like cmake available in your path even if they aren't installed on your system.

VirtualRunEnv (The Host/Run Context)

    Purpose: Provides what is needed to execute your compiled program.

    Trigger: Automatically generated for regular requires.

    Files Generated: conanrunenv-release-x86_64.sh and a wrapper conanrun.sh.

    Logic: It automatically adds the bin folders of your dependencies to PATH and lib folders to LD_LIBRARY_PATH. libraries later, mostly relevant on Linux/macOS

- Lifecycle Methods
  - Conan executes specific methods in a strict order to build and package your library
  - You only implement the ones you need.

  - config_options(self) and configure(self)
	- Used to configure the settings and options dynamically.
    - For example, Windows does not use fPIC. 
	  - You would remove it here so it doesn't cause a conflict
	
	def config_options(self):
        if self.settings.os == "Windows":
           del self.options.fPIC

  - requirements(self)
	- This is the programmatic equivalent of the [requires] section in conanfile.txt
	- You declare your dependencies here

	def requirements(self):
        self.requires("fmt/10.1.1")
        self.requires("zlib/1.3")

  - layout(self)
	- Defines where the source files are and where the build artifacts should go
	- If you are using CMake, Conan provides a built-in layout that matches standard CMake practices

	def layout(self):
        cmake_layout(self)
	
  - generate(self)
	- Prepares the build environment
	- This step runs before the actual build
	- It creates the toolchain files (CMakeToolchain) and the dependency config files (CMakeDeps) 
	  so your build system knows how to find everything

	def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

 - build(self)
   - This is where the actual compilation happens
   - You tell Conan how to invoke your build system
   - For a CMake project, you initialize a CMake helper, configure the project, and run the build command

   def build(self):
       cmake = CMake(self)
       cmake.configure()
       cmake.build()

  - package(self)
	- Once the build is done, Conan needs to isolate the final artifacts (header files, .lib, .dll, .so, .a) 
	  from the messy build folder and put them into a clean "package" folder
	- With CMake, this usually just triggers the install target

	def package(self):
        cmake = CMake(self)
        cmake.install()

  - package_info(self)
	- This is the most crucial step for the consumer of your package
	- It tells Conan how other projects should link against your newly created library
	- You define the include directories and the names of the compiled libraries
	
	def package_info(self):
        # Tells consumers to link against a library named 'mylibrary'
        self.cpp_info.libs = ["mylibrary"]
</pre>

## Info - Understanding Conan Virtual Environments
<pre>
- In Conan 2.x, "Virtual Environments" are the mechanism used to inject the environment variables 
  like PATH, LD_LIBRARY_PATH, or custom flags required to either build a project or run an executable

- Unlike Python's venv, which creates a physical directory of binaries, Conan's virtual environments 
  are script-based
	
- They generate shell scripts (.sh, .bat, or .ps1) that modify your current terminal session to "see" the 
  dependencies located in the Conan cache
	
- Conan separates the environment into two distinct "contexts" to avoid polluting your runtime with 
  build-only tools like CMake or a cross-compiler

- There are 2 virtual environments in Conan 
  1. Build Context
  2. Host/Run Context

- VirtualBuildEnv (The Build Context)
  - Purpose - Provides tools needed to compile your code
  - Trigger - Generated when you have tool_requires (e.g., cmake/3.25.0, ninja/1.11.0)
  - Files Generated - conanbuildenv-release-x86_64.sh and a wrapper conanbuild.sh
  - Usage - Sourcing this makes tools like cmake available in your path even if they aren't installed on your system

- VirtualRunEnv (The Host/Run Context)
  - Purpose - Provides what is needed to execute your compiled program
  - Trigger - Automatically generated for regular requires
  - Files Generated - conanrunenv-release-x86_64.sh and a wrapper conanrun.sh
  - Logic - It automatically adds the bin folders of your dependencies to PATH and lib folders to LD_LIBRARY_PATH
</pre>
