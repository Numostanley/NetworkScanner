# How to deploy


## Server Setup

ssh into the server using username and password

```
ssh username@ip_address

then enter the username and password in the authentication prompt
```

Example:

```
ssh ubuntu@ip_address
```

ssh into the server using key (recommended)

```
ssh -i "my-key.pem" username@ip_address
```

Example:

```
ssh -i "my-key.pem" ubuntu@ip_address
```

Run:

```sudo apt upgrade -y && sudo apt update```


## Prerequisite Software Installations

Redis (Note: Advisable to configure Redis on another server):

```
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis
```

Nginx:

```
sudo apt install nginx
```

Python3-pip

```
sudo apt install python3-pip
```


## Cloning Scanning Tools

Create `tools` directory and `cd` into the `tools` directory

Example:

```
mkdir tools && cd tools
```

CVEScannerV2:

```
git clone --recursive https://github.com/scmanjarrez/CVEScannerV2.git
```

Dirby:

```git clone https://github.com/BrainiacRawkib/dirby.git```

ScreenShot (BigBrowser):

```git clone https://github.com/BrainiacRawkib/BigBrowser.git```

Scanvus:

```git clone https://github.com/Numostanley/scanvus.git```

SSLyze:

```git clone https://github.com/nabla-c0d3/sslyze.git```

WafW00f

```git clone https://github.com/EnableSecurity/wafw00f```

WhatWeb

```git clone https://github.com/urbanadventurer/WhatWeb.git```

Wapiti

```sudo apt install wapiti```


### Some Scanning Tools Configuration

`cd` into each tool directory and install their dependencies 

CVEScannerv2:

```
cd CVEScannerV2/
pip3 install -r requirements.txt
python3 ./database.py
```

Dirby

```
cd dirby/
pip install -r requirements.txt
```


## VulnScanner repo Cloning

`cd` to the home directory and clone the VulnScanner repo

```git clone https://github.com/CyberMeStudio/VulnScanner.git```

```cd VulnScanner/```


## Create and Activate a Python virtual environment

`cd` to the VulnScanner directory: `cd VulnScanner/`

`python3 -m venv venv`

`source venv/bin/activate`


### Install dependencies

```pip install -r requirements/prod.txt```
