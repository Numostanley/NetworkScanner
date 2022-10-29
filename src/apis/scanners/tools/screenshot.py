"""
script to run the screenshot scan on the host
"""

import subprocess

from apis.utils.error_logs import logger
from apis.scanners.utils.extras import s3_filesystem_move, sanitize_host
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
            self.cmd.run(f'nmap -oX {self.xml_output_file} -sV {self.host}',
                         shell=True,
                         capture_output=True,
                         text=True,
                         check=True)

            # execute BigBrowser command and create bigbrowser_report/
            self.cmd.run(f'xvfb-run ./BigBrowser.py {self.xml_output_file} {self.host}',
                         shell=True,
                         capture_output=True,
                         text=True,
                         check=True)

            source = f'bigbrowser_report/{self.zip_output_file}'  # generated zip file
            destination = '/root/VulnScanner-AppData'

            # move source file to destination
            s3_filesystem_move(source, destination)
            return True
        except subprocess.CalledProcessError as e:
            logger.error('ScreenShotScanner.scan@Error')
            logger.error(e)
            return None
        finally:
            self.cmd.run(f'rm -r bigbrowser_report/{self.zip_output_file}')

    def response(self):
        """return response"""
        return self.scan()
