Member API Documentation
========================


1. Add or Update Repository Member Permissions
----------------------------------------------

Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/collaborators/{username}``

Parameters
~~~~~~~~~~

+----------------+----------+-----------+------------------------------+
| Parameter      | Type     | Data Type | Description                  |
+================+==========+===========+==============================+
| access_token\* | query    | string    | personal access token        |
+----------------+----------+-----------+------------------------------+
| owner\*        | path     | string    | Repository Owner Path        |
|                |          |           | (Organization or User Path)  |
+----------------+----------+-----------+------------------------------+
| repo\*         | path     | string    | Repository Path(path)        |
+----------------+----------+-----------+------------------------------+
| username\*     | path     | string    | username/login               |
+----------------+----------+-----------+------------------------------+
| permission     | formData | string    | permission: pull, push,      |
|                |          |           | admin, customer role name.   |
|                |          |           | Default: push                |
+----------------+----------+-----------+------------------------------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 7543745,
        "login": "centking",
        "name": "占分",
        "avatar_url": null,
        "html_url": "https://gitcode.com/centking",
        "remark": "",
        "type": "User",
        "permissions": {
          "pull": true,
          "push": true,
          "admin": false
        }
      }

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'http://api.gitcode.com/api/v5/repos/dengmengmian/test03/collaborators/user1?access_token={your-token}' \
      --form 'permission="admin"'


2. Remove a Repository Member
-----------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/collaborators/{username}``


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
| username\*     | path  | string    | username/login                  |
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

      curl --location --request DELETE 'http://api.gitcode.com/api/v5/repos/dengmengmian/test03/collaborators/user1?access_token={your-token}' \


3. Get All Members of a Repository
----------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/collaborators``


Parameters
~~~~~~~~~~

+----------------+----------+-----------+------------------------------+
| Parameter      | Type     | Data Type | Description                  |
+================+==========+===========+==============================+
| access_token\* | formData | string    | personal access token        |
+----------------+----------+-----------+------------------------------+
| owner\*        | path     | string    | Repository Owner Path        |
|                |          |           | (Organization or User Path)  |
+----------------+----------+-----------+------------------------------+
| repo\*         | path     | string    | Repository Path(path)        |
+----------------+----------+-----------+------------------------------+
| page           | query    | int       | Current Page                 |
|                |          |           | Number，default:1            |
+----------------+----------+-----------+------------------------------+
| per_page       | query    | int       | Items Per Page, Maximum      |
|                |          |           | 100,default:20               |
+----------------+----------+-----------+------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": "708",
          "name": "Lzm_0916",
          "username": "Lzm_0916",
          "nick_name": null,
          "state": null,
          "avatar": null,
          "avatar_url": null,
          "email": null,
          "name_cn": null,
          "web_url": "https://test.gitcode.net/Lzm_0916",
          "access_level": null,
          "expires_at": null,
          "limited": null,
          "type": "ProjectMember",
          "last_owner": null,
          "is_current_source_member": null,
          "last_source_owner": null,
          "join_way": null,
          "source_name": null,
          "member_roles": null,
          "iam_id": null,
          "committer_system_from": null,
          "permissions": {
            "pull": null,
            "push": null,
            "admin": true
          }
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location  'http://api.gitcode.com/api/v5/repos/dengmengmian/test03/collaborators?access_token={your-token}' \


4. Check if a User is a Member of a Repository
----------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/collaborators/{username}``


Parameters
~~~~~~~~~~

+----------------+-------+-----------+---------------------------------+
| Parameter      | Type  | Data Type | Description                     |
+================+=======+===========+=================================+
| access_token\* | query | string    | personal access token           |
+----------------+-------+-----------+---------------------------------+
| owner\*        | path  | string    | Repository Ownership Path       |
|                |       |           | (Company, Organization, or      |
|                |       |           | Personal Path)                  |
+----------------+-------+-----------+---------------------------------+
| repo\*         | path  | string    | Repository Path(path)           |
+----------------+-------+-----------+---------------------------------+
| username       | path  | string    | username/login                  |
+----------------+-------+-----------+---------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "message": "404 Not Found"
      }
      or
      {

      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/collaborators/dengmengmian1?access_token=yuBy'


5. View the Permissions of a Repository Member
----------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/collaborators/{username}/permission``


Parameters
~~~~~~~~~~

+----------------+-------+-----------+---------------------------------+
| Parameter      | Type  | Data Type | Description                     |
+================+=======+===========+=================================+
| access_token\* | query | string    | personal access token           |
+----------------+-------+-----------+---------------------------------+
| owner\*        | path  | string    | Repository Ownership Path       |
|                |       |           | (Company, Organization, or      |
|                |       |           | Personal Path)                  |
+----------------+-------+-----------+---------------------------------+
| repo\*         | path  | string    | Repository Path(path)           |
+----------------+-------+-----------+---------------------------------+
| username\*     | path  | string    | username/login                  |
+----------------+-------+-----------+---------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 268,
        "login": "dengmengmian",
        "permission": "admin"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/collaborators/dengmengmian/permission?access_token=yuBy'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/member/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
