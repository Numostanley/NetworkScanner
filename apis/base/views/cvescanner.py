from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from apis.utils import responses, error_logs
from apis.scan_reports.tools.cvescanner import CVEScanner 


class CVEScannerAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        """script to execute NMAP command to scan an IP address."""

        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        
        if not ip_address:
            return Response("IP was not specified.",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # scan ip address and return response
            cvescanner = CVEScanner(ip_address)
            data = cvescanner.response()
            print(data)
            return responses.http_response_200('Scan successful', data)
        except Exception as e:
            error_logs.logger.error('CVEScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
