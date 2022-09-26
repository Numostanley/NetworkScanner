import xmltodict
import re
import json
import subprocess
import os
from apis.utils.error_logs import logger
from rest_framework.response import Response
from rest_framework import status



def convert_to_json(out_file):
    """Script to convert xml_output to Json."""
     
    os.chdir("ip_scans")
    
    data = []
      
    # Clean and filter the dict values.
    try:
        with open(out_file, 'r') as f:
            xml_content = f.read()
            
            # parse nmap xml result to dict values
            nmap_results = xmltodict.parse(xml_content)
        
            nmap_dict = nmap_results['nmaprun']['host']['ports']['port']
          
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
                
                end_time = nmap_results['nmaprun']['host']['@endtime']
                start_time = nmap_results['nmaprun']['host']['@starttime']
                
                scan_time = {"Scan time": f"{int(end_time) - int(start_time)} secs"}
                
                result.update(scan_time)    
                data.append(result)
                
                #save the cleaned data in JSON format.
                result = json.dumps(data, indent=4)
                return result
    
    except KeyError as e: # either host is down
        # or no open ports or CVEScan data
        
        subprocess.run(f'rm -f {out_file}',
                    capture_output=True,
                    shell=True,
                    check=True)
        
        logger.error("Key Error")
        logger.error(e)
        return {"message" : "host is either down or has no open ports or CVEScan data"}
        
    
    