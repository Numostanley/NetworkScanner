"""
script to run the CVEScannerV2 scan on the host
"""

import json
import subprocess
import xmltodict

from apis.utils.error_logs import logger
from .base import Scanner, get_server_user


class CVEScanner(Scanner):
    """script to execute CVEScanner command to scan an IP address."""

    def __init__(self, ip_address: str, tool='CVEScannerV2'):
        super(CVEScanner, self).__init__(ip_address, tool)
        self.ip_address = ip_address
        self.output_file = f'{ip_address}.xml'
        self.data = []
        self.tool = tool

    def change_directory(self):
        # cd to the CVEScannerV2 directory
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
        """run the scan on the specified ip address"""
        # change directory
        self.change_directory()

        # create ip_scans dir
        self.mkdir_ip_scans_dir()

        # execute nmap script
        xml_content = self.cmd.run(['sudo', 'nmap', '-oX', f'ip_scans/{self.output_file}', 
                                     '-sV', '--script', './cvescannerv2.nse', f'{self.ip_address}'])

        # cd into ip_scans directory
        self.server_os.chdir("ip_scans")
        
        # open the xml file to ensure it was created.
        with open(self.output_file, 'r') as f:
            xml_file = f.read()
                    
        # parse nmap xml result to dict values
        nmap_results = xmltodict.parse(xml_file)
        
        json_result = json.dumps(nmap_results, indent=4, sort_keys=True)

        results = self.get_host_port_list(json_result)
        return results

    def response(self):
        """return result in json format"""
        response = json.dumps(self.scan(), indent=4, sort_keys=True)
        return response

    def get_host_port_list(self, json_result):
        """
        retrieve list of ports from the result
        """
        nmap_results = json.loads(json_result)
        
        try:
            nmap_port_list = nmap_results['nmaprun']['host']['ports']['port']
            
            for port in nmap_port_list:
                if isinstance(port, dict):
                    result = {
                        "port": port['@portid'],
                        "protocol": port['@protocol'],
                        "state": port['state']['@state'],
                        "service-name": port['service']['@name'],
                    }
                if isinstance(port, list):
                    result = {
                        "port": port[0],
                        "protocol": port[1],
                        "state": port[3]['@state'],
                        "service-name": port[2]['@name'],
                    }

                port_index = nmap_port_list.index(port)
                try:
                    nmap_script = nmap_port_list[port_index]['script']
                except KeyError:
                    continue
                try:
                    if isinstance(nmap_script, dict):
                        item_elements = nmap_script['elem']

                        cve_results = item_elements[5:]
                        CvE_Data = []

                        for item in cve_results:
                            
                            data =[value for value in item.split("\t")]
                            # cve_id, cvssv2, cvssv3, exploitdb, metasploit
                            if len(data) == 5:
                                cve_dict = {
                                    "cveid": data[0].strip(),
                                    "csvssv2": data[1].strip(),
                                    "csvssv3": data[2].strip(),
                                    "exploitdb": data[3].strip(),
                                    "metasploit": data[4].strip()
                                }

                                CvE_Data.append(cve_dict)
                             
                        if item_elements[0][:7] == 'product':
                            product = item_elements[0]
                            version = item_elements[1]
                        else:
                            product = None
                            version = None
                            
                        result.update({
                            "Product": product,
                            "version": version,
                            "cves": item_elements[3],
                            "CVE_Data": CvE_Data
                        })

                    if isinstance(nmap_script, list):
                        first_item = nmap_script[0]
                        item_elements = first_item['elem']

                        cve_results = item_elements[5:]
                        cve_data = []

                        for item in cve_results:
                            
                            data =[value for value in item.split("\t")]
                            # cve_id, cvssv2, cvssv3, exploitdb, metasploit
                            if len(data) == 5:
                                cve_dict = {
                                    "cveid": data[0].strip(),
                                    "csvssv2": data[1].strip(),
                                    "csvssv3": data[2].strip(),
                                    "exploitdb": data[3].strip(),
                                    "metasploit": data[4].strip()
                                }

                                cve_data.append(cve_dict)
                      
                        if item_elements[0][:7] == 'product':
                            product = item_elements[0]
                            version = item_elements[1]
                        else:
                            product = None
                            version = None
                            
                        result.update({
                            "Product": product,
                            "version": version,
                            "cves": item_elements[3],
                            "CVE_Data": cve_data
                        })

                    self.data.append(result)
                except UnboundLocalError:
                    pass
                
        except (KeyError, AttributeError) as e:  # either host is down
            # or no open ports

            logger.error("CVEScanner.get_host_port_list@Error")
            logger.error(e)
            pass
     
        finally:
            self.cmd.run(['rm', '-f', f'{self.output_file}'],
                        capture_output=True,
                        check=True)
        if self.data:
            return self.data
        else:
            return {
                "message": "host is either down or has no open ports or CVEScan data"
            }
