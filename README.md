# MB8611 CLI

[![QA](https://github.com/Tatsh/mb8611/actions/workflows/qa.yml/badge.svg)](https://github.com/Tatsh/mb8611/actions/workflows/qa.yml)
[![Tests](https://github.com/Tatsh/mb8611/actions/workflows/tests.yml/badge.svg)](https://github.com/Tatsh/mb8611/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/github/Tatsh/mb8611/badge.svg?branch=master)](https://coveralls.io/github/Tatsh/mb8611?branch=master)
[![Documentation Status](https://readthedocs.org/projects/mb8611/badge/?version=latest)](https://mb8611.readthedocs.io/en/latest/?badge=latest)
![PyPI - Version](https://img.shields.io/pypi/v/mb8611)
![GitHub tag (with filter)](https://img.shields.io/github/v/tag/Tatsh/mb8611)
![GitHub](https://img.shields.io/github/license/Tatsh/mb8611)
![GitHub commits since latest release (by SemVer including pre-releases)](https://img.shields.io/github/commits-since/Tatsh/mb8611/v0.0.1/master)

CLI tool and library for managing the Motorola MB8611 series modem and maybe other Motorola devices.

## Installation

### Poetry

```shell
poetry add mb8611
```

### Pip

```shell
pip install mb8611
```

## Command line usage

```plain
Usage: mb8611 [OPTIONS] {addr|address|clear-log|conn|connection|connection-
              info|conninfo|down|downstream|lag|lag-
              status|log|reboot|software|software-status|startup|startup-
              sequence|up|upstream}

  Main CLI.

Options:
  -H, --host TEXT      Host to connect to.
  -d, --debug          Enable debug level logging.
  -j, --json           Only output JSON. Encoded lists (tables) will still be
                       parsed.
  -p, --password TEXT  Administrator password.
  -u, --username TEXT  Administrator username.
  --help               Show this message and exit.
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
mb8611 --output-json conn | jq -r .MotoHomeOnline
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
mb8611 up -j | jq -r '.MotoConnUpstreamChannel[]|@csv' | tr -d '"' | tabulate -s ','
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

**Note:** The modem does not require any authentication for the currently working actions such as
`addr`.

The following actions do not work as they require proper authentication (these return `'UN-AUTH'`
at this time):

- `clear-log` / `SetStatusLogSettings`
- `SetStatusSecuritySettings`
- `SetMotoLagStatus`
- `SetMotoStatusDSTargetFreq`
