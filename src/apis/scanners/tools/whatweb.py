"""
script to run the whatweb scan on the ip addresses
"""

import json
import subprocess

from .base import Scanner, get_server_user


class WhatWebScanner(Scanner):

    def __init__(self, ip_address: str, tool='WhatWeb'):
        super(WhatWebScanner, self).__init__(ip_address, tool)
        self.ip_address = ip_address
        self.output_file = f'{ip_address}.json'
        self.tool = tool

    def change_directory(self):
        # change directory to `/home/{$username}/tools/WhatWeb` directory
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
        """execute WhatWeb command"""
        # change directory
        self.change_directory()

        # create ip_scans dir
        self.mkdir_ip_scans_dir()

        try:
            self.cmd.run(f'./whatweb {self.ip_address} '
                           f'--log-json=ip_scans/{self.output_file}',
                           shell=True)
            return self.cmd.run(f'cat ip_scans/{self.output_file}',
                                  shell=True,
                                  text=True,
                                  capture_output=True).stdout
        finally:
            self.cmd.run(f'sudo rm ip_scans/{self.output_file}', shell=True)

    def response(self):
        """return response"""
        return json.loads(self.scan())

    def run(self, *args, **kwargs):
        self.response()
