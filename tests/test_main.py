import json

from click.testing import CliRunner
from pytest_mock.plugin import MockerFixture

from mb8611.client import CallHNAPError, LoginFailed
from mb8611.main import main


def test_main_login_failed(mocker: MockerFixture, runner: CliRunner) -> None:
    client = mocker.patch('mb8611.main.Client')
    client.side_effect = LoginFailed()
    run = runner.invoke(main, ('up',))
    assert run.exit_code != 0


def test_main_hnap_error(mocker: MockerFixture, runner: CliRunner) -> None:
    client = mocker.patch('mb8611.main.Client')
    client.return_value.__enter__.return_value.call_hnap.side_effect = CallHNAPError(
        {'GetMultipleHNAPsResponse': {
            'GetMultipleHNAPsResult': 'UN-AUTH'
        }})
    run = runner.invoke(main, ('up',))
    assert run.exit_code != 0


def test_main(mocker: MockerFixture, runner: CliRunner) -> None:
    client = mocker.patch('mb8611.main.Client')
    client.return_value.__enter__.return_value.call_hnap.return_value = {
        'GetMotoStatusSoftwareResponse': {
            'StatusSoftwareSpecVer': 'DOCSIS 3.1',
            'StatusSoftwareHdVer': 'V1.0',
            'StatusSoftwareSfVer': '8611-19.2.18',
            'StatusSoftwareMac': '00:AA:BB:CC:DD:EE',
            'StatusSoftwareSerialNum': 'FFFF-MB8611-eE-FFF',
            'StatusSoftwareCertificate': 'Installed',
            'StatusSoftwareCustomerVer': 'Prod_19.2_d31',
            'GetMotoStatusSoftwareResult': 'OK'
        }
    }
    run = runner.invoke(main, ('software',))
    assert run.exit_code == 0
    assert run.stdout == '''StatusSoftwareCertificate: Installed
StatusSoftwareCustomerVer: Prod_19.2_d31
StatusSoftwareHdVer: V1.0
StatusSoftwareMac: 00:AA:BB:CC:DD:EE
StatusSoftwareSerialNum: FFFF-MB8611-eE-FFF
StatusSoftwareSfVer: 8611-19.2.18
StatusSoftwareSpecVer: DOCSIS 3.1
'''


def test_main_table_keys(mocker: MockerFixture, runner: CliRunner) -> None:
    client = mocker.patch('mb8611.main.Client')
    client.return_value.__enter__.return_value.call_hnap.return_value = {
        "GetMotoStatusUpstreamChannelInfoResponse": {
            "MotoConnUpstreamChannel":
                "1^Locked^SC-QAM^1^5120^17.6^40.3^|+|1^Locked^SC-QAM^1^5120^17.6^40.3^",
            "GetMotoStatusUpstreamChannelInfoResult":
                "OK"
        }
    }
    run = runner.invoke(main, ('up',))
    assert run.exit_code == 0
    assert run.stdout == ("[['1', 'Locked', 'SC-QAM', '1', '5120', '17.6', '40.3', ''], "
                          "['1', 'Locked', 'SC-QAM', '1', '5120', '17.6', '40.3', '']]\n")


def test_main_table_keys_json(mocker: MockerFixture, runner: CliRunner) -> None:
    client = mocker.patch('mb8611.main.Client')
    client.return_value.__enter__.return_value.call_hnap.return_value = {
        "GetMotoStatusUpstreamChannelInfoResponse": {
            "MotoConnUpstreamChannel":
                "1^Locked^SC-QAM^1^5120^17.6^40.3^|+|1^Locked^SC-QAM^1^5120^17.6^40.3^",
            "GetMotoStatusUpstreamChannelInfoResult":
                "OK"
        }
    }
    run = runner.invoke(main, ('up', '--json'))
    assert run.exit_code == 0
    response_json = json.dumps(
        {
            'MotoConnUpstreamChannel': [['1', 'Locked', 'SC-QAM', '1', '5120', '17.6', '40.3', ''],
                                        ['1', 'Locked', 'SC-QAM', '1', '5120', '17.6', '40.3', '']],
            'GetMotoStatusUpstreamChannelInfoResult': 'OK'
        },
        indent=2)
    assert run.stdout == f'{response_json}\n'


def test_main_json(mocker: MockerFixture, runner: CliRunner) -> None:
    client = mocker.patch('mb8611.main.Client')
    response = {
        'GetMotoStatusSoftwareResponse': {
            'StatusSoftwareSpecVer': 'DOCSIS 3.1',
            'StatusSoftwareHdVer': 'V1.0',
            'StatusSoftwareSfVer': '8611-19.2.18',
            'StatusSoftwareMac': '00:AA:BB:CC:DD:EE',
            'StatusSoftwareSerialNum': 'FFFF-MB8611-eE-FFF',
            'StatusSoftwareCertificate': 'Installed',
            'StatusSoftwareCustomerVer': 'Prod_19.2_d31',
            'GetMotoStatusSoftwareResult': 'OK'
        }
    }
    response_json = json.dumps(response['GetMotoStatusSoftwareResponse'], indent=2)
    client.return_value.__enter__.return_value.call_hnap.return_value = response
    run = runner.invoke(main, ('software', '--json'))
    assert run.exit_code == 0
    assert run.stdout == f'{response_json}\n'
