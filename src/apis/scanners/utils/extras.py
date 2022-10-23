"""helper functions for extra utilities"""

from base64 import b64encode

from s3fs.core import S3FileSystem


def convert_file_to_base64(file: str):
    """convert file to base64 bytes"""
    with open(file, mode="rb") as f:
        bytes_file = f.read()
        encode_string = b64encode(bytes_file)

    # with open(output_file, 'wb') as result:
    #     result.write(encode_string)
    return encode_string


def s3_filesystem_move(source: str, destination: str):
    """move file from source to destination"""
    S3FileSystem().mv(source, destination)
