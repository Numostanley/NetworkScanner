from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from apis.utils import responses, error_logs
from .nmap_scan import scan_ip_address
from .utils import generate_scan_report_pdf, delete_scan_report


class ScanIPAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')
        if not ip_address:
            return responses.http_response_400('IP address not specified!')
        try:
            # scan ip address
            data = scan_ip_address(ip_address)
            return responses.http_response_200('Scan successful', data)
        except Exception as e:
            error_logs.logger.error('ScanIPAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')


class DownloadScanReportAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        query_params = request.query_params

        # get ip_address from the url query parameters
        ip_address = query_params.get('ip_address', '')

        if not ip_address:
            return responses.http_response_400('IP address not specified!')

        pdf_file = generate_scan_report_pdf(ip_address)

        try:
            # return generated scan report as response
            file_response = FileResponse(open(pdf_file, 'rb'),
                                         as_attachment=True,
                                         filename=pdf_file)
            return file_response
        except Exception as e:
            error_logs.logger.error('DownloadScanReportAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
        finally:
            # delete file
            delete_scan_report(pdf_file)
