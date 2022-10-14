from apis.scanners.hosts.models import Host
from apis.utils import responses


def validate_host_in_query_params(query_params):
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
    pass
