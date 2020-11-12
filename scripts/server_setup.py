"""Script to setup the server for tests"""

from argparse import ArgumentParser
import time
import sys
import paramiko

def main():
    """Main entry point of script."""
    argument_parser = ArgumentParser(
        prog='python server_setup.py branch_name',
        description="Checks out and builds the given branch's code"
	)
    argument_parser.add_argument('branch_name', help='branch to checkout and build')
    args = argument_parser.parse_args()

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='18.188.207.58', username='ec2-user', password='jerryseinfeld')

    chan = ssh_client.get_transport().open_session()
    chan.get_pty()
    chan.invoke_shell()
    chan.send('cd CI/ECE1140-Project; git fetch; git checkout ' + args.branch_name +
              '; git pull; mkdir build -p; cd build; cmake ..; make\n')
    time.sleep(25)


if __name__ == "__main__":
    sys.exit(main())
