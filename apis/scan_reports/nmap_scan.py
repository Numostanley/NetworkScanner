"""
script to run the nmap scan on the ip addresses
"""

import json
import os
import subprocess

import xmltodict


def scan_ip_address(ip_address: str):
    """script to execute NMAP command to scan an IP address."""
    output_file = f'{ip_address}.xml'

    # change directory to ~/ (/home/{$username})
    os.chdir("../")

    # navigate to the CVEScannerV2 directory
    os.chdir("CVEScannerV2")

    try:
        # create ip_scans directory
        subprocess.run('mkdir ip_scans',
                       capture_output=True,
                       shell=True,
                       check=True)
    except subprocess.CalledProcessError:
        # if `mkdir ip_scans` command raises an error, skip because
        # ip_scans directory has already been created
        pass

    # execute nmap script
    xml_content = subprocess.run(f'sudo nmap -oX ip_scans/{output_file} '
                                 f'-sV --script ./cvescannerv2.nse {ip_address}',
                                 shell=True)

    # parse nmap xml result to dict values
    nmap_results = xmltodict.parse(xml_content)

    data = []
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

            if isinstance(nmap_script, list):
                first_item = nmap_script[0]
                item_elements = first_item['elem']
                result.update({
                    "version": item_elements[1],
                    "cves": item_elements[3],
                    "cveid": "",
                    "csvssv2": "",
                    "csvssv3": "",
                    "exploitdb": "",
                    "metasploit": ""
                })

            if isinstance(nmap_script, dict):
                item_elements = nmap_script['elem']
                result.update({
                    "version": item_elements[1],
                    "cves": item_elements[3],
                    "cveid": "",
                    "csvssv2": "",
                    "csvssv3": "",
                    "exploitdb": "",
                    "metasploit": ""
                })

            data.append(result)
    except KeyError:  # no open ports
        pass

    # return result in json format
    result = json.dumps(data, indent=4, sort_keys=True)
    return result
