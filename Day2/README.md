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
