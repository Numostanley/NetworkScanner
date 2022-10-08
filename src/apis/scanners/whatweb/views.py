from apis.utils import responses, error_logs

from apis.scanners.hosts.models import Host
from apis.utils.views import AuthProtectedAPIView
from .models import WhatWeb
from .tasks import whatweb_task


class WhatWebScannerAPIView(AuthProtectedAPIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')
        try:
            # scan ip address as background task
            whatweb_task.delay(ip_address)
            return responses.http_response_200('Scan in progress...')
        except Exception as e:
            error_logs.logger.error('WhatWebScannerAPIView.get@Error')
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

        whatweb_data = WhatWeb.get_whatweb_scan_by_ip_addr(host)

        if whatweb_data.count() < 1:
            return responses.http_response_404("No scan result exists for this IP address.")

        if whatweb_data.count() > 0:
            return responses.http_response_200('Data successfully retrieved', whatweb_data)

        return responses.http_response_500('An error occurred!')
