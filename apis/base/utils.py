# import json
# import subprocess
# import os



# def wapiti_scan(ip_address: str):
#     """Script to scan IP with wapiti scanner."""
    
#     out_file = f'{ip_address}.json'
    
#     # change directory to ~/ (/home/{$username})
#     os.chdir("../")

#     # navigate to the sslyze_json output directory
#     os.chdir("tools/wapiti_output")
    
#     # create json file for the ip to be scanned
#     try:
#         subprocess.run(f'type > {out_file}', 
#                        capture_output=True,
#                            shell=True,
#                            check=True)
#     except subprocess.CalledProcessError:
#         # if `type > {out_file}` command raises an error, skip because
#         # out_file has already been created
#         pass
    
#     scan_output = subprocess.run(f"wapiti -u http://{ip_address}/"
#                                  f" -f json -o /mnt/c/Users/'STANLEY NUMONDE/Documents'/Work/CyberMeStudio/tools/wapiti_output/{out_file}",
#                                  shell=True)
    
#     # parse the generated JSON file
#     with open(out_file, 'r') as f:
#         json_output = f.read()
        
#         out = json.loads(json_output)
        
#         result = [
#             out['vulnerabilities'],
#             out['anomalies'],
#             out['infos'],
#         ]
        
#         res = json.dumps(result, indent=4, sort_keys=True)
        
#         print(res)
        
#         return 'done'


