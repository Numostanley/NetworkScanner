from django.http import FileResponse

from apis.scanners.hosts.models import Host
from apis.scanners.utils.pdf.cvescanner import CVEScannerPDFGenerator
from apis.utils import responses, error_logs
from apis.utils.views import AuthProtectedAPIView
from .models import CVEScannerV2
from .tasks import cvescanner_task


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
        tool = 'cvescanner'
        template_file_name = 'cve_scan_report.html'
        static_file = 'cve_main.css'
        cve_pdf = CVEScannerPDFGenerator(data, host, tool, template_file_name, static_file)

        # generate pdf and return file path
        pdf = cve_pdf.generate_pdf()

        try:
            # return generated scan report as response
            file_response = FileResponse(open(pdf, 'rb'),
                                         as_attachment=True,
                                         filename=pdf)
            return file_response
        except Exception as e:
            error_logs.logger.error('CVEDownloadScanReportAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
        finally:
            # delete file
            cve_pdf.delete_pdf()


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

        cve_data = CVEScannerV2.get_cvescannerv2_by_host(host=host)

        if cve_data.count() < 1:
            return responses.http_response_404("No scan result exists for this IP address.")

        if cve_data.count() > 0:
            return responses.http_response_200('Data successfully retrieved', cve_data)

        return responses.http_response_500('An error occurred!')
