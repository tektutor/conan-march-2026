# Day 1

## Today's agenda
<pre>
- CMake Overview
  
- Introduction to Conan
  - What is Conan?
  - Why use a package manager for C/C++ applications?
  - Comparision with vcpkg, hunter and system-level package managers
  - Conan 1.x vs Conan 2.x
  
- Setup up the environment
  - Installing Conan v2.x

- CMake High-Level Architecture
- Conan High-Level Architecture

Hands-on Lab exercises
- Develop a C++ application with CMake
- Develop a C++ application that depends on static library with CMake
- Develop a C++ application that depends on dynamic library with CMake
- Develop a simple C++ application that depends on third-party library
  - We will be using Conan and CMake in this example
  - Understand how CMake integrates with conan package manager
  - Understand Conanfile.txt recipe
  - Supporting Debug and Release Build Types 
</pre>

## Info - CMake Overview
<pre>
- CMake is a build system generator
- it is not really a build tool, it depends on other build tools like Make, Ninja, MSBuild, etc.,
- in other words, it is a meta-build system
- is a Transpiler for Build Systems
- it takes CMakeLists.txt as input and transpiles it into a massive graph of dependencies and build rules
- it is opensource and a cross-platform meta-build system
- all our build instructions we will be writing in the CMakeLists.txt
- CMake reads the CMakeLists.txt and checks your system for compilers and your application dependencies
- it is a target based system
- it follows 3 stage workflow
  1. Configuration
     - Reads CMakeLists.txt, builds a dependency graph, caches system variables in CMakeCache.txt
  2. Generation
     - Produces the native build files for the chosen "Generator"
       e.g Makefile, Ninja, Visual Studio Solution file, etc.,
  3. Build
     - Invokes the underlying build tool to compile the source code into binaries
- Advantages
  - Out of source builds
   - By building in a separate /build directory, the source tree remains clean
   - no *.o, obj files will not clutter your code as intermediate files and binaries files will be generated in a separate folder
     typically build folder
   - independent of compiler
     - it can switch between GCC, Clang, MSVC without changing  a single line of project code
   - Extensibility
     - Features like FetchContent allows CMake to automatically download and integrate external Git Repositories during the 
       configuration phase
</pre>


## Info - CMake High Level Architecture
![architecture](CMake-HighLevel-Architecture.png)

## Info - Conan Overview
<pre>
- Conan is a package manager for C/C++ applications
- it is opensource tool and cross-platform tool
- Just like
  - NPM for NodeJS or Javascript languages
  - nuget for Visual Studio
  - pip for Python
  - Package Managers on the OS level
    - apt or apt-get, yum, rpm, dnf, etc.,
- Conan installs third-party packages on a project level
- Conan also supports transitive dependencies
  - Your application depends on Library A
  - Library A depends on B
  - B in turn depends on C
 </pre>

