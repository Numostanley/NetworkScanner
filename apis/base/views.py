import subprocess
import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from apis.utils.error_logs import logger
from .utils import convert_to_json


# Create your views here.

class GetRoutes(APIView):
    
    def get(self, request, *args, **kwargs):
        
        Routes = {
            
            "Get_Routes": "/api/v1",
            "Scan_IP": "/api/v1/scan"
            
            }
        
        return Response(Routes)



class VulnerabilityScanner(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        
        return Response("Enter IP to be scaned.")
    

    def post(self, request, *args, **kwargs):
        """script to execute NMAP command to scan an IP address."""
        
        ip_address = request.data['IP']
        
        if not ip_address:
            return Response("IP was not specified.", 
                            status=status.HTTP_400_BAD_REQUEST)
        
        out_file = f"{ip_address}.xml"

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
        
        xml_content = subprocess.run(f'sudo nmap -oX ip_scans/{out_file} '
                                 f'-sV --script ./cvescannerv2.nse {ip_address}',
                                 shell=True)
        
        #convert xml_output to Json
        result = convert_to_json(out_file)
        
        print(result)

        return Response(result, status=status.HTTP_200_OK)
