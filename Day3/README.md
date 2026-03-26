# Day 3

## Today's Agenda
<pre>
- Understanding Python Recipe
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
  - fPIC (Position Independent Code) is necessary for static libraries that 
	might be linked into sharedVirtualBuildEnv

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

## Info - Conan Virtual Environment
<pre>
- In the C++ world, a Conan Virtual Environment is a mechanism used to manage the tools and environment variables 
  required to build and run your projects without cluttering your system globally

- Think of it as the C++ equivalent of Python’s venv
	
- It ensures that when you need a specific version of CMake, a compiler, or a shared library, 
  they are "in your path" only when you are working on that specific project

- There are 2 types of Virtual Environment
  1. Build environment (VirtualBuildEnv) and
  2. Run environment (VirtualRunEnv)
</pre>

## Info - VirtualBuildEnv - Build environment
<pre>
- This manages the tools you required to build your application
	
- What it includes ?
  - Paths to compilers (GCC, Clang), build tools (CMake, Ninja, Meson), 
	and code generators (Protobuf, Flex/Bison)

  - Conan generates a file named conanbuild.sh for Linux/macOS or conanbuild.bat/ps1 for Windows
	
  - this file can be located under build/{Debug,Release}/generators/conanbuild.sh

- Why use it ?
  - So you can use cmake or ninja directly in your terminal, knowing it's the exact version specified in your conanfile
</pre>

## Info - VirtualRunEnv - Run environment
<pre>
- This manages the tools you need to run your application binary after it’s built
	
- What it includes?
  - Paths to shared libraries (.so, .dll, .dylib) and runtime executables
	
  - It sets variables like PATH, LD_LIBRARY_PATH, and DYLD_LIBRARY_PATH
	
  - Conan generates a file named conanrun.sh for Linux/MacOS or conanrun.bat/ps1 for Windows

  - this file can be located under build/{Debug,Release}/generators/conanrun.sh

- Why use it
  - To prevent "Library not found" errors when you try to launch your compiled application	
</pre>
