"""
script to run the wafw00f scan on the host
"""

import json
import subprocess

from .base import Scanner, get_server_user


class WafWoofScanner(Scanner):

    def __init__(self, ip_address: str, tool='wafw00f'):
        super(WafWoofScanner, self).__init__(ip_address, tool)
        self.ip_address = ip_address
        self.output_file = f'{ip_address}.json'
        self.tool = tool

    def change_directory(self):
        # change directory to `/home/{$username}/tools/wafw00f` directory
        self.server_os.chdir(f"/home/{get_server_user()}/tools/{self.tool}")

    def mkdir_ip_scans_dir(self):
        """create ip_scans directory"""
        try:
            # create ip_scans directory
            self.cmd.run(['mkdir', 'ip_scans'],
                         capture_output=True,
                         check=True)
        except subprocess.CalledProcessError:
            # if `mkdir ip_scans` command raises an error, skip because
            # ip_scans directory has already been created
            pass

    def scan(self):
        """execute waw00f command"""
        # change directory
        self.change_directory()

        # create ip_scans dir
        self.mkdir_ip_scans_dir()
        try:
            self.cmd.run(['wafw00f', f'{self.ip_address}', '-o', f'ip_scans/{self.output_file}', '-f', 'json'])

            # cd into ip_scans directory
            self.server_os.chdir("ip_scans")
            
            # open the JSON file to ensure it was created.
            with open(self.output_file, 'r') as f:
                json_output = f.read()
                
                return json_output
        finally:
            self.cmd.run(['rm', '-f', f'{self.output_file}'])

    def response(self):
        """return response"""
        return json.loads(self.scan())
