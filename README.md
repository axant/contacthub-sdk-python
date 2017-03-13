[![Build Status](https://travis-ci.org/axant/contacthub-sdk-python.svg?branch=master)](https://travis-ci.org/axant/contacthub-sdk-python) [![Coverage Status](https://coveralls.io/repos/github/axant/contacthub-sdk-python/badge.svg)](https://coveralls.io/github/axant/contacthub-sdk-python)

# Contacthub Python SDK

## Table of contents

-   [Introduction](#introdcution)
-   [Getting started](#getting_started)
    -   [Installing and importing the SDK](#installing)
	-   [Performing simple operations on customers](#simpleoperations)
-   [Authentication](#authentication)
	

<a name="introduction"/>
## Introduction
This is the official Python SDK for [ContactHub REST API] (https://contactlab.github.io/contacthub-json-schemas/apidoc.html).
This SDK easily allows to access your data on ContactHub, making the authentication immediate and simplifying reading/writing operations.

For all information about ContactHub, check [here] http://contactlab.com/en/offer/engagement-marketing-platform/contacthub/

<a name="getting_started"/>
## Getting started

<a name="installing"/>
### Installing and importing the SDK

The ContactHub SDK can be installed from PyPi:

```
pip install contacthub
```
After installing, for importing the contacthub SDK just:

```
import contacthub
```

<a name="simpleoperations"/>
### Performing simple operations on customers

####Getting Customer's data

Retrieving entity's data can be easily archived with simple operations.

First of all, you need to authenticate with credentials provided by `ContactHub`:

```
from contacthub import Workspace

workspace = Workspace(workspace_id = 'workspace_id', token = 'token')
```

After that you can get a `Node` object to perform all operations on customers and events:

```
my_node = workspace.get_node(node_id='node_id')
```

With a node, is immediate to get all customers data in a ``list`` of ``Customer`` objects:

```
customers = my_node.customers

for customer in customers:
  print(customer.base.firstName)
```

Getting a single ``Customer``:

```
my_customer = my_node.get_customer(id='id')

print('Welcome back %s', % my_customer.base.firstName)
```
or querying on customers by theirs own properties:

```
fetched_customers = my_node.query(Customer).filter((Customer.base.firstName == 'Bruce') & (Customer.base.secondName == 'Wayne')).all()
```

####Posting a new Customer

Creating and posting a Customer is simple as getting:

```

from contacthub.models import Customer

my_customer = Customer(node = my_node)
my_customer.base.contacts.email = 'myemail@email.com'
my_customer.extended['my_string'] = 'my new extended property string'
my_customer.post()
```

After creating, another way to post the new Customer object is using a ``Node``:

```
my_node.post(my_customer)
```

Both instructions have same effects, you have only to choose the more comfortable way!


####Relationship between Customers and Events

In this SDK entities are easily connected.
For retrieving all events associated to a ``Customer``, just:

```
my_customer = my_node.get_customer(id='id')
events = my_customer.events
```

Note that relations are immutable objects. You can just consult events associated to a ``Customer``,
but you cannot add new ones or delete.

<a name="authentication"/>
## Authentication

You can create a `Workspace` object that allows the control of the workspace's nodes. It require the workspace id and the access token provided by
ContactHub. 

```
my_workspace = Workspace(workspace_id='workspace_id', token='token')
```

If not specified, the SDK will use the default URL for the ConctactHub API: https://api.contactlab.it/hub/v1
You can also specify a different base URL for the API:

```
my_workspace = Workspace(workspace_id='workspace_id', token='token', base_url='base_url')
```

Once obtained a workspace, you're able to access the various nodes linked to it with the `get_node` method:
```
my_node = workspace.get_node(node_id='node_id')
```

This method will return a `Node` object, that allows you to perform all operations on customers and events.
A ``Node`` is a key object for getting, posting, putting, patching and deleting data on entities.

### Authenticating via configuration file

You can specify the workspace ID, the access token and the base url (not mandatory. If ommited, the default base URL for ContactHub will be used) 
via INI file:

```
my_workspace = Workspace.from_INI_file('file.INI')
```

The file must follow this template :
```
workspace_id = workspace_id
token = token
base_url = base_url
```