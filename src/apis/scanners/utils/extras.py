"""helper functions for extra utilities"""

from base64 import b64encode
from pathlib import Path

from core.extras import env_vars


def convert_file_to_base64(file: str):
    """convert file to base64 bytes"""
    with open(file, mode="rb") as f:
        bytes_file = f.read()
        encode_string = b64encode(bytes_file)

    # with open(output_file, 'wb') as result:
    #     result.write(encode_string)
    return encode_string


def retrieve_screenshot_scanned_file(host: str):
    """
    retrieve file (from: /{env_vars.S3_DIR_PATH}/{sanitize_host_zip})
    if exists else return None
    """
    sanitize_host_zip = f'{sanitize_host(host)}.zip'
    file_path = f'{env_vars.S3_DIR_PATH}/{sanitize_host_zip}'
    if Path(file_path).exists():
        return file_path
    return None


def sanitize_host(host: str):
    """remove ., :, /, // if exist in host"""
    if '.' in host:
        host = ''.join(host.split('.'))
    if ':' in host:
        host = ''.join(host.split(':'))
    if '/' in host:
        host = ''.join(host.split('/'))
    if '//' in host:
        host = ''.join(host.split('//'))
    return host
