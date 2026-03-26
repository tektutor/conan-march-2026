# Day 4

## Today's Agenda
<pre>
- Finding the application dependencies
  
- Remote Repositories and Uploading
  - Default remotes: ConanCenter, Artifactory, custom
  - Adding/removing remotes
  - Uploading packages to a remote
  - Hands-on Lab
  
- Versioning and Package ID Management
  - Semantic versioning in Conan
  - Version ranges and constraints
  - Package ID modes and revisions
  - Lockfiles and reproducible builds
  - Hands-on Lab

- Profiles and Configuration Management
 - Creating and switching profiles
 - Cross-compilation with profiles
 - Custom settings, options, environment variables
 - Hands-on Lab

- Diamond Dependency Conflict Resolution
</pre>

## Lab - Find the application dependencies
```
cd ~/conan-march-2026
git pull
cd Day3/transitive-dependency
conan graph info .
conan graph info . --format=json > graph.json
conan graph info . --format=html > graph.html
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/7fbacb29-18ed-4a61-a0f2-27bc863b0a67" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/7c22fbe4-778b-4d50-9058-d31dc1977184" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/c4629e22-9fa0-49b9-80c0-9fa1674076da" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/e7aac599-992c-473a-b2ec-0ab35326ac48" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/b28cbdc8-2406-4d80-af71-81b7ba94d3d3" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/9bc2f258-a327-4646-96d3-105444a8c1cc" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/647f5cd5-3b83-4a63-86c6-e2efc4df03fa" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/5ec32c21-1c6c-4248-84fb-150095853c50" />


## Lab - Uploading your custom conan package to Remote Conan Repository
```
cd ~/conan-march-2026
git pull
cd Day4/simple-cpp-app
tree

podman volume create gitea-data

podman run -d --name gitea \  
  -p 3000:3000 \
  -v gitea-data:/data:Z \
  gitea/gitea:latest

podman ps

podman logs gitea

conan remote add my_gitea http://localhost:3000/api/packages/jegan/conan

conan remote login my_gitea jegan -p Root@123

cd lib
conan install . --build=missing
cmake --preset conan-release
cmake --build --preset conan-release
conan create . --build=missing

cd ..
conan install . --build=missing
cmake --preset conan-release
cmake --build --preset conan-release

conan upload "hello_lib/1.0:*" -r my_gitea -c
```

## Info - Versioning and Package ID Management
```
- Semantic versioning in Conan
  - In Conan, Semantic Versioning (SemVer) is the standard language used to communicate compatibility
    between packages
  - It follows the classic Major.Minor.Patch format (e.g., 1.2.3), but Conan adds powerful logic on
    top to handle version ranges and conflict resolution in complex C++ dependency graphs

- Version ranges and constraints
  - In your conanfile.txt or conanfile.py, you don't always have to hardcode a specific version
  - Conan allows Version Ranges, which let your project automatically pick the best available version
    within a safe boundary
  - [>1.0 <2.0] - Anything greater than 1.0 but less than 2.0
  - ~1.2 is equivalent to [>=1.2 <1.3], it allows patch updates only
  - ^1.2.3 is equivalent to [>=1.2.3 <2.0.0], it allows minor and patch updates
  - When using ranges, Conan will always resolve to the latest version that fits the range in your
    remote or local cache

- Package ID modes and revisions
  - The Package ID (The Binary Fingerprint)
    - The Package ID is a SHA-1 hash that represents a specific binary configuration
    - Even if the version is the same (fmt/11.0.2), you might have one Package ID for
      Windows/MSVC and another for Linux/GCC
    - Conan calculates this ID based on
      - Settings
        - OS
        - Compiler
        - Build Type
        - Architecture.
      - Options
        - Shared vs. Static
        - Header-only
      - Requirements
        - The versions of the libraries it links against

- Package ID Modes (Binary Compatibility)
  - This is where it gets interesting
  - If Library A depends on Library B, what happens if Library B moves from version 1.0.0 to 1.0.1?
  - Does Library A need a brand-new binary (a new Package ID), or can it reuse the old one?
  - Package ID Modes define this "Binary Compatibility" policy
  - Here are the most common ones
    - minor_mode(default)
      - A change in the Minor version of a dependency triggers a new Package ID
      - If fmt goes 11.0 -> 11.1, your app must be rebuilt
    - patch_mode
      - Even a Patch change in a dependency triggers a new Package ID
      - Very strict; ensures maximum safety but causes more rebuilds
    - major_mode
      - Only a Major version change triggers a new Package ID
      - Assumes the library is binary-compatible across minor updates
    - full_version_mode
      - Any change at all (even a revision) triggers a new Package ID
      - The most paranoid setting; used for safety-critical systems

- Lockfiles and reproducible builds
  - In the world of C++, a reproducible build is the "Holy Grail."
  - It means that if you build your project today, and your teammate builds it six months from now
    on a different machine, you both get the exact same binary output
  - In Conan, Lockfiles are the specialized tools that make this possible
  - Without them, even a small change in a remote repository (like a new patch version of fmt) could
    silently change your build
```

## Lab - Creating a Conan Lockfile
```
conan lock create . --version 1.0 --user jegan --channel stable
conan install . --lockfile=conan.lock

#Updating a lock file to support latest dependencies
conan lock create . --lockfile=conan.lock --update
```

## Lab - Diamond Dependency Issue
```
cd ~/conan-march-2026
git pull
cd Day4/diamond-dependency/logger/v1

# Build logger v1.0
conan install . --build=missing
cmake --preset conan-release
cmake --build --preset conan-release
conan create . --build=missing

# Build logger v2
cd ../v2
conan install . --build=missing
cmake --preset conan-release
cmake --build --preset conan-release
conan create . --build=missing
```
