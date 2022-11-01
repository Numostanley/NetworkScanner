# How to deploy


## Server Setup

ssh into the server using username and password

```
ssh username@ip_address

then enter the username and password in the authentication prompt
```

**Example:**

```
ssh ubuntu@ip_address
```

ssh into the server using key (recommended)

```
ssh -i "my-key.pem" username@ip_address
```

**Example:**

```
ssh -i "my-key.pem" ubuntu@ip_address
```

**Run:**

```
sudo apt upgrade -y && sudo apt update
```


## Prerequisite Software Installations

**Redis:**
<br>
**Note: Advisable to configure Redis on another server**

```
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update

sudo apt-get install redis -y
```

**Nginx:**

```
sudo apt install nginx -y
```

**Python3-pip:**

```
sudo apt install python3-pip -y

pip install --upgrade pip
```

**Lua && Nmap:**

```
sudo apt-get install -y lua-sql-sqlite3

sudo apt-get install nmap -y
```

**Ruby:**

```
sudo apt install ruby-full -y

gem install address
```

**Java:**

```
sudo apt install openjdk-11-jre -y

sudo apt install openjdk-11-jdk -y
```

**Zap:**
<br>
**Note: Install and Modify ZAP's version to the latest version during deployment**

```
wget https://github.com/zaproxy/zaproxy/releases/download/v2.12.0/ZAP_2.12.0_Linux.tar.gz

tar -xf ZAP_2.12.0_Linux.tar.gz

mv ZAP_2.12.0 ZAP
```

**PhantomJS:**

```
sudo apt install phantomjs -y
```

**xvfb:**

```
sudo apt install xvfb -y
```


## Cloning Scanning Tools

Create `tools` directory and `cd` into the `tools` directory

**Example:**

```
mkdir tools && cd tools
```

**CVEScannerV2:**

```
git clone --recursive https://github.com/scmanjarrez/CVEScannerV2.git

cd CVEScannerV2/

pip3 install -r requirements.txt

python3 ./database.py
```

`cd` out of CVEScannerV2


**dirby:**

```
git clone https://github.com/BrainiacRawkib/dirby.git

cd dirby/

pip install -r requirements.txt
```

`cd` out of dirby


**ScreenShot (BigBrowser):**

```
git clone https://github.com/BrainiacRawkib/BigBrowser.git

cd BigBrowser/

pip install -r requirements.txt
```

`cd` out of BigBrowser


**scanvus:**

```
git clone https://github.com/Numostanley/scanvus.git

cd scanvus/

pip install -r requirements.txt
```

`cd` out of scanvus


**sslyze:**

```
git clone https://github.com/nabla-c0d3/sslyze.git

cd sslyze/

pip install --upgrade pip setuptools wheel

pip install --upgrade sslyze
```

`cd` out of sslyze


**wafw00f:**

```
git clone https://github.com/EnableSecurity/wafw00f.git

cd wafw00f/

python3 setup.py install
```

`cd` out of wafw00f


**WhatWeb:**

```
git clone https://github.com/urbanadventurer/WhatWeb.git
```


**Wapiti:**

```
sudo apt install wapiti -y
```


## VulnScanner repo Cloning

`cd` to the home directory and clone the VulnScanner repo

```
git clone https://github.com/CyberMeStudio/VulnScanner.git

cd VulnScanner/
```


## Create and Activate a Python virtual environment

`cd` to the VulnScanner directory: `cd VulnScanner/`

```
python3 -m venv venv

source venv/bin/activate
```


### Update pip and Install dependencies

```
pip install --upgrade pip

pip install -r requirements/prod.txt
```
