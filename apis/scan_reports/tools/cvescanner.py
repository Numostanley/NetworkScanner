"""
script to run the CVEScannerV2 scan on the ip addresses
"""

import json
import subprocess

import xmltodict
import re
from apis.utils.error_logs import logger
from .base import Scanner


class CVEScanner(Scanner):
    """script to execute CVEScanner command to scan an IP address."""

    def __init__(self, ip_address: str, tool='CVEScannerV2'):
        super().__init__(tool, ip_address)
        self.ip_address = ip_address
        self.output_file = f'{ip_address}.xml'
        self.data = []
        self.tool = tool

    def change_directory(self):
        # change directory to ~/ (/home/{$username})
        self.server_os.chdir("../")

        # cd to the CVEScannerV2 directory
        self.server_os.chdir(f"/home/{self.server_user()}/tools/{self.tool}")

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
        """run the scan on the specified ip address"""
        # change directory
        self.change_directory()

        # create ip_scans dir
        self.mkdir_ip_scans_dir()

        # execute nmap script
        xml_content = self.cmd.run(f'sudo nmap -oX ip_scans/{self.output_file} '
                                     f'-sV --script ./cvescannerv2.nse {self.ip_address}',
                                     shell=True)

        # cd into ip_scans directory
        self.server_os.chdir("ip_scans")
        
        # open the xml file to ensure it was created.
        with open(self.output_file, 'r') as f:
            xml_file = f.read()
            
            # parse nmap xml result to dict values
            nmap_results = xmltodict.parse(xml_file)

            results = self.get_host_port_list(nmap_results)
            return results

    def response(self):
        """return result in json format"""
        response = json.dumps(self.scan(), indent=4, sort_keys=True)
        return response

    def get_host_port_list(self, nmap_results):
        """
        retrieve list of ports from the result
        """

        nmap_port_list = nmap_results['nmaprun']['host']['ports']['port']
        try:
            for port in nmap_port_list:
                result = {
                    "port": port['@portid'],
                    "protocol": port['@protocol'],
                    "state": port['state']['@state'],
                    "service-name": port['service']['@name'],
                }

                port_index = nmap_port_list.index(port)

                nmap_script = nmap_port_list[port_index]['script']

                if isinstance(nmap_script, dict):
                    item_elements = nmap_script['elem']

                    cve_results = item_elements[5:]
                    CvE_Data = []

                    for item in cve_results:
                        cve_id, cvssv2, cvssv3, exploitdb, metasploit = re.split(r"\t+", item)

                        cve_dict = {
                            "cveid": cve_id.strip(),
                            "csvssv2": cvssv2.strip(),
                            "csvssv3": cvssv3.strip(),
                            "exploitdb": exploitdb.strip(),
                            "metasploit": metasploit.strip()
                        }

                        CvE_Data.append(cve_dict)

                    result.update({
                        "Product": item_elements[0],
                        "version": item_elements[1],
                        "cves": item_elements[3],
                        "CVE_Data": CvE_Data
                    })

                if isinstance(nmap_script, list):
                    first_item = nmap_script[0]
                    item_elements = first_item['elem']

                    cve_results = item_elements[5:]
                    CvE_Data = []

                    for item in cve_results:
                        cve_id, cvssv2, cvssv3, exploitdb, metasploit = re.split(r"\t+", item)

                        cve_dict = {
                            "cveid": cve_id.strip(),
                            "csvssv2": cvssv2.strip(),
                            "csvssv3": cvssv3.strip(),
                            "exploitdb": exploitdb.strip(),
                            "metasploit": metasploit.strip()
                        }

                        CvE_Data.append(cve_dict)

                    result.update({
                        "Product": item_elements[0],
                        "version": item_elements[1],
                        "cves": item_elements[3],
                        "CVE_Data": CvE_Data
                    })

                self.data.append(result)

            end_time = nmap_results['nmaprun']['host']['@endtime']
            start_time = nmap_results['nmaprun']['host']['@starttime']

            scan_time = {"Scan time": f"{int(end_time) - int(start_time)} secs"}

            self.data.append(scan_time)

        except KeyError as e:  # either host is down
            # or no open ports or CVEScan data

            # delete the created file if an error occured.
            subprocess.run(f'rm -f {self.output_file}',
                        capture_output=True,
                        shell=True,
                        check=True)

            logger.error("Key Error")
            logger.error(e)
            return {"message": "host is either down or has no open ports or CVEScan data"}

        return self.data
