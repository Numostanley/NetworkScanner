from django.http import FileResponse

from apis.utils import responses, error_logs
from apis.scanners.hosts.models import Host
from apis.scanners.utils.extras import retrieve_screenshot_scanned_file
from apis.utils.views import AuthProtectedAPIView
from .tasks import screenshot_task


class ScreenShotScannerAPIView(AuthProtectedAPIView):

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
            screenshot_task.delay(host)
            return responses.http_response_200('Scan in progress')
        except Exception as e:
            error_logs.logger.error('ScreenShotScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')


class ScreenShotScanResultAPIView(AuthProtectedAPIView):

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
            # retrieve the zipped screenshot scanned file for host
            try:
                file = retrieve_screenshot_scanned_file(host.ip_address)
                # if file is found return a FileResponse
                return FileResponse(open(file, 'rb'), as_attachment=True, filename=file)
            except FileNotFoundError:
                return responses.http_response_404('Not scanned result found!')
        except Exception as e:
            error_logs.logger.error('ScreenShotScanResultAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
