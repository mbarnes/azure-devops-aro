[![Python package](https://github.com/microsoft/azure-devops-python-api/workflows/Python%20package/badge.svg)](https://github.com/microsoft/azure-devops-python-api/actions)
[![Build Status](https://dev.azure.com/mseng/vsts-cli/_apis/build/status/vsts-python-api?branchName=dev)](https://dev.azure.com/mseng/vsts-cli/_build/latest?definitionId=5904&branchName=dev)
[![Python](https://img.shields.io/pypi/pyversions/azure-devops.svg)](https://pypi.python.org/pypi/azure-devops)

# Azure DevOps Python API

This repository contains Python APIs for interacting with and managing Azure DevOps. These APIs power the Azure DevOps Extension for Azure CLI. To learn more about the Azure DevOps Extension for Azure CLI, visit the [Microsoft/azure-devops-cli-extension](https://github.com/Microsoft/azure-devops-cli-extension) repo.

## Install 

```
git clone <repo>
python3 -m venv env
source ./env/bin/activate
pip install -r ./hack/requirements.txt
```

## Get started


To use the API, establish a connection using a [personal access token](https://docs.microsoft.com/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=vsts) and the URL to your Azure DevOps organization. Then get a client from the connection and make API calls.

```python
# Fill in with your personal access token, org URL and project
personal_access_token = 'YOURPAT'
organization_url = 'https://dev.azure.com/YOURORG'
project = 'YOURPROJECT'
```

## Usage
Run pipe.py
```bash
$ python3 pipe.py
```
