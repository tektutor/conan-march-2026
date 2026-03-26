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
  - Take a local Python recipe and save it into the Local Cache without actually building the C++ code
    - Understand conan export
  - Build the package from scratch inside the Local Cache so other projects on your machine can use it
    - Understand conan create
  - Distributing package to JFrog Artifactory 
    - Understand conan upload
  - Listing all packages in your local Conan Cache
	- Understand conan list
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

##### Info - VirtualBuildEnv - Build environment
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

##### Info - VirtualRunEnv - Run environment
<pre>
- This manages the tools you need to run your application binary after it’s built
	
- What it includes?
  - Paths to shared libraries (.so, .dll, .dylib) and runtime executables
	
  - It sets variables like PATH, LD_LIBRARY_PATH, and DYLD_LIBRARY_PATH
	
  - Conan generates a file named conanrun.sh for Linux/MacOS or conanrun.bat/ps1 for Windows

  - this file can be located under build/{Debug,Release}/generators/conanrun.sh

- Why use it ?
  - To prevent "Library not found" errors when you try to launch your compiled application	
</pre>

## Lab - Conan Transitive Dependency
Note
<pre>
- In this exercise, the main application and lib application are independent projects
- The lib folder is just present as a sub-folder but otherwise they are totally independent projects
- Hence, the lib project has its own conan recipe file and its own CMakeLists.txt
- On the similar note, the main project has its own conan recipe file and a separate CMakeLists.txt
- The lib project is a static library that depends on fmt third-party library
- The main application depends on the static library(lib project)
</pre>

<pre>
cd ~/conan-march-2026
git pull
cd Day3/transitive-dependency
ls -l

cat lib/CMakeLists.txt
cat lib/conanfile.py
cat lib/inc/hello.h
cat lib/src/hello.cpp
	
</pre>
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/48aeed69-3340-4007-bbde-0fefb18d6494" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/6ee69de3-e5ad-486f-8829-dc8aa5b3aec9" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/147a442c-e14c-4307-b2d1-9287969a337a" />

Let's build the static library project
```
# This command will download fmt library from the ConanCenter Remote Repository, save the fmt source code under user home .conan2 folder
# and build the fmt library into the Conan Local cache
# Conan default profile by default builds the dependent libraries in Release mode, hence it will only generates conan-release preset
conan install . --build=missing

# The below command has a collection of many preset configurations used in release builds
# This is equivalent to cmake -S . -B build/Release -DCMAKE_BUILD_TYPE=Release DCMAKE_TOOLCHAIN_FILE=build/Release/generators/conan_toolchain.cmake
cmake --preset conan-release

# This builds the code as static library using the toolchain generated by conan
cmake --build --preset conan-release

# This copies the static library, its CMakeLists.txt and the exported header files into the Conan Local cache folder ( e.g /home/jegan/.conan2/p/... )
conan create . --build=missing
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/1f088b1c-3b26-44b3-a321-a326df8788fc" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/3bef3195-f6e4-48c7-bfca-64bbb5b4e0c5" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/cd2aa10c-ff2c-44e9-9fe4-01521a479614" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/599614f7-f4c0-47ea-a412-dcddcc39d6b0" />

Let's build the main application now
```
cd ~/conan-march-2026
git pull
cd Day3/transitive-dependency
ls -l

cat CMakeLists.txt
cat conanfile.py
cat cat/main.cpp

# This command will use the hello_lib library from the Local Conan Cache under the user home .conan2 folder
# Conan default profile by default builds the dependent libraries in Release mode, hence it will only generates conan-release preset
conan install . --build=missing

# The below command has a collection of many preset configurations used in release builds
# This is equivalent to cmake -S . -B build/Release -DCMAKE_BUILD_TYPE=Release DCMAKE_TOOLCHAIN_FILE=build/Release/generators/conan_toolchain.cmake
cmake --preset conan-release

# This builds the main application code using the conan-release preset generated by conan
cmake --build --preset conan-release
```

<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/8405e184-18a4-4359-8fb5-c2f7d9a8e637" />

<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/d69b3dcc-0a2a-4b7a-84e6-1fe39953bf23" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/dbf84582-fddb-4901-b4a0-de919bde12b7" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/3a4d8040-1efd-4791-bfb0-9a0ec3d0c2ae" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/23dfeb5e-d4c6-46ab-81c2-f1e6363dd4d3" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/7b4ce546-6fe7-453e-8ced-5e6ef0274c32" />

## Lab - C++ Qt Widgets Application using CMake and Conan
```
cd ~/conan-march-2026
git pull
cd Day3/qt-widget-application
ls -l
cat CMakeLists.txt
cat conanfile.py
cat MyDlg.h
cat MyDlg.cpp
cat main.cpp
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/5c73b76f-8e7f-41a8-a8fc-e9ed1b00b592" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/a7302d32-07ca-444e-b005-b4549d93e33a" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/88f8243c-4582-48d1-b694-4bc10ca88b09" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/bc87d643-75f2-4f0d-9cf5-99d6de381970" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/4f13d745-1c16-4bdd-9d43-fbd02675acf1" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/49768258-ea20-4b27-8026-49f1bdb7db83" />


Build and Run the application ( the interesting thing is I haven't installed Qt 6.x on my RHEL 10, CMake did the Qt installation for me
```
# Option 1 - You could install dependency this way 
conan install . --build=missing -c tools.system.package_manager:mode=install -c tools.system.package_manager:sudo=True

# Option 2 - You could also install dependency this way
conan install . --build=missing

## Option 1 - You could build the application this way
cmake -S . -B build/Release -DCMAKE_TOOLCHAIN_FILE=build/Release/generators/conan_toolchain.cmake  -DCMAKE_BUILD_TYPE=Release

# Option 2 - You could build the application this way
cmake --build build/Release

# Option 3 - You could also build the applicaiton this way
cmake --build --preset conan-release

# Here we are using the Conan virtual environment to run the Qt Widgets application
source build/Release/generators/conanrun.sh

# Run the Qt Widget application
build/Release/myQtApp
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/656d3af7-23d6-461d-a07c-3799032a31f6" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/3a797854-9718-48bb-a183-b0a53a261a03" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/3e03ca97-c74a-4bac-aec5-dc6b82fe0693" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/8ad516b3-8d87-4440-88a3-9d7149053677" />

## Lab - Using conan build command
If you have conan python recipe with build method defined, you could use the conan to build your application 
```
cd ~/conan-march-2026
git pull
cd Day3/qt-widget-application
ls -l
cat conanfile.py

conan build .

# Use the Conan virtual environment to the export the required tools path and environment variables before running your application
source build/Release/generators/conanrun.sh

# Run your application
build/Release/myQtApp
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/4dea6642-bf9e-42e9-b989-f39a385b8120" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/0378de91-6a12-4dc1-9894-56cf2ed15779" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-source build/conanrun.shattachments/assets/0394dffd-0503-450b-9a99-6a93b46d3d69" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/fd01f19c-a3b1-4c40-9d9a-13c6bb4256d5" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/5fa02c68-cfc4-4261-914e-af2a348762ae" />


## Lab - Conan export
<pre>
- What does it actually does When you run conan export ?
  - Conan performs two main tasks
    1. Copies the conanfile.py
	   - It takes your recipe and stores it in the local cache (usually ~/.conan2/p/...)
    2. Captures the "Recipe"
	   - It creates a unique reference for your package (e.g., hello/1.0@user/stable)
  - It does not compile any code
  - It only exports the instructions and any source files required to build the package later
- Why would you use it?
  - You use conan export when you want to make your library available to other projects on 
	your machine without fully building it yet
	
  - Source-only Packages
	- If you have a header-only library, exporting it is often all you need to do 
	  for others to use it
	
  - Testing Recipes
	- If you are debugging a complex conanfile.py, you might export it frequently to ensure Conan can parse the recipe and handle its metadata correctly.
	- Development of a Library
	  - If you are writing "Library A" and want "Project B" to be able to find it, 
	    you export "Library A" so it becomes a valid reference in your cache
</pre>

```
cd ~/conan-march-2026
git pull
cd Day3/qt-widget-application
ls -l
cat conanfile.py
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/c1aac44e-e3c7-4872-b8d0-31f701b99fb2" />

Let's export now
```
conan export .
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/9444c334-2b5d-466b-b835-5b783365625c" />

## Lab - Conan list
```
cd ~
conan list
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/1b93796b-a4d5-44ce-87dc-8ba9144573fa" />

## Info - Conan Profile
Understanding Conan Profiles
```
- A Conan Profile is essentially a configuration file that describes the environment
  where your code will be built or where it will eventually run

- Instead of typing long command-line arguments every time you want to install a library,
  you pack those settings into a profile.

- In modern Conan (2.0+), the system uses a two-profile approach:
  - Build Profile
    - Defines the machine doing the compiling (usually your laptop or a CI server)
  - Host Profile
    - Defines the machine where the compiled binary will actually execute
```

## Lab - Conan Profiles

Listing Conan profiles
```
conan profile list
```

Creating a Conan default profile
```
conan profile detect --force
```

View the default profile details
```
conan profile show -pr=default
```

Creates default profile if missing
```
conan profile detect
```

Find the path of the default profile
```
conan profile path default
```
