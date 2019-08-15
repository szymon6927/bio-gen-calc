#!/usr/bin/env python

import socket
import sys
from datetime import datetime
from os import environ

import paramiko


class SSHCredentials:
    SSH_HOSTNAME = environ.get('SSH_HOSTNAME', None)
    SSH_PORT = environ.get('SSH_PORT', None)
    SSH_USERNAME = environ.get('SSH_USERNAME', None)
    SSH_PASSWORD = environ.get('SSH_PASSWORD', None)


class Command:
    ROOT_PATH = "~/domains/gene-calc.pl/"
    APP_PATH = "~/domains/gene-calc.pl/public_python/"
    VIRTUAL_ENV_PATH = "~/login/.virtualenvs/gene-calc/bin/activate"

    @property
    def git_clone(self):
        return f"git -C {self.ROOT_PATH} clone -b trello-15-circleci https://github.com/szymon6927/bio-gen-calc.git"

    @property
    def copy_passenger_wsgi(self):
        return f"cp {self.APP_PATH}passenger_wsgi.py {self.ROOT_PATH}bio-gen-calc"

    @property
    def remove_current_files(self):
        return f"rm -rf {self.APP_PATH}*"

    @property
    def copy_files(self):
        return f"cp -r {self.ROOT_PATH}bio-gen-calc/* {self.APP_PATH}"

    @property
    def install_requirements(self):
        return (
            f"source {self.VIRTUAL_ENV_PATH} && "
            f"pip install -r {self.APP_PATH}requirements/requirements.txt && deactivate"
        )

    @property
    def remove_github_dir(self):
        return f"rm -rf {self.ROOT_PATH}bio-gen-calc/"

    @property
    def remove_python_cache(self):
        return r'find ~/domains/gene-calc.pl/public_python/ -name "*.pyc" -exec rm -f {} \;'

    @property
    def upgrade_db(self):
        return f"source {self.VIRTUAL_ENV_PATH} && flask db upgrade && deactivate"

    @property
    def restart_service(self):
        return "devil www restart gene-calc.pl"

    def make_backup(self):
        deploy_time = datetime.now().strftime("%H_%M___%d_%m_%Y")
        backup_package = f"backup_{deploy_time}"

        return backup_package, f"cp -r {self.ROOT_PATH}public_python/ {self.ROOT_PATH}{backup_package}/"

    def revert_deploy(self, deploy_package):
        return f"rm -rf {self.APP_PATH} && mv {self.ROOT_PATH}{deploy_package}/ public_python"


class Deployer:
    def __init__(self):
        self.client = None
        self.command = Command()

    def _connect(self):
        """Login to the remote server"""

        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            self.client.connect(
                hostname=SSHCredentials.SSH_HOSTNAME,
                port=SSHCredentials.SSH_PORT,
                username=SSHCredentials.SSH_USERNAME,
                password=SSHCredentials.SSH_PASSWORD,
            )
        except paramiko.AuthenticationException:
            print("Authentication failed, please verify your credentials")
            result_flag = False
        except paramiko.SSHException as ssh_exception:
            print(f"Could not establish SSH connection: {ssh_exception}")
            result_flag = False
        except socket.timeout as e:
            print(f"Connection timed out, message: {str(e)}")
            result_flag = False
        except Exception as e:
            print(f"Exception in connecting to the server, message: {str(e)}")
            result_flag = False
            self.client.close()
        else:
            result_flag = True

        return result_flag

    def _execute_command(self, command):
        """Execute a command on the remote server"""
        result_flag = True

        try:
            connection = self._connect()

            if connection:
                print(f"Executing command: {command}")

                stdin, stdout, stderr = self.client.exec_command(command, timeout=3600)
                ssh_output = stdout.read().decode()
                ssh_error = stderr.read().decode()

                status = stdout.channel.recv_exit_status()
                print(f"Status: {status}")

                if status != 0:
                    print(f"Problem occurred while running command: {command}")
                    print(f"The error is {ssh_error}")
                    result_flag = False
                else:
                    print(f"{command} -> command execution completed successfully")
                    print(f"Output is: ssh_output - {ssh_output}, ssh_error - {ssh_error}")

                self.client.close()
            else:
                print("Could not establish SSH connection")
                self.client.close()
                result_flag = False
        except socket.timeout:
            print(f"Command: {command} - timed out.")
            self.client.close()
            result_flag = False
        except paramiko.SSHException:
            print(f"Failed to execute the command: {command}")
            self.client.close()
            result_flag = False

        return result_flag

    def make_backup(self):
        backup_name, command = self.command.make_backup()

        executed = self._execute_command(command)

        if not executed:
            sys.exit("Error! Can not create a backup !!!")

        return backup_name

    def revert_deploy(self, backup_name):
        command = self.command.revert_deploy(backup_name)

        executed = self._execute_command(command)

        if not executed:
            sys.exit("Error! Can not revert a deploy !!!")

        self._execute_command(self.command.restart_service)

    def deploy(self):
        """Make an deployment"""
        backup_name = self.make_backup()

        workflow = {
            1: self.command.git_clone,
            2: self.command.copy_passenger_wsgi,
            3: self.command.remove_current_files,
            4: self.command.copy_files,
            5: self.command.install_requirements,
            6: self.command.remove_github_dir,
            7: self.command.remove_python_cache,
            8: self.command.upgrade_db,
            9: self.command.restart_service,
        }

        for step, command in workflow.items():
            print(f"Running step: {step}")

            executed = self._execute_command(command)
            if not executed:
                print(f"Something went from on step: {step} with command: {command}")
                print("Reverting deploy!")
                self.revert_deploy(backup_name)
                break


if __name__ == '__main__':
    print("**********************************")
    print("**********************************")
    print("**********************************")
    deployer = Deployer()
    deployer.deploy()
    print("**********************************")
    print("**********************************")
    print("**********************************")
