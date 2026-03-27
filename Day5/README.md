# Day 5

## Today's Agenda
<pre>
- Understanding Conan Workflow
- Hands-on Lab

- Lockfile
- Hands-on Lab
  
- Integrating Conan in CI/CD Pipelines
  - Using Conan in Jenkins
  - Automating CI/CD with Conan, CMake & Jenkins
  - Hands-on Lab
    
- Best Practices and Troubleshooting
  - Clean cache and resolve conflicts
  - Dependency pinning strategies
</pre>

## Info - Conan Best Practices and Troubleshooting

#### Clean cache and resolve conflicts
<pre>
# Deleting specific package
conan remove "zlib/*"
</pre>

Version Conflicts
<pre>
- Conan uses a graph-based resolution
- If Package A wants OpenSSL/1.1 and Package B wants OpenSSL/3.0, Conan will throw a "Version Conflict" error
- Use the [overrides] section in your conanfile.txt or conanfile.py to force the entire graph to use a specific version
</pre>

#### Dependency pinning strategies
<pre>
- Version Ranges
  - You can use pkg/[>1.0 <2.0] to allow minor updates, but this is risky in C++ due to potential breaking changes in headers
  - Conan uses Recipe Revisions and Binary Revisions
  - To achieve true pinning, enable core:required_revisions = True in your conan.conf
  - This ensures that if a library author changes the recipe without changing the version number, your build won't silently change
- Lockfiles
  - Use conan lock create conanfile.py to generate a .lock file
  - This snapshots the exact versions, revisions, and options for every dependency in your graph
</pre>

## Lab - Lockfile
```
conan lock create .
cat conan.lock

# Use the lockfile to install dependencies
conan install . --lockfile=conan.lock

#This refreshes the lockfile with the latest available revisions
conan lock create . --update
```

<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/598d21c1-3af8-4318-bce3-6c0e2f246aeb" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/f5aff7bd-2c7e-4ac3-90e6-321f94035bae" />
