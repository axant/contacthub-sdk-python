[![Build Status](https://travis-ci.org/axant/contacthub-sdk-python.svg?branch=master)](https://travis-ci.org/axant/contacthub-sdk-python) [![Coverage Status](https://coveralls.io/repos/github/axant/contacthub-sdk-python/badge.svg)](https://coveralls.io/github/axant/contacthub-sdk-python)

# Contacthub Python SDK

## Table of contents

-   [Introduction](#introdcution)
-   [Getting started](#getting_started)
    -   [Installing and importing the SDK](#installing)
	-   [Performing simple operations on customers](#simpleoperations)
-   [Authentication](#authentication)
-   [Operations on customers](#customers)
    -   [Post a new customer](#postc)
    -   [Get all customers](#getallc)
    -   [Query customers](#query)
    -   [Get a single customer](#getc)
-   [Operations on events](#events)
-   [API Reference](#apireference)

	

<a name="introduction"/>

## Introduction

This is the official Python SDK for [ContactHub REST API](https://contactlab.github.io/contacthub-json-schemas/apidoc.html).
This SDK easily allows to access your data on ContactHub, making the authentication immediate and simplifying reading/writing operations.

For all information about ContactHub, check [here](http://contactlab.com/en/offer/engagement-marketing-platform/contacthub/)

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

#### Getting Customer's data

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

#### Posting a new Customer

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


#### Relationship between Customers and Events

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

If not specified, the SDK will use the default URL for the ConctactHub API - `https://api.contactlab.it/hub/v1` - but you can specify a different base URL for the API:

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

<a name="customers"/>

## Operations on customers
After the [authentication](#authentication), you are ready to perform all operations on ContactHub's entities.


 
### Create and add a new customer

#### Creation
For adding a new customer in a node, first you have to create a new `Customer` object and associate it with his destination node, specifying to his constructor the `Node` object representing the ContactHub node.
In the Customer's constructor you have to specify the structure of the new `Customer` object.

```
from contacthub.entities import Customer, Entity

my_customer = Customer(node=my_node,
                        base=Entity(
                            firstName = 'Bruce',
                            secondName = 'Wayne',
                            contacts=Entity(
                                        email = 'bruce.wayne@darkknight.it', 
                                        fax = 'fax',
                                        otherContacts = [Entity(value='123',name='phone', type='MOBILE')]
                                        )
                                    )
                        )
```
You must specify all required attribute, according to your ContactHub configuration. You can find the required attributes in your [ContactHub dashboard](https://hub.contactlab.it/#/settings/properties).

**N.B.: You must follow the ContatHub schema selected for your base properties. Check the [ContactHub dashboard](https://hub.contactlab.it/#/settings/properties) for further information.**

##### Entity
An important tool for this SDK it's the `Entity` object. It represent a default generic object, used for simplify the declarations.
In `Entity` object constructor you can declare every field you need for creating new entities. These fields can be strings, integer, datetime object, other entities
and lists of above types.

For example:
```
from contacthub.entities import Entity

contacts = Entity(email = 'bruce.wayne@darkknight.it', fax = 'fax', otherContacts = [Entity(value='123',name='phone', type='MOBILE')])

my_customer.base.contacts = contacts
```

##### Extended properties

By default the extended property are already defined in the `Customer` object as an Entity.
You can update this Entity with new integers, strings or other Entities for storing what you need. Extended properties follow a standardized schema defined in the [ContactHub settings](https://hub.contactlab.it/#/settings/properties) for further information.**

```
my_customer.extended.my_extended_int = 1
my_customer.extended.my_extended_string = 'string'
my_customer.extended.my_extended_object = Entity(key='value')
```

#### Adding

Like every other entities in ContactHub, you can perform an operation via two methods:
    Via the Node's standard methods
    Performing the operation directly by your entity's object
 
##### Adding a new customer via the Node's standard method
In the first case, a new `Customer` can be added in ContactHub by the `Node` object:
```
my_node.add_customer(my_customer)
```

If the customer already exist in the node, you can force its update. The match criteria between customers is a configurable options in the [ContactHub settings](https://hub.contactlab.it/#/settings/properties). If the system notice a match between two customers and the flag `force_update` it's setted, the customer will be updated with new data.
```
my_node.add_customer(my_customer, forceUpdate=True)
```

##### Posting a customer directly
In the second case, you can post the new customer directly:

```
my_customer.post()
```

### Get all customers

For getting a list of customers, just:

```
customers = node.get_customers()
```
This method return a list of `Customer` objects. These objects contains all the properties related to the `customers` 
in attribute form, following the JSON schema of ContactHub's Customers.

For example, for accessing the email of a customer:
```
print(my_customer.base.contacts.email)
```

Or accessing the list of manual tag:
```
for tag in my_customer.tags.manual:
    print(tag)
```

In this way you can access every attribute of a single `customer`. 

Note that if you'll try to access for example the `base` attribute of a `Customer`, it will return an `Entity` object, the 
base object for this SDK, that will contain all the base properties of the `Customer` object.


#### Paging the customers

ContactHub allows you to page the list of your customers. You can specify the maximum number of customers per page 
and the page to get.

For example, if you have 50 customers and you want to divide them in 10 per page, getting only the second page, use
the `size` and the `page` parameters in this way:

```
customers = node.get_all_customers(size=10, page=2)
```

This call will return a list of 10 customers, taken from the 2nd page of the total 5.

#### Getting customers by their externalId

If there are many customers with the same `externalId`, you can get a list of them by:

```
customers = node.get_all_customers(externalId="01")
```

If it's stored only one customer associated with the specified externalId, this call will return a single `Customer` object
insted of a list.


#### Getting specific fields of customers

It's possible to filter the fields present in a `Customer`, specifying them in a list of fields: 

```
customers = node.get_all_customers(fields=[Customer.base.email,Customer.base.dob,Customer.extra ])
```
Every element of the fetched list will only have the given fields.

**None of the previous parameter passed to the `get_all_customers` method is required and you can combine them for getting the list of customers that suits your needs.**


### Query customer


### Get a single customer

You can get a single customer by specifying its `id` or `externalId`, getting a new `Customer` object.

By id:
```
my_customer = node.get_customer(id='01')
```

or by the externalId:
```
my_customer = node.get_customer(externalId='02')
```

In this last case, if there are multiple customers assiociated, this method will return a list of `Customers` object, performing the same call of the `get_all_customers(externalId="02")`


### Update a customer

#### Session

#### Tag

