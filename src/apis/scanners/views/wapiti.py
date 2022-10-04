from apis.utils import responses, error_logs
from apis.scanners.tasks import wapiti_task

from .base import AuthProtectedAPIView


class WapitiScannerAPIView(AuthProtectedAPIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')
        try:
            # scan ip address as background task
            wapiti_task.delay(ip_address)
            return responses.http_response_200('Scan in progress...')
        except Exception as e:
            error_logs.logger.error('WapitiScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
