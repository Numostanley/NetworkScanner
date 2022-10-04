"""
script to run the wafw00f scan on the ip addresses
"""

import json
import subprocess

from .base import Scanner, get_server_user


class WafWoofScanner(Scanner):

    def __init__(self, ip_address: str, tool='wafw00f'):
        super(WafWoofScanner, self).__init__(ip_address, tool)
        self.ip_address = ip_address
        self.output_file = 'result.json'
        self.tool = tool

    def change_directory(self):
        # change directory to `/home/{$username}/tools/wafw00f` directory
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
        """execute waw00f command"""
        # change directory
        self.change_directory()

        # create ip_scans dir
        self.mkdir_ip_scans_dir()

        self.cmd.run(f'wafw00f {self.ip_address} -o ip_scans/{self.output_file} -f json',
                       shell=True)

        try:
            return self.cmd.run(f'cat ip_scans/{self.output_file}',
                                shell=True,
                                text=True,
                                capture_output=True).stdout
        finally:
            self.cmd.run(f'sudo rm ip_scans/{self.output_file}',
                           shell=True,
                           capture_output=True)

    def response(self):
        """return response"""
        return json.loads(self.scan())
