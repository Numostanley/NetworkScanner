from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from apis.utils import responses, error_logs
from apis.scan_reports.tools.wapiti import WapitiScanner


class WapitiAPIView(APIView):
    
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response("Enter IP to be scaned.")
    
    
    def post(self, request, *args, **kwargs):
        """script to execute wapiti command to scan an IP address."""
        
        ip_address = request.data['IP']

        if not ip_address:
            return Response("IP was not specified.",
                            status=status.HTTP_400_BAD_REQUEST)
            
        try:
            # scan ip address and return response
            wapiti_scan = WapitiScanner(ip_address)
            data = wapiti_scan.response()
            print(data)
            return responses.http_response_200('Scan successful', data)
        except Exception as e:
            error_logs.logger.error('WapitiAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
        
        