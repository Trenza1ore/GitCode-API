Tag API Documentation
=====================


1. List All Tags of a Repository
--------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/tags``

Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| owner\*        | Repository Owner Path           | path  | string    |
|                | (Organization or User Path)     |       |           |
+----------------+---------------------------------+-------+-----------+
| repo\*         | Repository Path(path)           | path  | string    |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number，default:1  | query | int       |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum         | query | int       |
|                | 100,default:20                  |       |           |
+----------------+---------------------------------+-------+-----------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "name": "v1.0",
          "message": "111",
          "commit": {
            "sha": "3e43581d16bc456802a1fee673b9a2a9b9618f0f",
            "date": "2024-04-14T02:59:22+00:00"
          },
          "tagger": {
            "name": "占分",
            "email": "7543745+centking@user.noreply.gitcode.com",
            "date": "2024-04-14T06:18:54+00:00"
          }
        }
      ]

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/tags?access_token=xxxx'


2. Create a Tag for a Repository
--------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/tags``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| owner\*        | Repository Owner Path           | path  | string    |
|                | (Organization or User Path)     |       |           |
+----------------+---------------------------------+-------+-----------+
| repo\*         | Repository Path(path)           | path  | string    |
+----------------+---------------------------------+-------+-----------+
| refs\*         | ref name，default main          | body  | string    |
+----------------+---------------------------------+-------+-----------+
| tag_name\*     | create tag name                 | body  | string    |
+----------------+---------------------------------+-------+-----------+
| tag_message    | Tag Description, default blank  | body  | string    |
+----------------+---------------------------------+-------+-----------+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "name": "tag2",
        "message": "",
        "commit": {
          "sha": "5d165dae3b073d3e92ca91c3edcb21994361462c",
          "date": "2024-04-08T13:13:33+00:00"
        },
        "tagger": null
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/tags?access_token=xxxx' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "refs": "main",
          "tag_name": "tag",
      }'


3. List Protected Tags for a Repository
---------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/protected_tags``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| owner\*        | Repository Owner Path           | path  | string    |
|                | (Organization or User Path)     |       |           |
+----------------+---------------------------------+-------+-----------+
| repo\*         | Repository path                 | path  | string    |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number，default:1  | query | int       |
|                | default 1                       |       |           |
+----------------+---------------------------------+-------+-----------+
| per_page       | Number of items per page: max   | query | int       |
|                | 100, default 20                 |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "name": "tag_name",
          "create_access_level": 30,
          "create_access_level_desc": "Developer, Maintainer, Admin"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/test-org/test-repo/protected_tags?access_token=your-token'


4. Delete Protected Tag
-----------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/protected_tags/{tag_name}``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access token\* | Personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| owner\*        | Repository Owner Path           | path  | string    |
|                | (Organization or User Path)     |       |           |
+----------------+---------------------------------+-------+-----------+
| repo\*         | Repository path                 | path  | string    |
+----------------+---------------------------------+-------+-----------+
| tag_name\*     | Tag name                        | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      HTTP status 204 No Content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/repos/test-org/test-repo/protected_tags/your_tag?access_token=your-token'


5. Get Protected Tag Details
----------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/protected_tags/{tag_name}``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access token\* | Personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| owner\*        | Repository Owner Path           | path  | string    |
|                | (Organization or User Path)     |       |           |
+----------------+---------------------------------+-------+-----------+
| repo\*         | Repository path                 | path  | string    |
+----------------+---------------------------------+-------+-----------+
| tag_name\*     | Tag name                        | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "name": "tag_name",
        "create_access_level": 30,
        "create_access_level_desc": "Developer, Maintainer, Admin"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/test-org/test-repo/protected_tags/your_tag?access_token=your-token'


6. Create Protected Tag
-----------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/protected_tags``


Parameters
~~~~~~~~~~

+------------------------+------------------------+-------+-----------+
| Parameter              | Description            | Type  | Data Type |
+========================+========================+=======+===========+
| access token\*         | Personal access token  | query | string    |
+------------------------+------------------------+-------+-----------+
| owner\*                | Repository Owner Path  | path  | string    |
|                        | (Organization or User  |       |           |
|                        | Path)                  |       |           |
+------------------------+------------------------+-------+-----------+
| repo\*                 | Repository path        | path  | string    |
+------------------------+------------------------+-------+-----------+
| name\*                 | Tag name               | body  | string    |
+------------------------+------------------------+-------+-----------+
| create_access_level    | Allowed creation       | body  | int       |
|                        | access level (0: No    |       |           |
|                        | one; 30: Developer,    |       |           |
|                        | Maintainer, Admin; 40: |       |           |
|                        | Maintainer, Admin),    |       |           |
|                        | default: 40            |       |           |
+------------------------+------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "name": "your_tag_name",
        "create_access_level": 30,
        "create_access_level_desc": "Developer, Maintainer, Admin"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/test-org/test-repo/protected_tags?access_token=your-token' \
      --header 'Content-Type: application/json' \
      --data '{"name": "your_tag_name", "create_access_level": 30}'


7. Update Protected Tag
-----------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/protected_tags``


Parameters
~~~~~~~~~~

+------------------------+------------------------+-------+-----------+
| Parameter              | Description            | Type  | Data Type |
+========================+========================+=======+===========+
| access token\*         | Personal access token  | query | string    |
+------------------------+------------------------+-------+-----------+
| owner\*                | Repository Owner Path  | path  | string    |
|                        | (Organization or User  |       |           |
|                        | Path)                  |       |           |
+------------------------+------------------------+-------+-----------+
| repo\*                 | Repository path        | path  | string    |
+------------------------+------------------------+-------+-----------+
| name\*                 | Tag name               | body  | string    |
+------------------------+------------------------+-------+-----------+
| create_access_level\*  | Allowed creation       | body  | int       |
|                        | access level (0: No    |       |           |
|                        | one; 30: Developer,    |       |           |
|                        | Maintainer, Admin; 40: |       |           |
|                        | Maintainer, Admin)     |       |           |
+------------------------+------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "name": "your_tag_name",
        "create_access_level": 30,
        "create_access_level_desc": "Developer, Maintainer, Admin"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/test-org/test-repo/protected_tags?access_token=your-token' \
      --header 'Content-Type: application/json' \
      --data '{"name": "your_tag_name", "create_access_level": 30}'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/tag/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
