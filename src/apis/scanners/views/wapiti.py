from apis.utils import responses, error_logs
from apis.scanners.tools.wapiti import WapitiScanner

from .base import AuthProtectedAPIView


class WapitiScannerAPIView(AuthProtectedAPIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')
        try:
            # scan ip address and return response
            wapiti = WapitiScanner(ip_address)
            data = wapiti.response()
            return responses.http_response_200('Scan successful', data)
        except Exception as e:
            error_logs.logger.error('WapitiScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
