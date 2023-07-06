# VulnScanner
This is a boilerplate for a network vulnerability scanning open-source application.

Details of how to run this project on a server can be accessed through the mkdocs file by running the following commands on your terminal;

```
# clone repository
git clone https://github.com/Numostanley/NetworkScanner.git
```

```
# enter the root directory
cd NetworkScanner
```

```
# enter the src directory
cd src
```

```
# Install all dependencies (assuming you already have Python >3.10 installed and a virtual environment set up).
pip install -r requirements.txt
```

```
# Go back to the root directory
cd ..
```

```
# enter the docs directory
cd docs
```

```
# run mkdocs command
mkdocs serve
```

This server-side application implements several network scanning tools including
nmap CVEScannerV2, Scanvus, Wapiti, Whatweb, SSlyze, Wafw00f, OWASP ZAP and Derbi.
