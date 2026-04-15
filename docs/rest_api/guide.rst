GitCode REST API
================

The GitCode API offers powerful features, enabling developers to
interact programmatically with resources on GitCode. This documentation
will guide you on how to use the GitCode API, covering topics such as
making effective API requests, authentication methods, status codes,
pagination, path parameters, and more.

Effective API Requests
----------------------

To make a request to the GitCode API, you must include the ``api path``
and specify the ``API version``. The current available version is
``/api/v5``.

Here is a basic example of making a request to the GitCode API:

.. container:: highlight

   .. code:: text

      curl "https://api.gitcode.com/api/v5/users/{username}"

Authentication
--------------

Most GitCode API requests require authentication, or they will only
return public data if no authentication is provided. The documentation
for each endpoint will specify whether authentication is required.

You can authenticate to the GitCode API using a `Personal Access
Token <https://gitcode.com/setting/token-classic>`__ .

If the authentication information is invalid or missing, GitCode will
return an error with the status code 401:

.. container:: highlight

   .. code:: text

      {
        "message": "401 Unauthorized"
      }

Authorization
~~~~~~~~~~~~~

You can authenticate using the API by passing your Personal Access Token
in the ``Authorization`` header.

Example of the Personal Access Token in the Request Header:

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/user' \
      --header 'Authorization: Bearer {your-token}'

PRIVATE-TOKEN
~~~~~~~~~~~~~

You can authenticate by passing your Personal Access Token in the
``PRIVATE-TOKEN`` header.

Example of the Personal Access Token in the Request Header:

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/user' \
      --header 'PRIVATE-TOKEN: {your-token}'

access_token
~~~~~~~~~~~~

You can authenticate by passing your Personal Access Token in the
``access_token`` query parameter.

Example of the Personal Access Token in the Query:

.. container:: highlight

   .. code:: text

      curl  "https://api.gitcode.com/api/v5/users/{username}?access_token={your-token}"

Response Codes
--------------

The GitCode API returns different status codes based on the context and
operation. This helps you understand what went wrong if a request
results in an error.

The following table outlines the general behavior of the GitCode API
functions:

+-------------------+--------------------------------------------------+
| Request Type      | Description                                      |
+===================+==================================================+
| ``GET``           | Access one or more resources and return the      |
|                   | result in JSON format                            |
+-------------------+--------------------------------------------------+
| ``POST``          | If the resource is successfully created, returns |
|                   | ``201 Created`` and the newly created resource   |
|                   | in JSON format                                   |
+-------------------+--------------------------------------------------+
| ``GET`` / ``PUT`` | If the resource is successfully accessed or      |
|                   | modified, returns ``200 OK``, and the (modified) |
|                   | result is returned in JSON format                |
+-------------------+--------------------------------------------------+
| ``DELETE``        | If the resource is successfully deleted, returns |
|                   | ``204 No Content``; if the resource is scheduled |
|                   | for deletion, returns ``202 Accepted``           |
+-------------------+--------------------------------------------------+

Here are the possible return codes for GitCode API requests:

+-----------------------------+----------------------------------------+
| Response Code               | Description                            |
+=============================+========================================+
| ``200 OK``                  | The ``GET``, ``PUT``, or ``DELETE``    |
|                             | request was successful, and the        |
|                             | resource itself is returned in JSON    |
|                             | format                                 |
+-----------------------------+----------------------------------------+
| ``201 Created``             | The ``POST`` request was successful,   |
|                             | and the resource is returned in JSON   |
|                             | format                                 |
+-----------------------------+----------------------------------------+
| ``202 Accepted``            | The ``GET``, ``PUT``, or ``DELETE``    |
|                             | request was successful, and the        |
|                             | resource is planned for processing     |
+-----------------------------+----------------------------------------+
| ``204 No Content``          | The server successfully fulfilled the  |
|                             | request, but no additional content is  |
|                             | sent in the response body              |
+-----------------------------+----------------------------------------+
| ``301 Moved Permanently``   | The resource has been moved to a new   |
|                             | URL provided in the ``Location``       |
|                             | header                                 |
+-----------------------------+----------------------------------------+
| ``304 Not Modified``        | The resource has not been modified     |
|                             | since the last request                 |
+-----------------------------+----------------------------------------+
| ``400 Bad Request``         | A required attribute for the API       |
|                             | request is missing. For example, the   |
|                             | title of an issue is not provided      |
+-----------------------------+----------------------------------------+
| ``401 Unauthorized``        | The user is unauthenticated. A valid   |
|                             | user token is required                 |
+-----------------------------+----------------------------------------+
| ``403 Forbidden``           | The request is not allowed. For        |
|                             | example, the user is not authorized to |
|                             | delete a project                       |
+-----------------------------+----------------------------------------+
| ``404 Not Found``           | The resource cannot be accessed. For   |
|                             | example, the resource ID cannot be     |
|                             | found or the user does not have access |
|                             | to it                                  |
+-----------------------------+----------------------------------------+
| ``405 Method Not Allowed``  | The request method is not supported    |
+-----------------------------+----------------------------------------+
| ``409 Conflict``            | A conflicting resource already exists. |
|                             | For example, creating a project with   |
|                             | an existing name                       |
+-----------------------------+----------------------------------------+
| ``412 Precondition Failed`` | The request was rejected. This can     |
|                             | occur when trying to delete a resource |
|                             | that has been modified during the      |
|                             | process, if the                        |
|                             | ``If-Unmodified-Since`` header is      |
|                             | provided                               |
+-----------------------------+----------------------------------------+
| ``418 I'm a teapot``        | Request Rejected, Suspected Unsafe     |
+-----------------------------+----------------------------------------+
| ``422 Unprocessable``       | The entity cannot be processed         |
+-----------------------------+----------------------------------------+
| ``429 Too Many Requests``   | The user has exceeded the rate limit   |
|                             | for the application                    |
+-----------------------------+----------------------------------------+
| ``500 Server Error``        | The server encountered an error while  |
|                             | processing the request                 |
+-----------------------------+----------------------------------------+
| ``503 Service Unavailable`` | The server cannot handle the request   |
|                             | because it is temporarily overloaded   |
+-----------------------------+----------------------------------------+
| ``504 Time Out``            | Gateway Timeout: Network Timeout       |
+-----------------------------+----------------------------------------+

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/guide/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
