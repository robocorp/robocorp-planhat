# Robocorp-Planhat: A Planhat API SDK integrated with Robocorp's Python Automation Framework

[![PyPI - Version](https://img.shields.io/pypi/v/robocorp-planhat?label=robocorp&color=%23733CFF)](https://pypi.org/project/robocorp-planhat)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This automation library is designed for use with [Robocorp's Python Automation Framework](https://github.com/robocorp/robocorp). It includes data modeling for the base Planhat API object types and a customized client and associated session for use in authenticating, retrieving, and updating those objects.

For additional information regarding the Planhat API, please refer to the [Planhat API documentation](https://docs.planhat.com/).

## Installation

For most users, this project should be installed via your `conda.yaml` or `package.yaml` within a Robocorp automation task package or action server package under your pip dependancies. For example:

```yaml
conda:
  channels:
    - conda-forge
  dependencies:
    - python=3.9.16
    - pip=22.1.2
    - pip:
      - robocorp==1.6.2
      - robocorp-planhat==1.0.0
```

Alternatively, you can use your preferred installation method to install the package directly from PyPI.

## Getting started

To use the Planhat API, you will need to have a Planhat account and an API key. You can find your API key in the Planhat web application under `Settings > Service Accounts`. You will need to create a new service account and generate an API key.

Once you have your API key, you can use the Planhat API SDK to authenticate and retrieve data from Planhat. Here is an example of how to use the Planhat API SDK to retrieve a list of companies:

```python
from planhat import Planhat, types as ph_types

# Create a Planhat client
client = Planhat(api_key="your-api-key")

# Retrieve a list of Companies
companies = client.get_objects(ph_types.Company)

# Print the names of the companies
for company in companies:
    print(company.name)
```

## Using Control Room Vault

When used in conjunction with the Robocorp Python Automation Framework, you can use Robocorp's Control Room Vault to store your Planhat API key. This is a secure way to store your API key and access it from your Robocorp automation tasks. When creating the secret in the Control Room vault, it maust have the key `api_key`. Here is an example of how to use the Planhat API SDK with the Control Room Vault:

```python
from robocorp.tasks import task
from planhat import Planhat, types as ph_types

@task
def get_companies():
    # Create a Planhat client
    client = Planhat(vault_secret_name="your-vault-secret-name")

    # Retrieve a list of Companies
    companies = client.get_objects(ph_types.Company)

    # Print the names of the companies
    for company in companies:
        print(company.name)
```

Further documentation on how to use the Robocorp Python Automation Framework can be found on the [Robocorp Docs site](https://robocorp.com/docs).

## API Reference

Information on specific classes and methods can be found in the [API Reference](/docs/api/planhat.md).

## Changelog

See the [CHANGELOG](/docs/CHANGELOG.md) for a history of notable changes.