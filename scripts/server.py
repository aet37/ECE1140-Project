import paramiko
import time


if __name__ == "__main__":
    ssh_client=paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='3.23.104.34',username='ec2-user',password='jerryseinfeld')
    stdin,stdout,stderr=ssh_client.exec_command('cd ECE1140-Project')
    time.sleep(1)
    print(stdout.readlines())
    stdin,stdout,stderr=ssh_client.exec_command('pwd')
    print(stdout.readlines())
    # stdin,stdout,stderr=ssh_client.exec_command('cmake ..')
    # print(stderr.readlines())
    # stdin,stdout,stderr=ssh_client.exec_command('make')
    # print(stdout.readlines())