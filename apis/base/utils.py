import xmltodict
import re
import json
import subprocess
import os
from apis.utils.error_logs import logger


def CVE_Scan(ip_address: str):
    """Script to scan IP and convert output to JSON."""

    out_file = f"{ip_address}.xml"

    # change directory to ~/ (/home/{$username})
    os.chdir("../")

    # navigate to the CVEScannerV2 directory
    os.chdir("tools/CVEScannerV2")

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

    xml_content = subprocess.run(f'sudo nmap -oX ip_scans/{out_file} '
                                 f'-sV --script ./cvescannerv2.nse {ip_address}',
                                 shell=True)

    result = convert_to_json(out_file)

    return result


def convert_to_json(out_file: str):
    os.chdir("ip_scans")

    data = []

    # Convert the xml output to JSON
    try:
        with open(out_file, 'r') as f:
            xml_content = f.read()

            # parse nmap xml result to dict values
            nmap_results = xmltodict.parse(xml_content)

            nmap_dict = nmap_results['nmaprun']['host']['ports']['port']

            # clean and filter the dict values
            for port in nmap_dict:
                result = {
                    "port": port['@portid'],
                    "protocol": port['@protocol'],
                    "state": port['state']['@state'],
                    "service-name": port['service']['@name'],
                }

                port_index = nmap_dict.index(port)

                nmap_script = nmap_dict[port_index]['script']

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

                data.append(result)

            end_time = nmap_results['nmaprun']['host']['@endtime']
            start_time = nmap_results['nmaprun']['host']['@starttime']

            scan_time = {"Scan time": f"{int(end_time) - int(start_time)} secs"}

            data.append(scan_time)

    except KeyError as e:  # either host is down
        # or no open ports or CVEScan data

        subprocess.run(f'rm -f {out_file}',
                       capture_output=True,
                       shell=True,
                       check=True)

        logger.error("Key Error")
        logger.error(e)
        return {"message": "host is either down or has no open ports or CVEScan data"}

    # convert the cleaned data to JSON format.
    result = json.dumps(data, indent=4)
    return result



def sslyze_scan(ip_address: str):
    """Script to scan IP with SSLYZE scanner."""
    
    out_file = f'{ip_address}.json'
    
    # change directory to ~/ (/home/{$username})
    os.chdir("../")

    # navigate to the sslyze_json output directory
    os.chdir("tools/sslyze_json")
    
    scan_output = subprocess.run(f'python3 -m sslyze {ip_address} '
                                 f'--json_out={ip_address}.json',
                                 shell=True)
    
    with open(f'{ip_address}.json') as f:
        json_output = f.read()
        
        return json_output
    
    
    