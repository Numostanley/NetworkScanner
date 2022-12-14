"""
script to run the SSLYZE scan on the host
"""

import json
import subprocess

from apis.utils.error_logs import logger
from .base import Scanner, get_server_user


class SslyzeScanner(Scanner):
    """script to execute SSLYZE command to scan an IP address."""

    def __init__(self, ip_address: str, tool='sslyze'):
        super(SslyzeScanner, self).__init__(ip_address, tool)
        self.ip_address = ip_address
        self.output_file = f'{ip_address}.json'
        self.data = []
        self.tool = tool

    def change_directory(self):
        # cd to the SSLYZE directory
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
        
        self.cmd.run(['python3', '-m', 'sslyze', f'{self.ip_address}',
                                 f'--json_out=ip_scans/{self.output_file}'])   

        # cd into ip_scans directory
        self.server_os.chdir("ip_scans")
        
        # open the JSON file to ensure it was created.
        with open(self.output_file, 'r') as f:
            json_output = f.read()
            
            # parse the generated JSON file
            sslyze_result = json.loads(json_output)

            results = self.get_host_port_list(sslyze_result)
            return results

    def response(self):
        """return result in json format"""
        response = json.dumps(self.scan(), indent=4, sort_keys=True)
        return response

    def get_host_port_list(self, sslyze_result):
        """
        retrieve list of ports from the result
        """
        try:
        
            if sslyze_result["server_scan_results"][0]["scan_status"] == "ERROR_NO_CONNECTIVITY":
                # No connection was made with the server
                
                # delete the created file if an error occurred.
                subprocess.run(['rm', '-f', f'{self.output_file}'],
                            capture_output=True,
                            check=True)
                
                return {
                    "Response": "ERROR_NO_CONNECTIVITY"
                }
            elif sslyze_result["server_scan_results"][0]["scan_status"] == "COMPLETED":
                if sslyze_result["server_scan_results"][0]["scan_result"]["certificate_info"]["status"] == "COMPLETED":
                
                    result = {
                        "ip_address": sslyze_result["server_scan_results"][0]["server_location"]["ip_address"],
                        "port": sslyze_result["server_scan_results"][0]["server_location"]["port"],
                        "connection_type": sslyze_result["server_scan_results"][0]["server_location"]["connection_type"],
                        "scan_status": sslyze_result["server_scan_results"][0]["scan_status"],
                        "uuid": sslyze_result["server_scan_results"][0]["uuid"],
                        "date_scans_completed": sslyze_result["date_scans_completed"],
                        "date_scans_started": sslyze_result["date_scans_started"],
                        "connectivity_error_trace": sslyze_result["server_scan_results"][0]["connectivity_error_trace"],
                        "connectivity_result": sslyze_result["server_scan_results"][0]["connectivity_result"],
                        "connectivity_status": sslyze_result["server_scan_results"][0]["connectivity_status"],
                        "network_configuration": sslyze_result["server_scan_results"][0]["network_configuration"],
                        "scan_result": {
                            "certificate_info": {
                                "error_reason": sslyze_result["server_scan_results"][0]["scan_result"]["certificate_info"]["error_reason"],
                                "error_trace": sslyze_result["server_scan_results"][0]["scan_result"]["certificate_info"]["error_trace"],
                                "result": {
                                    "certificate_deployments": {
                                        "leaf_certificate_has_must_staple_extension": sslyze_result["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0][ "leaf_certificate_has_must_staple_extension"],
                                        "leaf_certificate_is_ev": sslyze_result["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["leaf_certificate_is_ev"],
                                        "leaf_certificate_signed_certificate_timestamps_count": sslyze_result["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["leaf_certificate_signed_certificate_timestamps_count"],
                                        "leaf_certificate_subject_matches_hostname": sslyze_result["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["leaf_certificate_subject_matches_hostname"],
                                        "ocsp_response": sslyze_result["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["ocsp_response"],
                                        "ocsp_response_is_trusted": sslyze_result["server_scan_results"][0]["scan_result"]["certificate_info"]["result"]["certificate_deployments"][0]["ocsp_response_is_trusted"],
                                        } 
                                },
                                "status": sslyze_result["server_scan_results"][0]["scan_result"]["certificate_info"]["status"],
                            }
                        }
                        
                    }
                else:
                    subprocess.run(['rm', '-f', f'{self.output_file}'],
                        capture_output=True,
                        check=True)
                    
                    return {
                        "Response": "SCAN_RESULT_CERTIFICATE_INFO_ERROR"
                    }
        except KeyError as e:
            # delete the created file if an error occured.
            subprocess.run(['rm', '-f', f'{self.output_file}'],
                        capture_output=True,
                        check=True)

            logger.error("Key Error")
            logger.error(e)
            return {
                "Response": f"Scan result does not contain {e}"
            }
        finally:
            subprocess.run(['rm', '-f', f'{self.output_file}'],
                        capture_output=True,
                        check=True)
            
        self.data.append(result)
        return self.data
