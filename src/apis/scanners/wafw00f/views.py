from apis.utils import responses, error_logs

from apis.scanners.hosts.models import Host
from apis.utils.views import AuthProtectedAPIView
from .models import WafWoof
from .tasks import wafwoof_task


class WafWoofScannerAPIView(AuthProtectedAPIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        if 'ip_address' not in query_params:
            return responses.http_response_400('IP address key not found in Query Parameters!')

        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')
        try:
            # scan ip address as background task
            wafwoof_task.delay(ip_address)
            return responses.http_response_200('Scan in progress...')
        except Exception as e:
            error_logs.logger.error('WafWoofScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')


class WafW00fScanResultAPIView(AuthProtectedAPIView):

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        if 'ip_address' not in query_params:
            return responses.http_response_400('IP address key not found in Query Parameters!')

        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')

        host = Host.get_host(ip_address=ip_address)
        if not host:
            return responses.http_response_404('Host not found!')

        wafwoof_data = WafWoof.get_wafw00f_scan_by_ip_address(host)

        if wafwoof_data.count() < 1:
            return responses.http_response_404("No scan result exists for this IP address.")

        if wafwoof_data.count() > 0:
            return responses.http_response_200('Data successfully retrieved', wafwoof_data)

        return responses.http_response_500('An error occurred!')
