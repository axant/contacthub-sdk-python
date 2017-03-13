.. _getting_started:

Getting started
===============

Installing the SDK
------------------

The ContactHub SDK can be installed from PyPi::

   pip install contacthub

After installing, for importing the contacthub SDK in your project just::

   import contacthub

Performing simple operations on entities
----------------------------------------

Getting Customer's data
^^^^^^^^^^^^^^^^^^^^^^^
Retrieving entity's data can be easily archived with simple operations.

First of all, you need to authenticate with credentials provided by `ContactHub`:

.. code-block:: python

    from contacthub import Workspace

    workspace = Workspace(workspace_id = 'workspace_id', token = 'token')

After that you can get a `Node` object to perform all operations on customers and events:

.. code-block:: python

   my_node = workspace.get_node(node_id='node_id')

A ``Node`` is the key object for get, post, put, patch and delete data on entities.

With a node, is immediate to get all customers data in a ``list`` of ``Customer`` objects:

.. code-block:: python

   customers = my_node.customers

   for customer in customers:
      print(customer.base.firstName)


Getting a single ``Customer``:

.. code-block:: python

   my_customer = my_node.get_customer(id='id')

   print('Welcome back %s', % my_customer.base.firstName)

or querying on customers by theirs own properties:

.. code-block:: python

   fetched_customers = my_node.query(Customer).filter((Customer.base.firstName == 'Bruce') & (Customer.base.secondName == 'Wayne')).all()

Posting a new Customer
^^^^^^^^^^^^^^^^^^^^^^

Creating and posting a Customer is simple as getting:

.. code-block:: python

    from contacthub.models import Customer

    my_customer = Customer(node = my_node)
    my_customer.base.contacts.email = 'myemail@email.com'
    my_customer.extended['my_string'] = 'my new extended property string'
    my_customer.post()

After creating, another way to post a new entity's object is using a ``Node``:

.. code-block:: python

    my_node.post(my_customer)

Both instructions have same effects, you have only to choose the more comfortable way!


Relationship between Customers and Events
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this SDK entities are easily connected.
For retrieving all events associated to a ``Customer``, just:

.. code-block:: python

    my_customer = my_node.get_customer(id='id')
    events = my_customer.events

Note that relations are immutable objects. You can just consult events associated to a ``Customer``,
but you cannot add new ones or delete.