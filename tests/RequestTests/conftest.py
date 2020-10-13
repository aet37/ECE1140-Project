"""Test fixtures for request tests"""

import time
import pytest
import paramiko

@pytest.fixture(scope='session')
def start_server():
    """Starts the server."""
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='3.23.104.34', username='ec2-user', password='jerryseinfeld')

    chan = ssh_client.get_transport().open_session()
    chan.get_pty()
    chan.invoke_shell()
    chan.send('cd Luke/ECE1140-Project/build/src; ./main &\n')
    time.sleep(2)
    print(chan.recv(1024))

    yield

    chan.send('kill $(ps | grep main | cut -d " " -f1)')
    chan.close()
