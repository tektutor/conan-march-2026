# Day 1

## Conan Overview
<pre>
- this is a package manager for C/C++ projects
- it is an opensource tool
- it works pretty much on any OS ( Windows, Mac OS-X, Linux distros )
- just like package manager is Linux distros 
- package manager is used
  - to install/uninstall/upgrade software tools
  - NodeJS
    - npm 
- example
  - Ubuntu - apt/apt-get as the package manager
</pre>

## Lab - Develop a simple C++ application that pulls information from a mysql database

#### Install MySQl DB Server
```
sudo apt update && sudo apt install -y mysql-server

sudo systemctl enable mysql
sudo systemctl start mysql
sudo systemctl status mysql

# Let's connect to mysql server using the below mysql client
mysql -u root -p
```

#### Install mysql db connector
```
sudo apt install -y libmysqlcppconn-dev
```

#### Let's setup our project directory structure
```
cd ~
mkdir -p mysql-cpp-demo/src
touch CMakeLists.txt
touch src/main.cpp
```  

## Lab - Install Conan Package Manager ( You dont' have to install this now )
``` 
sudo pip install conan
```



