from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from apis.utils import responses, error_logs
from apis.scan_reports.tools.cvescanner import CVEScanner 


class GetRoutes(APIView):

    def get(self, request, *args, **kwargs):
        Routes = {
            "Get_Routes": "/api/v1",
            "Scan_IP": "/api/v1/scan"
        }

        return Response(Routes)


class CVEScannerAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response("Enter IP to be scaned.")

    def post(self, request, *args, **kwargs):
        """script to execute NMAP command to scan an IP address."""

        ip_address = request.data['IP']

        if not ip_address:
            return Response("IP was not specified.",
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # scan ip address and return response
            cvescanner = CVEScanner(ip_address)
            data = cvescanner.response()
            # print(data)
            return responses.http_response_200('Scan successful', data)
        except Exception as e:
            error_logs.logger.error('CVEScannerAPIView.get@Error')
            error_logs.logger.error(e)
            return responses.http_response_500('An error occurred!')
