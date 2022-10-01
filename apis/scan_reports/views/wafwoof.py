from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from apis.utils import responses, error_logs
from apis.scan_reports.tools.wafwoof import WafWoofScanner


class WafWoofScannerAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')
        try:
            # scan ip address and return response
            wafwoof = WafWoofScanner(ip_address)
            data = wafwoof.response()
            return responses.http_response_200('Scan successful', data)
        except Exception as e:
            error_logs.logger.error('WafWoofScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
