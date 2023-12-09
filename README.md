# MB8611 CLI

[![QA](https://github.com/Tatsh/mb8611-cli/actions/workflows/qa.yml/badge.svg)](https://github.com/Tatsh/mb8611-cli/actions/workflows/qa.yml)
[![Tests](https://github.com/Tatsh/mb8611-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/Tatsh/mb8611-cli/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/Tatsh/mb8611-cli/badge.svg?branch=master)](https://coveralls.io/github/Tatsh/mb8611-cli?branch=master)
[![Documentation Status](https://readthedocs.org/projects/mb8611-cli/badge/?version=latest)](https://mb8611-cli.readthedocs.io/en/latest/?badge=latest)
![PyPI - Version](https://img.shields.io/pypi/v/mb8611-cli)
![GitHub tag (with filter)](https://img.shields.io/github/v/tag/Tatsh/mb8611-cli)
![GitHub](https://img.shields.io/github/license/Tatsh/mb8611-cli)
![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/Tatsh/mb8611-cli/v0.0.1/master)

CLI tool for managing the Motorola MB8611 series modem and maybe other Motorola devices.

## Installation

### Poetry

```shell
poetry add mb8611-cli
```

### Pip

```shell
pip install mb8611-cli
```

## Command line usage

```plain
Usage: mb8611 [--host HOST] --password PASSWORD [--username USERNAME] [--debug] ACTION

Options:
  -H, --host TEXT      Defaults to '192.168.100.1'.
  -d, --debug          Enable debug level logging
  -u, --username TEXT  Defaults to 'admin'.
  -p, --password TEXT  [required]
  --help               Show this message and exit
```

## Library usage

Refer to `mb8611.api` files for fields. Almost every field type is a string.

### Actions

- `GetHomeAddress`
- `GetHomeConnection`
- `GetMotoLagStatus`
- `GetMotoStatusConnectionInfo`
- `GetMotoStatusDownstreamChannelInfo`
- `GetMotoStatusLog`
- `GetMotoStatusLogXXX`
- `GetMotoStatusSecAccount`
- `GetMotoStatusSecXXX`
- `GetMotoStatusSoftware`
- `GetMotoStatusStartupSequence`
- `GetMotoStatusUpstreamChannelInfo`
- `GetNetworkModeSettings`

Some actions require a specific payload:

- `Login` — [`LoginPayload`](mb8611/api/login.py)
- `SetMotoLagStatus` — [`SetMotoLagStatusPayload`](mb8611/api/settings.py)
- `SetMotoStatusDSTargetFreq` — see [`SetMotoStatusDSTargetFreqPayload`](mb8611/api/settings.py)
- `SetStatusLogSettings` — see [`ClearLogPayload`](mb8611/api/settings.py)
- `SetStatusSecuritySettings` — see [`RebootPayload`](mb8611/api/settings.py)

### Example

```python
import pprint

from mb8611.client import Client

with Client(the_password) as client:
    addr = client.call_hnap('GetHomeAddress')
    # Fully typed dictionary
    assert addr['GetHomeAddressResponse']['GetHomeAddressResult'] == 'OK'
    pprint.pprint(addr)
```

`Client` implements a context manager. Calling `Client.login` unnecessary when using it with the
`with` statement.

```python
{'GetHomeAddressResponse': {'GetHomeAddressResult': 'OK',
                            'MotoHomeIpAddress': '...',
                            'MotoHomeIpv6Address': '',
                            'MotoHomeMacAddress': '...',
                            'MotoHomeSfVer': '8611-19.2.18'}}
```

## Examples

### Check if the modem is online

```shell
mb8611 --output-json --password ... conn | jq -r .MotoHomeOnline
```

```plain
Connected
```

### Display the modem's Upstream Bonded Channels

The output is a list of lists. Columns are:

- Channel
- Lock Status
- Channel Type
- Channel ID
- Symb. Rate (Ksym/sec)
- Freq. (MHz)
- Pwr (dBmV)

```shell
mb8611 -p ... up -j | jq -r '.MotoConnUpstreamChannel[]|@csv' | tr -d '"' | tabulate -s ','
```

```plain
-  ------  ------  -  ----  ----  --
1  Locked  SC-QAM  1  5120  17.6  43
2  Locked  SC-QAM  2  5120  24    47
3  Locked  SC-QAM  3  5120  30.4  43
4  Locked  SC-QAM  4  5120  36.8  44
-  ------  ------  -  ----  ----  --
```

## Known issues

Some actions currently return `'UN-AUTH'`. I have not figured out the issue. They always
work in the browser.

- `clear-log` / `SetStatusLogSettings`
- `SetStatusSecuritySettings`
- `SetMotoLagStatus`
- `SetMotoStatusDSTargetFreq`

Some actions only work when wrapped through the `GetMultipleHNAPs` API, such as `GetHomeAddress`.
This may be related to the same issue above.
