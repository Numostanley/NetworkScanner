"""
script to run the dirb scan on the ip addresses
"""

import subprocess

from .base import Scanner


class DirBScanner(Scanner):

    def __init__(self, ip_address, tool='dirb'):
        super(DirBScanner, self).__init__(ip_address, tool)
        self.ip_address = ip_address
        self.output_file = f'{ip_address}'
        self.tool = tool

    def change_directory(self):
        # change directory to ~/ (/home/{$username})
        self.server_os.chdir("../")

    def mkdir_ip_scans_dir(self):
        pass

    def scan(self):
        """scan ip address with dirb"""
        self.change_directory()
        return subprocess.run(f'dirb https://{self.ip_address}/')

    def response(self):
        return self.scan()
