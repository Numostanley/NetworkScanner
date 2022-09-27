from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .utils import scan_IP


class GetRoutes(APIView):

    def get(self, request, *args, **kwargs):
        Routes = {
            "Get_Routes": "/api/v1",
            "Scan_IP": "/api/v1/scan"
        }

        return Response(Routes)


class VulnerabilityScanner(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response("Enter IP to be scaned.")

    def post(self, request, *args, **kwargs):
        """script to execute NMAP command to scan an IP address."""

        ip_address = request.data['IP']

        if not ip_address:
            return Response("IP was not specified.",
                            status=status.HTTP_400_BAD_REQUEST)

        # scan IP and convert to the output to JSON
        result = scan_IP(ip_address)
        return Response(result, status=status.HTTP_200_OK)
