from unittest.mock import patch

import pytest

from deploy import Command
from deploy import Deployer


def test_command_make_backup():
    command = Command()

    backup_package, make_backup_command = command.make_backup()

    assert backup_package.startswith("backup_") is True
    assert backup_package in make_backup_command
    assert "cp -r" in make_backup_command
    assert "public_python" in make_backup_command


def test_command_revert_deploy():
    command = Command()

    backup_package, make_backup_command = command.make_backup()
    revert_command = command.revert_deploy(backup_package)

    assert backup_package in revert_command
    assert "cp -r" in revert_command


def test_deployer_connect():
    deployer = Deployer()

    result = deployer._connect()

    assert result is False


@patch('deploy.Deployer._execute_command')
@patch('deploy.Deployer._connect')
def test_deployer_make_backup(mock_connect, mock_exec_command):
    mock_connect.return_value = True
    mock_exec_command.return_value = True

    deployer = Deployer()
    result = deployer.make_backup()

    assert "backup_" in result


@patch('deploy.Deployer._execute_command')
@patch('deploy.Deployer._connect')
def test_deployer_make_backup_when_command_execution_failed(mock_connect, mock_exec_command):
    mock_connect.return_value = True
    mock_exec_command.return_value = False

    deployer = Deployer()

    with pytest.raises(SystemExit, match=r".* Can not create a backup .*"):
        deployer.make_backup()


@patch('deploy.Deployer._execute_command')
@patch('deploy.Deployer._connect')
def test_deployer_revert_deploy(mock_connect, mock_exec_command):
    mock_connect.return_value = True
    mock_exec_command.return_value = True

    deployer = Deployer()
    backup_name = deployer.make_backup()
    result = deployer.revert_deploy(backup_name)

    assert result is True


@patch('deploy.Deployer._execute_command')
@patch('deploy.Deployer._connect')
def test_deployer_revert_deploy_when_command_execution_failed(mock_connect, mock_exec_command):
    mock_connect.return_value = True
    mock_exec_command.return_value = False

    deployer = Deployer()

    with pytest.raises(SystemExit, match=r".* Can not revert a deploy .*"):
        deployer.revert_deploy("test_backup_name")


@patch('deploy.Deployer._execute_command')
@patch('deploy.Deployer._connect')
def test_deployer_deploy(mock_connect, mock_exec_command):
    mock_connect.return_value = True
    mock_exec_command.return_value = True

    deployer = Deployer()
    result = deployer.deploy()

    assert result is True


@patch('deploy.Deployer.revert_deploy')
@patch('deploy.Deployer.make_backup')
@patch('deploy.Deployer._execute_command')
@patch('deploy.Deployer._connect')
def test_deployer_deploy_when_command_execution_failed(
    mock_connect, mock_exec_command, mock_make_backup, mock_revert_deploy
):
    mock_connect.return_value = True
    mock_exec_command.return_value = False
    mock_make_backup.return_value = "test_backup_name"
    mock_revert_deploy.return_value = True

    deployer = Deployer()
    result = deployer.deploy()

    assert result is False
