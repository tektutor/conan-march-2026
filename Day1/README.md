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
- it uses a conanfile.txt or conafile.py recipe file as the input
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

## Info - Why use Conan?
<pre>
- Application Binary Interface(ABI) compatibility
  - It ensures you don't lik a debug library into a application built in Release mode (this could cause application crashes)
- Transitive Dependencies
  - It handles the Graph
    - If Library A depends on B
    - B depends onC
    - Conan solves the math for you
- Reproducibility
  - Using lockfiles, you can generate that your CI/CD builds the exact same code as your developer machine
- Cross-Platform
  - The same conanfile.py or conanfile.txt will work on Windows(Visual Studio), Linux (GCC) and Mac OS-X(Clang)
</pre>  

## Info - Alternate tools for Conan
<pre>
- vcpkg, hunter, qmake, etc.,  
</pre>

## Info - vcpkg(The modern standard)
<pre>
- created by Microsoft but now is a cross-platform tool
- vcpkg is current the one of the most popular choice for C++ developers
- How it works?
  - it uses a manifes file called vcpkg.json in your project root
  - when you run CMake, vcpkg automatically downloads and builds those libraries into a local folder
- Advantagess
  - Huge Library ( 2000+ packages), execellent IDE integration, and manifest mode that ensures everyone on your team
    uses the same version of the library
- Disadvantages
  - it builds everything from source code by default, which can take a long time on the first run
</pre>

## Info - Hunter
<pre>
- it is CMake's native dependency management tool
- is unique because it is written entirely in CMake code, hence we don't need to install any other tool to get hunter
- How it works?
  - You add a few lines to your CMakeLists.txt to gate the project
  - It then handles downloading and building dependencies during the cmake configuration step
- Advantages
  - Zero external dependencies, if you have CMake installed already then you have hunter by default
  - It follows pure CMake philosophies perfectly
- Disadvantages
  - Much smaller library(repository) than vcpkg or conan
  - It can significantly slow down your intinial configuration time becuase CMake is doing the heavy-lifting of dependency management
  - CMake is good as meta-build system, hence not an ideal choice for dependency management
</pre>

## Info - Conan v1.x vs v2.x
<pre>
- Conan believes the core philosophy - that everything is a graph
- Conan v1.x
  - Treats dependencies more like a flat list
  - It often struggles with diamond dependencies
  - where two libraries depend on differnt versions of a third library 
  - requires complex workaround to deal with the diamond dependency issue
- Conan v2.x
  - Built on a rigorous dependency graph model
  - every version conflict or configuration mismatch is caught during the intial graph resolution, before a single file is downloaded
  - I wouldn't say diamond dependency issue will not happen in Conan v2.x, whenever it encounters such dependency issues, it will let us manually
    resolve that like how git handles the automatic merge, in case it files a merge conflict which can't be automatically resolved, it will
    report the issue and let us deal with it manually
</pre>

## Info - Conan High-Level Architecture
![conan](Conan-HighLevel-Architecture.png)

## Info - Installing Conan 
```
pip install conan
```

## Lab - Hello World C++ projec with CMake
```
cd ~/conan-march-2026
cd Day1/
mkdir -p hello/{src,inc}
touch src/main.cpp src/hello.cpp inc/hello.h
touch CMakeLists.txt
tree
```

<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/bc0e49d5-8a8e-42fc-ba02-816f6f7d1173" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/c5c7c929-7419-43a6-b670-4632db4e707b" />


Build and run the application using cmake
```
cd ~/conan-march-2026
git pull
Day1/hello

mkdir build && cd build
cmake ..
cmake --build .
```

<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/93ad5bd5-e229-4a6c-acda-2535bf7a8c9f" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/5d596b67-4996-446d-8e57-93285fb82b78" />
