"""
script to run the dirb scan on the ip addresses
"""

import json
import subprocess

from .base import Scanner, get_server_user


class DirByScanner(Scanner):

    def __init__(self, ip_address, tool='dirby'):
        super(DirByScanner, self).__init__(ip_address, tool)
        self.ip_address = ip_address
        self.output_file = f'{ip_address}'
        self.tool = tool

    def change_directory(self):
        # change directory to `/home/{$username}/tools/dirby` directory
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
        """scan ip website with dirb"""
        # change directory
        self.change_directory()

        # create ip_scans dir
        self.mkdir_ip_scans_dir()

        # execute test_dirby.py
        self.cmd.run(f'python3 dirby.py --scheme https --host {self.ip_address} --port 443 '
                     '--wordlist ./wordlists/common.txt > ip_scans/result.json',
                     shell=True)
        try:
            return self.cmd.run('cat ip_scans/result.json',
                                shell=True,
                                text=True,
                                capture_output=True).stdout
        finally:
            self.cmd.run('sudo rm ip_scans/result.json', shell=True)

    def response(self):
        """return response"""
        data = json.loads(self.scan())
        report = filter(lambda x: x['code'] < 400, data['report'])
        response = {
            'base_url': data['base_url'],
            'host': data['host'],
            'port': data['port'],
            'report': list(report)
        }
        return response

    def run(self, *args, **kwargs):
        self.response()
