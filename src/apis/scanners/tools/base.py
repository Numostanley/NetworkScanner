"""
An abstract class for all scanning tools
"""

import getpass
import os
import subprocess

from abc import ABC, abstractmethod

from celery import Task


def get_server_user():
    """
    get the current user account on the remote server
        ex: ubuntu@ip_address (where ubuntu is the server user)
    """
    return getpass.getuser()


class Scanner(Task, ABC):
    """
    cmd: to execute subprocess module commands
    server_os: to execute os module functions
    """
    cmd = subprocess
    server_os = os

    def __init__(self, ip_address: str, tool: str) -> None:
        """
        params:
            ip_address: ip address to scan
            tool: the tool to scan the ip address
        """
        pass

    @abstractmethod
    def change_directory(self):
        """change directory to the specified location"""
        pass

    @abstractmethod
    def mkdir_ip_scans_dir(self):
        """create ip_scans directory in the specified location"""
        pass

    @abstractmethod
    def scan(self):
        """run scan with specified tool"""
        pass

    @abstractmethod
    def response(self):
        """return the response"""
        pass
