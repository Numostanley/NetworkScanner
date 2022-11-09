"""
script to run the screenshot scan on the host
"""

import subprocess

from apis.utils.error_logs import logger
from apis.scanners.utils.extras import sanitize_host
from core.extras import env_vars
from .base import Scanner, get_server_user


class ScreenShotScanner(Scanner):

    def __init__(self, ip_address: str, tool='BigBrowser'):
        super(ScreenShotScanner, self).__init__(ip_address, tool)
        self.host = ip_address
        self.xml_output_file = f'{sanitize_host(self.host)}.xml'
        self.zip_output_file = f'{sanitize_host(self.host)}.zip'
        self.tool = tool

    def change_directory(self):
        # change directory to `/home/{$username}/tools/BigBrowser` directory
        self.server_os.chdir(f"/home/{get_server_user()}/tools/{self.tool}")

    def mkdir_ip_scans_dir(self):
        pass

    def scan(self):
        """execute BigBrowser"""
        # change directory
        self.change_directory()

        try:
            # scan host with nmap
            self.cmd.run(['nmap', '-oX', f'{self.xml_output_file}', '-sV', f'{self.host}'],
                         capture_output=True,
                         check=True)

            # execute BigBrowser command and create bigbrowser_report/
            self.cmd.run(['xvfb-run', './BigBrowser.py', f'{self.xml_output_file}', f'{self.host}'],
                         capture_output=True,
                         check=True)

            source_file = f'bigbrowser_report/{self.zip_output_file}'  # generated zip file from BigBrowser.py
            destination = env_vars.S3_DIR_PATH

            # move source file to destination
            self.cmd.run(['cp', f'{source_file}', f'/home/{get_server_user()}/{destination}'])
            return True
        except subprocess.CalledProcessError as e:
            logger.error('ScreenShotScanner.scan@Error')
            logger.error(e)
            return None
        finally:
            self.cmd.run(['rm', '-r', f'bigbrowser_report/{self.zip_output_file}', f'{self.xml_output_file}'],
                         capture_output=True)

    def response(self):
        """return response"""
        return self.scan()
