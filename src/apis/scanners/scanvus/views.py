from apis.utils import responses, error_logs

from apis.scanners.hosts.models import Host
from apis.utils.views import AuthProtectedAPIView
from .models import Scanvus
from .tasks import scanvus_task

# Create your views here.

class ScanvusScannerAPIView(AuthProtectedAPIView):
    
    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get host key from the url query parameters
        if 'host' not in query_params:
            return responses.http_response_400('Host key not found in query parameters!')
        
        # get username key from the url query parameters
        if 'username' not in query_params:
            return responses.http_response_400('Username key not found in query parameters!')
        
        # get password key from the url query parameters
        if 'password' not in query_params:
            return responses.http_response_400('Password key not found in query parameters!')

        # get host, username and password values from the url query parameters
        host = query_params.get('host', '')
        username = query_params.get('username', '')
        password = query_params.get('password', '')
        
        if not host:
            return responses.http_response_400('Host not specified!')
        
        if not username:
            return responses.http_response_400('Username not specified!')
        
        if not password:
            return responses.http_response_400('Password not specified!')

        try:
            # scan ip address with credentials as background task
            scanvus_task.delay(host, username, password)
            return responses.http_response_200('Scan in progress')
        except Exception as e:
            error_logs.logger.error('ScanvusScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')


class ScanvusScanResultAPIView(AuthProtectedAPIView):
    
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

        scanvus_data = Scanvus.get_scanvus_scan_by_host(host)
        
        if scanvus_data.count() < 1:
            return responses.http_response_404("No scan result exists for this host.")

        if scanvus_data.count() > 0:
            return responses.http_response_200('Data successfully retrieved', scanvus_data)

        return responses.http_response_500('An error occurred!')
    
    