from apis.utils import responses, error_logs

from apis.utils.views import AuthProtectedAPIView
from .tasks import sslyze_task
from apis.scanners.hosts.models import Host
from .models import SSLyze


class SslyzeScannerAPIView(AuthProtectedAPIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')
        try:
            # scan ip address as background task
            sslyze_task.delay(ip_address)
            return responses.http_response_200('Scan in progress...')
        except Exception as e:
            error_logs.logger.error('SslyzeAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')


class SSLyzeScanResultAPIView(AuthProtectedAPIView):
    
    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')
        
        host = Host.get_host(ip_address=ip_address)
        if not host:
            return responses.http_response_404('Host not found!')

        sslyze_data = SSLyze.get_sslyze_scan_by_ip_address(host=host)
        
        if sslyze_data.count() < 1:
            return responses.http_response_404("No scan result exists for this IP address.")

        if sslyze_data.count() > 0:
            return responses.http_response_200('Data successfully retrieved',sslyze_data)

        return responses.http_response_500('An error occurred!')
