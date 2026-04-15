OAuth authorizations
====================


1. OAuth Authentication Endpoint
--------------------------------

Request
~~~~~~~

``GET https://gitcode.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state={state}``

============== ======================================== ===== =========
Parameter      Description                              Type  Data Type
============== ======================================== ===== =========
client_id\*    The client ID of the GitCode app         query string
redirect_uri\* redirect url                             query string
scope          scope                                    query string
state          State Parameter, Preventing CSRF Attacks query string
============== ======================================== ===== =========


2. Redirection
--------------

If the user grants your authorization request, GitCode will redirect
back to your specified website, including the code parameter and the
state parameter you provided in the previous step.

``GET {redirect_uri}?code={code}&state={state}``


3. Obtaining an Authorization Token
-----------------------------------

Once you receive the authorization_code in the redirect URL, you can
exchange it for an access token by making a POST request to GitCode’s
token endpoint.

``POST https://gitcode.com/oauth/token?grant_type=authorization_code&code={code}&client_id={client_id}&client_secret={client_secret}``

+-----------------+-------------------+-----------+--------------------+
| Parameter       | Description       | Type      | Data Type          |
+=================+===================+===========+====================+
| grant_type      | grant_type        | query     | authorization_code |
+-----------------+-------------------+-----------+--------------------+
| code\*          | code              | query     | string             |
+-----------------+-------------------+-----------+--------------------+
| client_id\*     | The client ID of  | query     | string             |
|                 | the GitCode app   |           |                    |
+-----------------+-------------------+-----------+--------------------+
| client_secret\* | The secret of the | form-data | string             |
|                 | GitCode app       |           |                    |
+-----------------+-------------------+-----------+--------------------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "access_token": "eyPZPVNfsibj9tap_ibj3t3p",
          "expires_in": 1296000,
          "refresh_token": "b77ced3aee884348852160deab3697a1",
          "scope": "all_user all_key all_groups all_projects all_pr all_issue all_note all_hook all_repository",
          "created_at": "2024-04-20T09:07:59.889Z"
      }


4. Using an Access Token to Access the User Information API
-----------------------------------------------------------

.. container:: highlight

   .. code:: text

      Authorization: Bearer {access_token}
      GET https://api.gitcode.com/api/v5/user


5. Refreshing the Access Token
------------------------------

``POST https://gitcode.com/oauth/token?grant_type=refresh_token&refresh_token={refresh_token}``

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/oauth/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
