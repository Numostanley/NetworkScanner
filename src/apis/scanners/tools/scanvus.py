"""
script to run the SCANVUS scan on the ip addresses
"""

import json
import subprocess

from apis.utils.error_logs import logger
from .base import Scanner, get_server_user


class ScanvusScanner(Scanner):
    """script to execute SCANVUS command to scan an IP address."""
    
    def __init__(self, ip_address: str, username: str, password: str, tool='scanvus'):
        super(ScanvusScanner, self).__init__(ip_address, tool)
        self.ip_address = ip_address
        self.username = username
        self.password = password
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
        
        if self.password:
            self.cmd.run(f'sudo python3 scanvus.py --assessment-type remote_ssh --host {self.ip_address} '
                                 f'--user-name {self.username} --password {self.password} '
                                 f'--save-vuln-report-json-path ip_scans/{self.output_file}',
                                 shell=True)
        
        # cd into ip_scans directory
        self.server_os.chdir("ip_scans")
        
        # open the JSON file to ensure it was created.
        with open(self.output_file, 'r') as f:
            json_output = f.read()
            
            return json_output
   
    def response(self):
        """return json object as response"""
        return json.loads(self.scan())
    
        