"""helper functions for extra utilities"""

from base64 import b64encode
from pathlib import Path

from s3fs.core import S3FileSystem

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
    retrieve file (from: /root/VulnScanner-AppData/bigbrowser_report/{sanitize_host_zip})
    if exists else return None
    """
    sanitize_host_zip = f'{sanitize_host(host)}.zip'
    file_path = f'{env_vars.S3_DIR_PATH}/bigbrowser_report/{sanitize_host_zip}'
    if Path(file_path).exists():
        return file_path
    return None


def s3_filesystem_move(source: str, destination: str):
    """move file from source to destination"""
    S3FileSystem(env_vars.S3_BUCKET_NAME,
                 key=env_vars.S3_ACCESS_KEY,
                 secret=env_vars.S3_SECRET_KEY).mv(source, destination)


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
