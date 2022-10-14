from apis.utils import responses, error_logs

from apis.scanners.hosts.models import Host
from apis.utils.views import AuthProtectedAPIView
from .models import SSLyze
from .tasks import sslyze_task


class SslyzeScannerAPIView(AuthProtectedAPIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get host key from the url query parameters
        if 'host' not in query_params:
            return responses.http_response_400('Host key not found in query parameters!')

        # get host value from the url query parameters
        host = query_params.get('host', '')
        if not host:
            return responses.http_response_400('Host not specified!')

        try:
            # scan ip address as background task
            sslyze_task.delay(host)
            return responses.http_response_200('Scan in progress...')
        except Exception as e:
            error_logs.logger.error('SslyzeAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')


class SSLyzeScanResultAPIView(AuthProtectedAPIView):
    
    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get host key from the url query parameters
        if 'host' not in query_params:
            return responses.http_response_400('Host key not found in query parameters!')

        # get host value from the url query parameters
        host_key = query_params.get('host', '')
        if not host_key:
            return responses.http_response_400('Host not specified!')

        host = Host.get_host(host_key)
        if not host:
            return responses.http_response_404('Host not found!')

        sslyze_data = SSLyze.get_sslyze_scan_by_host(host=host)
        
        if sslyze_data.count() < 1:
            return responses.http_response_404("No scan result exists for this IP address.")

        if sslyze_data.count() > 0:
            return responses.http_response_200('Data successfully retrieved',sslyze_data)

        return responses.http_response_500('An error occurred!')
