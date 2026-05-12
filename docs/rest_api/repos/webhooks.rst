Webhook API Documentation
=========================


1. List WebHooks of a Repository
--------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/hooks``

Parameters
~~~~~~~~~~

+--------------+-------+-----------+-----------------------------------+
| Parameter    | Type  | Data Type | Description                       |
+==============+=======+===========+===================================+
| access_token | query | string    | personal access token             |
+--------------+-------+-----------+-----------------------------------+
| owner\*      | path  | string    | Repository Ownership Path         |
|              |       |           | (Company, Organization, or        |
|              |       |           | Personal Path)                    |
+--------------+-------+-----------+-----------------------------------+
| repo\*       | path  | string    | Repository Path(path)             |
+--------------+-------+-----------+-----------------------------------+
| page         | query | int       | Current Page Number               |
+--------------+-------+-----------+-----------------------------------+
| per_page     | query | int       | Items Per Page, Maximum           |
|              |       |           | 100,default:20                    |
+--------------+-------+-----------+-----------------------------------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 9523,
          "url": "http://duxwsqdkyx.cu/pxssss",
          "password": "123445",
          "result": "not found",
          "project_id": 282463,
          "result_code": 503,
          "push_events": false,
          "tag_push_events": false,
          "issues_events": true,
          "note_events": false,
          "merge_requests_events": true,
          "created_at": "2024-09-18T17:51:44+08:00"
        }
      ]

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/repos/mactribe/test02/hooks?access_token={your-token}'


2. Create a WebHook for a Repository
------------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/hooks``


Parameters
~~~~~~~~~~

+-----------------------+----------+-----------+-----------------------+
| Parameter             | Type     | Data Type | Description           |
+=======================+==========+===========+=======================+
| access_token          | formData | string    | personal access token |
+-----------------------+----------+-----------+-----------------------+
| owner\*               | path     | string    | Repository Ownership  |
|                       |          |           | Path (Company,        |
|                       |          |           | Organization, or      |
|                       |          |           | Personal Path)        |
+-----------------------+----------+-----------+-----------------------+
| repo\*                | path     | string    | Repository Path(path) |
+-----------------------+----------+-----------+-----------------------+
| url\*                 | formData | string    | url                   |
+-----------------------+----------+-----------+-----------------------+
| encryption_type       | formData | int       | Encryption Type:      |
|                       |          |           | 0(Password),          |
|                       |          |           | 1(Signature Key)      |
+-----------------------+----------+-----------+-----------------------+
| password              | formData | string    | The password is       |
|                       |          |           | included in the       |
|                       |          |           | request URL to        |
|                       |          |           | prevent malicious     |
|                       |          |           | requests.             |
+-----------------------+----------+-----------+-----------------------+
| push_events           | formData | boolean   | Push Code to          |
|                       |          |           | Repository Event      |
+-----------------------+----------+-----------+-----------------------+
| tag_push_events       | formData | boolean   | Tag Push to           |
|                       |          |           | Repository Event      |
+-----------------------+----------+-----------+-----------------------+
| issues_events         | formData | boolean   | Issue                 |
|                       |          |           | Creation/Closure      |
|                       |          |           | Event                 |
+-----------------------+----------+-----------+-----------------------+
| note_events           | formData | boolean   | Comment on            |
|                       |          |           | Issue/PR/commit Event |
+-----------------------+----------+-----------+-----------------------+
| merge_requests_events | formData | boolean   | Merge Request         |
|                       |          |           | Creation and Merging  |
|                       |          |           | Event                 |
+-----------------------+----------+-----------+-----------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 9529,
        "url": "http://duxwsqdkyx.cu/pxddddd",
        "password": "123445",
        "result": null,
        "project_id": 282463,
        "result_code": 0,
        "push_events": false,
        "tag_push_events": false,
        "issues_events": true,
        "note_events": false,
        "merge_requests_events": true,
        "created_at": "2024-09-26T16:13:27+08:00"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/mactribe/test02/hooks?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "url": "http://duxwsqdkyx.cu/px",
          "encryption_type": 0,
          "password": "123445",
          "push_events": false,
          "tag_push_events": false,
          "issues_events": true,
          "note_events": false,
          "merge_requests_events": true
      }'


3. Get a Specific WebHook of a Repository
-----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/hooks/{id}``


Parameters
~~~~~~~~~~

+--------------+-------+-----------+-----------------------------------+
| Parameter    | Type  | Data Type | Description                       |
+==============+=======+===========+===================================+
| access_token | query | string    | personal access token             |
+--------------+-------+-----------+-----------------------------------+
| owner\*      | path  | string    | Repository Ownership Path         |
|              |       |           | (Company, Organization, or        |
|              |       |           | Personal Path)                    |
+--------------+-------+-----------+-----------------------------------+
| repo\*       | path  | string    | Repository Path(path)             |
+--------------+-------+-----------+-----------------------------------+
| id\*         | path  | string    | ID of Webhook                     |
+--------------+-------+-----------+-----------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 9529,
        "url": "http://duxwsqdkyx.cu/pxddddd",
        "password": "123445",
        "result": null,
        "project_id": 282463,
        "result_code": 0,
        "push_events": false,
        "tag_push_events": false,
        "issues_events": true,
        "note_events": false,
        "merge_requests_events": true,
        "created_at": "2024-09-26T16:13:27+08:00"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/repos/mactribe/test02/hooks/9524?access_token={your-token}'


4. Update a WebHook of a Repository
-----------------------------------


Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}/hooks/{id}``


Parameters
~~~~~~~~~~

+-----------------------+----------+-----------+-----------------------+
| Parameter             | Type     | Data Type | Description           |
+=======================+==========+===========+=======================+
| access_token          | query    | string    | personal access token |
+-----------------------+----------+-----------+-----------------------+
| owner\*               | path     | string    | Repository Ownership  |
|                       |          |           | Path (Company,        |
|                       |          |           | Organization, or      |
|                       |          |           | Personal Path)        |
+-----------------------+----------+-----------+-----------------------+
| repo\*                | path     | string    | Repository Path(path) |
+-----------------------+----------+-----------+-----------------------+
| id\*                  | path     | string    | ID of Webhook         |
+-----------------------+----------+-----------+-----------------------+
| url\*                 | formData | string    | url                   |
+-----------------------+----------+-----------+-----------------------+
| encryption_type       | formData | int       | Encryption Type:      |
|                       |          |           | 0(Password),          |
|                       |          |           | 1(Signature Key)      |
+-----------------------+----------+-----------+-----------------------+
| password              | formData | string    | The password is       |
|                       |          |           | included in the       |
|                       |          |           | request URL to        |
|                       |          |           | prevent malicious     |
|                       |          |           | requests.             |
+-----------------------+----------+-----------+-----------------------+
| push_events           | formData | boolean   | Push Code to          |
|                       |          |           | Repository Event      |
+-----------------------+----------+-----------+-----------------------+
| tag_push_events       | formData | boolean   | Tag Push to           |
|                       |          |           | Repository Event      |
+-----------------------+----------+-----------+-----------------------+
| issues_events         | formData | boolean   | Issue                 |
|                       |          |           | Creation/Closure      |
|                       |          |           | Event                 |
+-----------------------+----------+-----------+-----------------------+
| note_events           | formData | boolean   | Comment on            |
|                       |          |           | Issue/PR/commit Event |
+-----------------------+----------+-----------+-----------------------+
| merge_requests_events | formData | boolean   | Merge Request         |
|                       |          |           | Creation and Merging  |
|                       |          |           | Event                 |
+-----------------------+----------+-----------+-----------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "url": "http://duxwsqdkyx.cu/pxddddd",
        "password": "123445",
        "result": null,
        "project_id": 282463,
        "result_code": 0,
        "push_events": false,
        "tag_push_events": false,
        "issues_events": true,
        "note_events": false,
        "merge_requests_events": true,
        "created_at": "2024-09-26T16:13:27+08:00"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PATCH 'https://api.gitcode.com/api/v5/repos/mactribe/test02/hooks/9516?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "url": "http://duxwsqdkyx.cu/dengmm",
          "encryption_type": 0,
          "password": "334455",
          "push_events": true,
          "tag_push_events": true,
          "issues_events": false,
          "note_events": true,
          "merge_requests_events": true
      }'


5. Delete a WebHook of a Repository
-----------------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/hooks/{id}``


Parameters
~~~~~~~~~~

+--------------+-------+-----------+-----------------------------------+
| Parameter    | Type  | Data Type | Description                       |
+==============+=======+===========+===================================+
| access_token | query | string    | personal access token             |
+--------------+-------+-----------+-----------------------------------+
| owner\*      | path  | string    | Repository Ownership Path         |
|              |       |           | (Company, Organization, or        |
|              |       |           | Personal Path)                    |
+--------------+-------+-----------+-----------------------------------+
| repo\*       | path  | string    | Repository Path(path)             |
+--------------+-------+-----------+-----------------------------------+
| id\*         | path  | string    | ID of Webhook                     |
+--------------+-------+-----------+-----------------------------------+


Response
~~~~~~~~

Http Code: 204, No Content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/repos/mactribe/test02/hooks/9516?access_token={your-token}'


6. Test if a WebHook is Successfully Sent
-----------------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/hooks/{id}/tests``


Parameters
~~~~~~~~~~

+--------------+-------+-----------+-----------------------------------+
| Parameter    | Type  | Data Type | Description                       |
+==============+=======+===========+===================================+
| access_token | query | string    | personal access token             |
+--------------+-------+-----------+-----------------------------------+
| owner\*      | path  | string    | Repository Ownership Path         |
|              |       |           | (Company, Organization, or        |
|              |       |           | Personal Path)                    |
+--------------+-------+-----------+-----------------------------------+
| repo\*       | path  | string    | Repository Path(path)             |
+--------------+-------+-----------+-----------------------------------+
| id\*         | path  | string    | ID of Webhook                     |
+--------------+-------+-----------+-----------------------------------+


Response
~~~~~~~~

Http Code: 204, No Content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/mactribe/test02/hooks/9516/tests?access_token={your-token}'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/webhooks/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
