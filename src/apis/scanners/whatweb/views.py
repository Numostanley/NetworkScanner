from apis.utils import responses, error_logs

from apis.scanners.hosts.models import Host
from apis.utils.views import AuthProtectedAPIView
from .models import WhatWeb
from .tasks import whatweb_task


class WhatWebScannerAPIView(AuthProtectedAPIView):

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
            whatweb_task.delay(host)
            return responses.http_response_200('Scan in progress...')
        except Exception as e:
            error_logs.logger.error('WhatWebScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')


class WhatWebScanResultAPIView(AuthProtectedAPIView):

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

        try:
            whatweb_data = WhatWeb.get_whatweb_scan_by_host(host)

            if whatweb_data:
                return responses.http_response_200('Data successfully retrieved!', whatweb_data)

            return responses.http_response_404("No scan result exists for this host!")
        except Exception as e:
            error_logs.logger.error('WhatWebScanResultAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
