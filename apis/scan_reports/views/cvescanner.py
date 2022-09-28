from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from apis.utils import responses, error_logs
from apis.scan_reports.tools.cvescanner import CVEScanner
from apis.scan_reports.utils.pdf.cvescanner import CVEScannerPDFGenerator


class CVEScannerAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')
        try:
            # scan ip address and return response
            cvescanner = CVEScanner(ip_address)
            data = cvescanner.response()
            return responses.http_response_200('Scan successful', data)
        except Exception as e:
            error_logs.logger.error('CVEScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')


class CVEDownloadScanReportAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')

        if not ip_address:
            return responses.http_response_400('IP address not specified!')

        data = []
        tool = 'cvescanner'
        template_file_name = 'cve_scan_report.html'
        static_file = 'cve_main.css'
        cve_pdf = CVEScannerPDFGenerator(data, ip_address, tool, template_file_name, static_file)

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
