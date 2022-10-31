"""
script to run the SCANVUS scan on the host
"""

import json
import subprocess

from .base import Scanner, get_server_user


class ScanvusScanner(Scanner):
    """script to execute SCANVUS command to scan an IP address."""
    
    def __init__(self, ip_address: str, username: str, password: str, key: str, tool='scanvus'):
        super(ScanvusScanner, self).__init__(ip_address, tool)
        self.ip_address = ip_address
        self.username = username
        self.password = password
        self.key = key
        self.output_file = f'{ip_address}.json'
        self.data = []
        self.tool = tool
        
    def change_directory(self):
        # cd to the SCANVUS directory
        self.server_os.chdir(f"/home/{get_server_user()}/tools/{self.tool}")
        
    def mkdir_ip_scans_dir(self):
        """create ip_scans directory"""
        try:
            # create ip_scans directory
            self.cmd.run('mkdir ip_scans',
                           capture_output=True,
                           shell=True,
                           check=True)
        except subprocess.CalledProcessError:
            # if `mkdir ip_scans` command raises an error, skip because
            # ip_scans directory has already been created
            pass
        
    def scan(self):
        """run the scan on the specified ip address"""
        # change directory
        self.change_directory()

        # create ip_scans dir
        self.mkdir_ip_scans_dir()

        # if password is given, execute scanvus with the username and password
        if self.password:
            self.cmd.run(f'python3 scanvus.py --assessment-type remote_ssh --host {self.ip_address} '
                                 f'--user-name {self.username} --password {self.password} '
                                 f'--save-vuln-report-json-path ip_scans/{self.output_file}',
                                 shell=True)

        # if key is given, execute scanvus with the username and key
        if self.key:
            self.cmd.run(f'python3 scanvus.py --assessment-type remote_ssh --host {self.ip_address} '
                                 f'--user-name {self.username} --key ~/tools/keys/{self.key} '
                                 f'--save-vuln-report-json-path ip_scans/{self.output_file}',
                                 shell=True)

        self.cmd.run(f'rm ~/tools/keys/{self.key}', shell=True)

        # cd into ip_scans directory
        self.server_os.chdir("ip_scans")
        try:
            # return an opened file
            with open(self.output_file, 'r') as f:
                opened_file = f.read()
            return opened_file

        except FileNotFoundError: #Error in scan credentials
            return json.dumps({"message":"Scan unsuccessful. Check credentials."})

        finally:
            subprocess.run(f'rm -f {self.output_file}',
                        capture_output=True,
                        shell=True,
                        check=True)

    def response(self):
        """return json object as response"""
        return json.loads(self.scan())
