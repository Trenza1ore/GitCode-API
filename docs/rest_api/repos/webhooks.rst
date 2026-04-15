Webhook API Documentation
=========================


1. List WebHooks of a Repository
--------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/hooks``

Parameters
~~~~~~~~~~

+--------------+-----------------------------------+-------+-----------+
| Parameter    | Description                       | Type  | Data Type |
+==============+===================================+=======+===========+
| access_token | personal access token             | query | string    |
+--------------+-----------------------------------+-------+-----------+
| owner\*      | Repository Ownership Path         | path  | string    |
|              | (Company, Organization, or        |       |           |
|              | Personal Path)                    |       |           |
+--------------+-----------------------------------+-------+-----------+
| repo\*       | Repository Path(path)             | path  | string    |
+--------------+-----------------------------------+-------+-----------+
| page         | Current Page Number               | query | int       |
+--------------+-----------------------------------+-------+-----------+
| per_page     | Items Per Page, Maximum           | query | int       |
|              | 100,default:20                    |       |           |
+--------------+-----------------------------------+-------+-----------+

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

+-----------------------+-----------------------+----------+-----------+
| Parameter             | Description           | Type     | Data Type |
+=======================+=======================+==========+===========+
| access_token          | personal access token | formData | string    |
+-----------------------+-----------------------+----------+-----------+
| owner\*               | Repository Ownership  | path     | string    |
|                       | Path (Company,        |          |           |
|                       | Organization, or      |          |           |
|                       | Personal Path)        |          |           |
+-----------------------+-----------------------+----------+-----------+
| repo\*                | Repository Path(path) | path     | string    |
+-----------------------+-----------------------+----------+-----------+
| url\*                 | url                   | formData | string    |
+-----------------------+-----------------------+----------+-----------+
| encryption_type       | Encryption Type:      | formData | int       |
|                       | 0(Password),          |          |           |
|                       | 1(Signature Key)      |          |           |
+-----------------------+-----------------------+----------+-----------+
| password              | The password is       | formData | string    |
|                       | included in the       |          |           |
|                       | request URL to        |          |           |
|                       | prevent malicious     |          |           |
|                       | requests.             |          |           |
+-----------------------+-----------------------+----------+-----------+
| push_events           | Push Code to          | formData | boolean   |
|                       | Repository Event      |          |           |
+-----------------------+-----------------------+----------+-----------+
| tag_push_events       | Tag Push to           | formData | boolean   |
|                       | Repository Event      |          |           |
+-----------------------+-----------------------+----------+-----------+
| issues_events         | Issue                 | formData | boolean   |
|                       | Creation/Closure      |          |           |
|                       | Event                 |          |           |
+-----------------------+-----------------------+----------+-----------+
| note_events           | Comment on            | formData | boolean   |
|                       | Issue/PR/commit Event |          |           |
+-----------------------+-----------------------+----------+-----------+
| merge_requests_events | Merge Request         | formData | boolean   |
|                       | Creation and Merging  |          |           |
|                       | Event                 |          |           |
+-----------------------+-----------------------+----------+-----------+


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

+--------------+-----------------------------------+-------+-----------+
| Parameter    | Description                       | Type  | Data Type |
+==============+===================================+=======+===========+
| access_token | personal access token             | query | string    |
+--------------+-----------------------------------+-------+-----------+
| owner\*      | Repository Ownership Path         | path  | string    |
|              | (Company, Organization, or        |       |           |
|              | Personal Path)                    |       |           |
+--------------+-----------------------------------+-------+-----------+
| repo\*       | Repository Path(path)             | path  | string    |
+--------------+-----------------------------------+-------+-----------+
| id\*         | ID of Webhook                     | path  | string    |
+--------------+-----------------------------------+-------+-----------+


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

+-----------------------+-----------------------+----------+-----------+
| Parameter             | Description           | Type     | Data Type |
+=======================+=======================+==========+===========+
| access_token          | personal access token | query    | string    |
+-----------------------+-----------------------+----------+-----------+
| owner\*               | Repository Ownership  | path     | string    |
|                       | Path (Company,        |          |           |
|                       | Organization, or      |          |           |
|                       | Personal Path)        |          |           |
+-----------------------+-----------------------+----------+-----------+
| repo\*                | Repository Path(path) | path     | string    |
+-----------------------+-----------------------+----------+-----------+
| id\*                  | ID of Webhook         | path     | string    |
+-----------------------+-----------------------+----------+-----------+
| url\*                 | url                   | formData | string    |
+-----------------------+-----------------------+----------+-----------+
| encryption_type       | Encryption Type:      | formData | int       |
|                       | 0(Password),          |          |           |
|                       | 1(Signature Key)      |          |           |
+-----------------------+-----------------------+----------+-----------+
| password              | The password is       | formData | string    |
|                       | included in the       |          |           |
|                       | request URL to        |          |           |
|                       | prevent malicious     |          |           |
|                       | requests.             |          |           |
+-----------------------+-----------------------+----------+-----------+
| push_events           | Push Code to          | formData | boolean   |
|                       | Repository Event      |          |           |
+-----------------------+-----------------------+----------+-----------+
| tag_push_events       | Tag Push to           | formData | boolean   |
|                       | Repository Event      |          |           |
+-----------------------+-----------------------+----------+-----------+
| issues_events         | Issue                 | formData | boolean   |
|                       | Creation/Closure      |          |           |
|                       | Event                 |          |           |
+-----------------------+-----------------------+----------+-----------+
| note_events           | Comment on            | formData | boolean   |
|                       | Issue/PR/commit Event |          |           |
+-----------------------+-----------------------+----------+-----------+
| merge_requests_events | Merge Request         | formData | boolean   |
|                       | Creation and Merging  |          |           |
|                       | Event                 |          |           |
+-----------------------+-----------------------+----------+-----------+


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

+--------------+-----------------------------------+-------+-----------+
| Parameter    | Description                       | Type  | Data Type |
+==============+===================================+=======+===========+
| access_token | personal access token             | query | string    |
+--------------+-----------------------------------+-------+-----------+
| owner\*      | Repository Ownership Path         | path  | string    |
|              | (Company, Organization, or        |       |           |
|              | Personal Path)                    |       |           |
+--------------+-----------------------------------+-------+-----------+
| repo\*       | Repository Path(path)             | path  | string    |
+--------------+-----------------------------------+-------+-----------+
| id\*         | ID of Webhook                     | path  | string    |
+--------------+-----------------------------------+-------+-----------+


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

+--------------+-----------------------------------+-------+-----------+
| Parameter    | Description                       | Type  | Data Type |
+==============+===================================+=======+===========+
| access_token | personal access token             | query | string    |
+--------------+-----------------------------------+-------+-----------+
| owner\*      | Repository Ownership Path         | path  | string    |
|              | (Company, Organization, or        |       |           |
|              | Personal Path)                    |       |           |
+--------------+-----------------------------------+-------+-----------+
| repo\*       | Repository Path(path)             | path  | string    |
+--------------+-----------------------------------+-------+-----------+
| id\*         | ID of Webhook                     | path  | string    |
+--------------+-----------------------------------+-------+-----------+


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
