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



