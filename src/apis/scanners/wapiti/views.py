from apis.utils import responses, error_logs

from apis.utils.views import AuthProtectedAPIView
from .tasks import wapiti_task
from apis.scanners.hosts.models import Host
from .models import Wapiti
from django.core.exceptions import ObjectDoesNotExist

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


class WapitiScanResultAPIView(AuthProtectedAPIView):
    
    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        
        if not ip_address:
            return responses.http_response_400('IP address not specified!')

        host = Host.get_host(ip_address=ip_address)
        wapiti_data = Wapiti.get_wapiti_scan_by_ip_address(host=host)
        
        if wapiti_data.count() < 1:
            return responses.http_response_404("No scan result exists for this IP address.")
        
        return responses.http_response_200('data successfully retrieved',wapiti_data)
        
        