from apis.utils import responses, error_logs

from apis.scanners.hosts.models import Host
from apis.utils.views import AuthProtectedAPIView
from .models import DirBy
from .tasks import dirby_task


class DirByScannerAPIView(AuthProtectedAPIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')
        try:
            # scan ip address as background task
            dirby_task.delay(ip_address)
            return responses.http_response_200('Scan in progress')
        except Exception as e:
            error_logs.logger.error('DirByScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')


class DirByScanResultAPIView(AuthProtectedAPIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')

        host = Host.get_host(ip_address=ip_address)
        if not host:
            return responses.http_response_404('Host not found!')

        dirby_data = DirBy.get_dirby_scan_by_ip_address(host)

        if dirby_data.count() < 1:
            return responses.http_response_404("No scan result exists for this IP address.")

        if dirby_data.count() > 0:
            return responses.http_response_200('Data successfully retrieved', dirby_data)

        return responses.http_response_500('An error occurred!')
