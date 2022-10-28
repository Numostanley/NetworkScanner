from apis.scanners.hosts.models import Host
from apis.utils import responses, error_logs
from apis.utils.views import AuthProtectedAPIView
from .models import CVEScannerV2
from .tasks import cvescanner_task, send_pdf_report


class CVEScannerAPIView(AuthProtectedAPIView):

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
            cvescanner_task.delay(host)
            return responses.http_response_200('Scan in progress...')
        except Exception as e:
            error_logs.logger.error('CVEScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')


class CVEDownloadScanReportAPIView(AuthProtectedAPIView):

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

        data = []
        if not data:
            return responses.http_response_404("No scan result for this host.")

        try:
            # send generated PDF report to user's email in the background
            send_pdf_report.delay(data, host)
            return responses.http_response_200('Report has been sent to you email!')
        except Exception as e:
            error_logs.logger.error('CVEDownloadScanReportAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')


class CVEScanResultAPIView(AuthProtectedAPIView):

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
            cve_data = CVEScannerV2.get_cvescannerv2_by_host(host)

            if cve_data:
                return responses.http_response_200('Data successfully retrieved!', cve_data)

            return responses.http_response_404("No scan result for this host!")
        except Exception as e:
            error_logs.logger.error('CVEScanResultAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
