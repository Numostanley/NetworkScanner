"""
script to run the wapiti scan on the ip addresses
"""

import json
import subprocess

from apis.utils.error_logs import logger
from .base import Scanner, get_server_user


class WapitiScanner(Scanner):
    """script to execute wapiti command to scan an IP address."""
    
    def __init__(self, ip_address: str, tool='wapiti'):
        super(WapitiScanner, self).__init__(ip_address, tool)
        self.ip_address = ip_address
        self.output_file = f'{ip_address}.json'
        self.data = []
        self.tool = tool

    def change_directory(self):
        # cd to the wapiti directory
        self.server_os.chdir(f"/home/{get_server_user()}/tools/{self.tool}")

    def mkdir_ip_scans_dir(self):
        """create ip_scans directory"""
        try:
            # create ip_scans directory
            self.cmd.run(f'mkdir ip_scans',
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
        
        # cd into ip_scans directory
        self.server_os.chdir("ip_scans")
        
        # create json file for the ip to be scanned
        try:
            self.cmd.run(f'sudo touch {self.output_file}',
                        capture_output=True,
                            shell=True,
                            check=True)
        except subprocess.CalledProcessError:
            # if `type > {output_file}` command raises an error, skip because
            # output_file has already been created
            pass
        
        self.cmd.run(f"wapiti -u https://{self.ip_address}/"
                        f" -f json -o /home/{get_server_user()}/tools/{self.tool}/ip_scans/{self.output_file}",
                        shell=True)
        
        # open the JSON file to ensure it was created.
        with open(self.output_file, 'r') as f:
            json_output = f.read()
            
            wapiti_result = json.loads(json_output)
            
            results = self.get_host_port_list(wapiti_result)
        return results
        
    def response(self):
        """return result in json format"""
        response = json.dumps(self.scan(), indent=4, sort_keys=True)
        return response
    
    def get_host_port_list(self, wapiti_result):
        """
        retrieve list of vulnerabilities from the result
        """
        try:
            
            result = [
                wapiti_result['vulnerabilities'],
                wapiti_result['anomalies'],
                wapiti_result['infos'],
            ]
            
            for re in result:
                self.data.append(re)
                
        except KeyError as e: # no vulnerability data
            subprocess.run(f'sudo rm -f {self.output_file}',
                        capture_output=True,
                        shell=True,
                        check=True)

            logger.error("Key Error")
            logger.error(e)
            return {"Response": f"Scan result does not contain {e}"}
        
        finally:
            subprocess.run(f'sudo rm -f {self.output_file}',
                        capture_output=True,
                        shell=True,
                        check=True)
             
        return self.data

