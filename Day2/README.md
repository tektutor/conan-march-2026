# Day 2

## Today's Agenda
<pre>
- Does Conan support GUI tools?
- Does Conan support binary package libraries for architectures other than x86_64 ?
- Understanding Conan Recipe
- Conanfile.txt vs Python Recipe 
- Conan text Recipe
- Conan Python Recipe
  
- Hands-on Lab Exercises
  - Develop a C++ application that depends on dynamic library with CMake
  - Develop a simple C++ application that depends on third-party library
    - We will be using Conan and CMake in this example
    - Understand how CMake integrates with conan package manager
    - Understand Conanfile.txt recipe
    - Supporting Debug and Release Build Types
  
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
</pre>


## Info - Does Conan support GUI Tools?
<pre>
- Officially, JFrog doesn't support any GUI tool for Conan but there are many community supported robust GUI tools
  - examples
    - Conan Explorer (conan-app-launcher)
    - Barbarian
    - Conan-GUI
- GUI Integrations available directly within popular IDEs
  - IDE Integrations
    - VS Code & CLion
      - Both editors have dedicated marketplace extensions for Conan
      - These extensions provide graphical menus to manage your profiles, search for packages and execute conan install
      - They integrate seamlessly with CMake, automating the generation and linking of your conanfile.txt dependencies 
        so you dont' have to step outside your editor
    - Qt Creator
      - Features a built-in Conan plugin
      - Once enabled, it can automatically setup the package manager 
    - Server Side Web UI
      - JFrog Artifactory Community Edition
        - If your goal is a GUI to manage remote packages rather than a local client then Artifactory CE provides a robuts
          Web UI
        - It is free for C/C++ packages and allows you to browse, manage and distribute your compiled binaries
          across your network
</pre>

## Info - Does Conan support binary package libraries for architectures other than x86_64 ?
<pre>
- Conan absolutely supports binary-level packages for architectures other than x86_64 but 
  it is limited in nature
- In fact, Conan's ability to manage binaries for any combination of OS, architecture and compiler
  is one of its core strength
- ConanCenter Remote Repository
  - provides extensive support for x86_64 architecture
  - limited support of binary packages for ARM or similar architecture
    - however, supports building binary packages for many architectures other than x86_64 from source code
  - Conan does support packages for Windows, Linux and Mac OS-X(supports M1, M2 & M3 applle silicon)  
  - Conan provides very minimal binary package libraries for Android
</pre>

## Info - Understanding Conan Recipe
<pre>
- A conanfile.txt or conanfile.py is a configuration file used by Conan C/C++ package manager
- It acts as a recipe that tells Conan which libraries your depends on and how to integrate them
  into your build system
- Think of it as the C/C++ equivalent of package.json used in NodeJS
  or requirements.txt used in Python
- Conan C/C++ package manager supports two formats
  1. conanfile.txt
  2. conanfile.py
</pre>

# Info - conanfile.txt
<pre>
- is used strictly for consuming packages, i.e downloading packages as binary/source, build and integrate with your application
- if you are building an application and just need to pull in thirdy-party libraries like Boost, Poco, or fmt, this is the
  simplest and recommended way to do it
</pre>

## Info - conanfile.py
<pre>
- Used for creating your custom Conan packages 
- When your consumption logic requires advanced Python scripting
- examples
  - Conditional dependencies based on the Operating System
</pre>

## Info - Conanfile.txt vs Conanfile.py
<pre>
- The fundamental difference comes down to simplicity vs power
- Use conanfile.txt
  - When you are building an application and your dependency needs are straight forward
  - You just wanted to download a few libraries (like fmt, nlohmann_json, or gtest ) to use in your project
  - Your list of dependencies does not change based on Operating System or Compiler
  - You want a configuration file that is extremely easy for beginners or non-C++ developerer to read and understand
- When to use conanfile.py
  - Use conanfile.py when you are writing a library that other people will use
    or when your application has complex build requirements
  - You wanted to export your code to Conan Server ( like Private JFrog Artifactory or Remote public ConanCenter )
    so that others can use your library
 - You need conditional dependencies
   - For example, you need wrappers on Windows, but POSIX libraries on LInux
 - You need to run custom scripts
   - If you need to download extra files from a custom url, run code generation scripts before compiling, or patch
     source code on the fly
 - You need to customize options programmatically
   - Like disabling a feature in dependency only if you are building a "Release" version of your application
</pre>

## Info - Conanfile.txt
<pre>
- Primary use-case - consuming packages
- Language - INI like plain text file
- can create packages - No
- Dynamic Logic - No (hard coding is the only option available)
- Learning curve - Easy
- Build System Hook - Static, relies entirely on generators
</pre>

## Info - Conanfile.py
<pre>
- Primary use-case - Creating packages (Libraries) & Advanced consumption
- Language - Python ( Need to subclass ConanFile )
- Can create package? - Yes
- Dynamic logic - Yes, if/elese OS checks, etc.,
- Learning Curve - Moderate to High
- Build System Hook - Deep Integration, can invoke CMake/Make directly
</pre>

## Info - Understanding a conanfile.txt recipe file
```
[requires]
fmt/10.1.1
zlib/1.3
poco/1.13.2

[tool_requires]
cmake/3.27.0

[generators]
CMakeDeps
CMakeToolChain

[layout]
cmake_layout

[options]
fmt/*:shared=False
zlib/*:shared=False
```

Let's understand the above conanfile.txt recipe
<pre>
- The file is written in simple INI-like format

- requires section
  - is the most critical section
  - it lists the libraries your project need to compile and run
  - you specify the package name and its version

 - tool_requires section
   - this is not a mandatory section, can be used when there is a need to specify 
     which version of CMake must be used to build the library
   - sometimes your project needs tools to build the code, rather than libaries to lin against
   - This section is used for build tools ( like CMake, Ninja or sepcific compilers ) that are
     only needed during the build process and won't be part of your final application

 - generators section
   - is the bridge between Conan and your build system
   - Once Conan downloads your dependencies, it need to tell your build system like CMake, Visual Studio,
     or Make where the header files and compiled binaries are kept
   - CMakeDeps - generates CMake configuration files ( xxx-config.cmake ) so you can use find_package() in 
     your CMakeLists.txt
  - CMakeToolChain - generatres a toolchain file that tells CMake to use Conan's evnvironment, compiler settings 
    and paths

- options section
  - Many C/C++ libraries can be compiled in different ways
  - For instance, as static libraries or shared dynamic libraries
  - This section, let you override the default options for the packages listed in [requires] section
  - The /* means that option applies to the package itself and any transitive dependencies 
  - You can toggle features, change linkage (shared=True/False) or set specific library configurations

- layout section
  - introducted in Conan v2.0+ to make local development smoother
  - the layout section tells Conan what directory structure your project uses
  - Using cmake_layout tells Conan to output the generated files into a standard CMake directory structure
    like build/Release or build/Debug, which prevents your root folder from getting cluttered
</pre>
