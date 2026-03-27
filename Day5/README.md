# Day 5

## Today's Agenda
<pre>
- Understanding Conan Workspace
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

## Lab - Conan workspace
```
cd ~/conan-march-2026
git pull
cd Day5/conan-workspace
tree
cat conanws.yml
cat build.sh
./build.sh
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/4d076b20-916a-477d-9ee9-9e21cad3f684" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/d78fc194-1b1a-4f13-b9fc-5881b6e19615" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/5a76aa91-b233-451a-8683-6bd696d9f28f" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/76374f2e-ff83-4646-aded-f5a68e8dcb77" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/30e37084-aa55-4347-993c-73ac2f0512eb" />


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

<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/74b42633-dbe5-41ba-bc24-948853339169" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/eb7d384e-b724-47b6-956c-072afb6140a4" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/7b95bfc8-c414-400f-9dd7-69953593db53" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/5f89ff9e-d903-47cf-a3ab-39dc38e709fe" />

## Lab - Setup Jenkins Continuous Integration Build Server
You could download Jenkins war file from official page https://www.jenkins.io/download/

```
cd ~/Downloads
# Launch Jenkins
java -jar ./jenkins.war
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/b7a334e3-1dd4-4491-988b-1a725a604b35" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/2e7a5ad4-805c-4473-aa68-3fe59ab3d22b" />
Access your Jenkins dashboard from your preferred web browser http://localhost:8080
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/ab9cc687-8eb7-4f73-8424-b00d24d0b25c" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/d49dd089-9da0-4b8a-81a2-0830c38136ba" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/b9313ce3-e32c-4c77-a56c-2c2769d7df55" />
Let's select the "Install Suggested Plugins"
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/895062db-dded-4e99-9b80-947423756458" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/fcb01e0f-ae3d-4d6d-9edb-75b6bc27bfe1" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/9d467877-f460-4756-b995-b80865f0700a" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/016430c7-fd1e-41a6-a857-3e7d86820780" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/103b1524-b0b0-4f21-96b0-9e0560caedeb" />
Let's create an admin user
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/ce8d0377-a6e4-49ec-a0ca-46d1a8efa4db" />
Click "Save and Continue"
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/2ab285e6-2bb1-4cc4-a0fa-45a48a2c9bdf" />
Click "Save and Finish"
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/1afb111b-d072-4eaa-865b-5596629178c0" />
Click "Start using Jenkins"
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/781d7a3b-c95c-4e84-b9cb-f8ccc13d6efa" />


Let's create a Jenkins CI Job
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/7d11d2fe-cfd5-471a-8c3f-15935edbe232" />
Select "Freestyle"
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/df7fcfdc-22c8-4c34-be71-b0f5c96738ba" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/96e1949e-0fe3-43bd-a1fa-2cd09988ec90" />
General section
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/9f794f0a-008b-4736-8d16-0b08fbce043a" />
Source Code Management
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/8e326bbb-88f8-4245-acae-a9922903a4bd" />
Triggers Section
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/9e2be9a6-5fb0-4193-90cd-ab3a12cb3922" />
Build Steps --> Select "Execute Shells"
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/d57f5f27-511e-476c-9782-cc314a37279c" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/4c82ba3c-d0a5-46ad-9621-4bbc3ca97fc7" />
Click "Save"
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/2a75821e-7607-46d0-adba-032ed8ef15ac" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/02437871-4c7c-48e8-80c6-6788d4fa1713" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/3d9e8349-fe64-4fa5-9d8f-3d9e080e0326" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/8b1a9ba2-47f7-4d1a-b2ff-be605d6350eb" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/496a011b-cbef-4c21-8d08-75a69a1ca7b8" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/7bcfc621-392c-4f26-973d-6f917d82b0bb" />

## Lab - Deleting individual conan package from Local cache
```
conan remove "logger/*" -c
```

## Lab - Deleting all the packages from Local cache
```
conan remove "*" -c
```
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/1026b1c4-7696-4da1-9c57-4e68c6a7c00c" />
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/b6585600-3326-4af4-b9c5-f8cba78bc58e" />


