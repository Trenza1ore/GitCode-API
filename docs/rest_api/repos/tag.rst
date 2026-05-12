Tag API Documentation
=====================


1. List All Tags of a Repository
--------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/tags``

Parameters
~~~~~~~~~~

+----------------+-------+-----------+---------------------------------+
| Parameter      | Type  | Data Type | Description                     |
+================+=======+===========+=================================+
| access_token\* | query | string    | personal access token           |
+----------------+-------+-----------+---------------------------------+
| owner\*        | path  | string    | Repository Owner Path           |
|                |       |           | (Organization or User Path)     |
+----------------+-------+-----------+---------------------------------+
| repo\*         | path  | string    | Repository Path(path)           |
+----------------+-------+-----------+---------------------------------+
| page           | query | int       | Current Page Number，default:1  |
+----------------+-------+-----------+---------------------------------+
| per_page       | query | int       | Items Per Page, Maximum         |
|                |       |           | 100,default:20                  |
+----------------+-------+-----------+---------------------------------+

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

+----------------+-------+-----------+---------------------------------+
| Parameter      | Type  | Data Type | Description                     |
+================+=======+===========+=================================+
| owner\*        | path  | string    | Repository Owner Path           |
|                |       |           | (Organization or User Path)     |
+----------------+-------+-----------+---------------------------------+
| repo\*         | path  | string    | Repository Path(path)           |
+----------------+-------+-----------+---------------------------------+
| refs\*         | body  | string    | ref name，default main          |
+----------------+-------+-----------+---------------------------------+
| tag_name\*     | body  | string    | create tag name                 |
+----------------+-------+-----------+---------------------------------+
| tag_message    | body  | string    | Tag Description, default blank  |
+----------------+-------+-----------+---------------------------------+
| access_token\* | query | string    | personal access token           |
+----------------+-------+-----------+---------------------------------+


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

+----------------+-------+-----------+---------------------------------+
| Parameter      | Type  | Data Type | Description                     |
+================+=======+===========+=================================+
| access_token\* | query | string    | personal access token           |
+----------------+-------+-----------+---------------------------------+
| owner\*        | path  | string    | Repository Owner Path           |
|                |       |           | (Organization or User Path)     |
+----------------+-------+-----------+---------------------------------+
| repo\*         | path  | string    | Repository path                 |
+----------------+-------+-----------+---------------------------------+
| page           | query | int       | Current Page Number，default:1  |
|                |       |           | default 1                       |
+----------------+-------+-----------+---------------------------------+
| per_page       | query | int       | Number of items per page: max   |
|                |       |           | 100, default 20                 |
+----------------+-------+-----------+---------------------------------+


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

+----------------+-------+-----------+---------------------------------+
| Parameter      | Type  | Data Type | Description                     |
+================+=======+===========+=================================+
| access token\* | query | string    | Personal access token           |
+----------------+-------+-----------+---------------------------------+
| owner\*        | path  | string    | Repository Owner Path           |
|                |       |           | (Organization or User Path)     |
+----------------+-------+-----------+---------------------------------+
| repo\*         | path  | string    | Repository path                 |
+----------------+-------+-----------+---------------------------------+
| tag_name\*     | path  | string    | Tag name                        |
+----------------+-------+-----------+---------------------------------+


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

+----------------+-------+-----------+---------------------------------+
| Parameter      | Type  | Data Type | Description                     |
+================+=======+===========+=================================+
| access token\* | query | string    | Personal access token           |
+----------------+-------+-----------+---------------------------------+
| owner\*        | path  | string    | Repository Owner Path           |
|                |       |           | (Organization or User Path)     |
+----------------+-------+-----------+---------------------------------+
| repo\*         | path  | string    | Repository path                 |
+----------------+-------+-----------+---------------------------------+
| tag_name\*     | path  | string    | Tag name                        |
+----------------+-------+-----------+---------------------------------+


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

+------------------------+-------+-----------+------------------------+
| Parameter              | Type  | Data Type | Description            |
+========================+=======+===========+========================+
| access token\*         | query | string    | Personal access token  |
+------------------------+-------+-----------+------------------------+
| owner\*                | path  | string    | Repository Owner Path  |
|                        |       |           | (Organization or User  |
|                        |       |           | Path)                  |
+------------------------+-------+-----------+------------------------+
| repo\*                 | path  | string    | Repository path        |
+------------------------+-------+-----------+------------------------+
| name\*                 | body  | string    | Tag name               |
+------------------------+-------+-----------+------------------------+
| create_access_level    | body  | int       | Allowed creation       |
|                        |       |           | access level (0: No    |
|                        |       |           | one; 30: Developer,    |
|                        |       |           | Maintainer, Admin; 40: |
|                        |       |           | Maintainer, Admin),    |
|                        |       |           | default: 40            |
+------------------------+-------+-----------+------------------------+


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

+------------------------+-------+-----------+------------------------+
| Parameter              | Type  | Data Type | Description            |
+========================+=======+===========+========================+
| access token\*         | query | string    | Personal access token  |
+------------------------+-------+-----------+------------------------+
| owner\*                | path  | string    | Repository Owner Path  |
|                        |       |           | (Organization or User  |
|                        |       |           | Path)                  |
+------------------------+-------+-----------+------------------------+
| repo\*                 | path  | string    | Repository path        |
+------------------------+-------+-----------+------------------------+
| name\*                 | body  | string    | Tag name               |
+------------------------+-------+-----------+------------------------+
| create_access_level\*  | body  | int       | Allowed creation       |
|                        |       |           | access level (0: No    |
|                        |       |           | one; 30: Developer,    |
|                        |       |           | Maintainer, Admin; 40: |
|                        |       |           | Maintainer, Admin)     |
+------------------------+-------+-----------+------------------------+


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
