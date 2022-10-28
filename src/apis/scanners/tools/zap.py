"""
script to run the zap scan on the host
"""

import json
import subprocess

from pathlib import Path

from apis.scanners.tools.base import Scanner
from apis.scanners.utils.extras import sanitize_host


class ZapScanner(Scanner):

    def __init__(self, ip_address: str, api_key: str, tool=''):
        super(ZapScanner, self).__init__(ip_address, tool)
        self.api_key = api_key
        self.host = ip_address
        self.output_file = f'{ip_address}.json'

    def change_directory(self):
        """change directory to locate the `scripts` path i.e VulnScan directory"""
        # retrieve the VulnScan directory
        path = Path(__file__).resolve().parent.parent.parent.parent.parent

        # append the scripts directory
        zap_script_path = f'{path}/scripts'

        # change the directory
        self.server_os.chdir(zap_script_path)

    def mkdir_ip_scans_dir(self):
        """create ip_scans directory"""
        try:
            # create ip_scans directory
            self.cmd.run('sudo mkdir ip_scans',
                         capture_output=True,
                         shell=True,
                         check=True)
        except subprocess.CalledProcessError:
            # if `mkdir ip_scans` command raises an error, skip because
            # ip_scans directory has already been created
            pass

    def scan(self):
        """execute zap script command"""
        self.change_directory()

        self.mkdir_ip_scans_dir()

        self.cmd.run(f'python3 ./zap_api_script.py '
                     f'{self.api_key} {self.host} --json_output=ip_scans/{sanitize_host(self.output_file)}')
        try:
            return open(self.output_file, 'r')
        finally:
            self.cmd.run(f'sudo rm -r ip_scans/{sanitize_host(self.output_file)}')

    def response(self):
        """return response"""
        return json.load(self.scan())
