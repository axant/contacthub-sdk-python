[![Build Status](https://travis-ci.org/axant/contacthub-sdk-python.svg?branch=master)](https://travis-ci.org/axant/contacthub-sdk-python) [![Coverage Status](https://coveralls.io/repos/github/axant/contacthub-sdk-python/badge.svg)](https://coveralls.io/github/axant/contacthub-sdk-python)

# Contacthub Python SDK

## Table of contents

-   [Installing and importing the SDK](#installing)
-   [Authentication](#authentication)
    -   [Workspace](#workspace)
	-   [Authenticating via configuration file](#authviaconfig)
	-   [Node](#node)

<a name="installing"/>
## Installing and importing the SDK

The ContactHub SDK can be installed from PyPi:

```
pip install contacthub
```
After installing, for importing the contacthub SDK just:

```
import contacthub
```

<a name="authentication"/>
## Authentication

<a name="workspace"/>
### Workspace

You can create a `Workspace` object that allows the control of the workspace's nodes. Pass to it the given workspace id and the access token

```
my_workspace = Workspace(workspace_id, token)
```

If not specified, the SDK will use the default URL for the ConctactHub API: https://api.contactlab.it/hub/v1
You can also specify a different base URL for the API:

```
my_workspace = Workspace(workspace_id, token, base_url)
```
<a name="authviaconfig"/>
### Authenticating via configuration file

It's possible specifying the workspace ID and the access token via INI file:

```
my_workspace = Workspace.from_INI_file('file.INI')
```

The file must follow this template :
```
workspace_id = workspace_id
token = token
base_url = base_url
```

You can also specify a different base URL for the API in this file. If ommited, the default base URL will be used.

<a name="node"/>
### Node

Once obtained a workspace, you can access the various nodes linked to it with the `get_node` method, specifying the node ID. 

```
my_node = workspace.get_node(node_id)
```

This method will return a `Node` object, that allows you to call all methods related to the various entity of ContactHub.