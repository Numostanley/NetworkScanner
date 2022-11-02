"""
script to run the dirby scan on the host
"""

import json

from .base import Scanner, get_server_user


class DirByScanner(Scanner):

    def __init__(self, ip_address, tool='dirby'):
        super(DirByScanner, self).__init__(ip_address, tool)
        self.host = ip_address
        self.tool = tool

    def change_directory(self):
        # change directory to `/home/{$username}/tools/dirby` directory
        self.server_os.chdir(f"/home/{get_server_user()}/tools/{self.tool}")

    def mkdir_ip_scans_dir(self):
        pass

    def scan(self):
        """scan ip website with dirby"""
        # change directory
        self.change_directory()

        # execute dirby.py
        self.cmd.run(['python3', 'dirby.py', '--scheme', 'https', '--host', f'{self.host}', '--port', '443', 
                     '--wordlist', './wordlists/common.txt'])
        try:
             return open('result.json', 'r')
        finally:
            self.cmd.run(['rm', 'result.json'])

    def response(self):
        """return python object as response"""
        return json.load(self.scan())
