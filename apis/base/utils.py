import json
import subprocess
import os



def sslyze_scan(ip_address: str):
    """Script to scan IP with SSLYZE scanner."""
    
    out_file = f'{ip_address}.json'
    
    # change directory to ~/ (/home/{$username})
    os.chdir("../")

    # navigate to the sslyze_json output directory
    os.chdir("tools/sslyze_json")
    
    scan_output = subprocess.run(f'python3 -m sslyze {ip_address} '
                                 f'--json_out={out_file}',
                                 shell=True)
    
    # parse the generated JSON file
    with open(f'{ip_address}.json') as f:
        json_output = f.read()
        
        out = json.loads(json_output)
        
        result = {
            "ip_address": out["server_scan_results"][0]["server_location"]["ip_address"],
            "port": out["server_scan_results"][0]["server_location"]["port"],
            "connection_type": out["server_scan_results"][0]["server_location"]["connection_type"],
            "scan_status": out["server_scan_results"][0]["scan_status"],
            "uuid": out["server_scan_results"][0]["uuid"],
            "date_scans_completed": out["date_scans_completed"],
            "date_scans_started": out["date_scans_started"],
            
        }
        
        res = json.dumps(result, indent=4, sort_keys=True)
        
        print(res)
        
        return 'done'


