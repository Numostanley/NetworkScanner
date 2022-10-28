from apis.utils import responses, error_logs

from apis.scanners.hosts.models import Host
from apis.utils.views import AuthProtectedAPIView
from .models import Zap
from .tasks import zap_task

class ZapScannerAPIView(AuthProtectedAPIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get host key from the url query parameters
        if 'host' not in query_params:
            return responses.http_response_400('Host key not found in query parameters!')
        
        # get api_key key from the url query parameters
        if 'api_key' not in query_params:
            return responses.http_response_400('API_key key not found in query parameters!')

        # get host value from the url query parameters
        host = query_params.get('host', '')
        
        # get api_key value from the url query parameters
        api_key = query_params.get('api_key', '')
        
        if not host:
            return responses.http_response_400('Host not specified!')
        
        if not api_key:
            return responses.http_response_400('API_key not specified!')

        try:
            # scan ip address as background task
            zap_task.delay(ip_address=host, api_key=api_key)
            return responses.http_response_200('Scan in progress...')
        except Exception as e:
            error_logs.logger.error('ZapAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
