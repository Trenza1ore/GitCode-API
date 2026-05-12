Milestone API Documentation
===========================


1. Get All Milestones of a Repository
-------------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/milestones``

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
| state        | query | string    | state: open, closed,              |
|              |       |           | all。Default: open                |
+--------------+-------+-----------+-----------------------------------+
| sort         | query | string    | sort: due_on                      |
+--------------+-------+-----------+-----------------------------------+
| direction    | query | string    | asc/desc, Default: asc            |
+--------------+-------+-----------+-----------------------------------+
| page         | query | int       | Current Page Number               |
+--------------+-------+-----------+-----------------------------------+
| per_page     | query | int       | Items Per Page, Maximum 100       |
+--------------+-------+-----------+-----------------------------------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "closed_issues": 0,
              "created_at": "2024-10-08T10:58:16+08:00",
              "description": "你好中国",
              "due_on": "2024-11-08",
              "number": 4914,
              "open_issues": 0,
              "repository_id": 4066481,
              "state": "active",
              "title": "你好中国",
              "updated_at": "2024-10-08T10:58:16+08:00",
              "url": "https://gitcode.com/dengmengmian/oneapi/milestones/1"
          }
      ]

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/milestones?state=open&sort=due_on&direction=asc&page=1&per_page=20&access_token=xxxx'


2. Get a Specific Milestone of a Repository
-------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/milestones/{number}``

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
| number\*     | path  | int       | Milestone ID (number)             |
+--------------+-------+-----------+-----------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "closed_issues": 0,
          "created_at": "2024-10-08T10:58:16+08:00",
          "description": "你好中国",
          "due_on": "2024-11-08",
          "number": 4914,
          "open_issues": 0,
          "repository_id": 4066481,
          "state": "active",
          "title": "你好中国",
          "updated_at": "2024-10-08T10:58:16+08:00",
          "url": "https://gitcode.com/dengmengmian/oneapi/milestones/1"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/milestones/4914?access_token=xxxx'


3. Delete a Specific Milestone of a Repository
----------------------------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/milestones/{number}``

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
| number\*     | path  | int       | Milestone ID (number)             |
+--------------+-------+-----------+-----------------------------------+


Response
~~~~~~~~

无


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request DELETE 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/milestones/4914?access_token=xxxx'


4. Update a Milestone of a Repository
-------------------------------------


Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}/milestones/{number}``

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
| number\*     | path  | int       | Milestone ID (number)             |
+--------------+-------+-----------+-----------------------------------+
| title\*      | body  | string    | Milestone Name                    |
+--------------+-------+-----------+-----------------------------------+
| state        | body  | string    | state: open, closed,              |
|              |       |           | all。Default: open                |
+--------------+-------+-----------+-----------------------------------+
| description  | body  | string    | Milestone Description             |
+--------------+-------+-----------+-----------------------------------+
| due_on\*     | body  | string    | Milestone due date                |
+--------------+-------+-----------+-----------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "closed_issues": 0,
          "created_at": "2024-10-08T10:58:16+08:00",
          "description": "你好中国",
          "due_on": "2024-11-08",
          "number": 4914,
          "open_issues": 0,
          "repository_id": 4066481,
          "state": "active",
          "title": "你好中国",
          "updated_at": "2024-10-08T10:58:16+08:00",
          "url": "https://gitcode.com/dengmengmian/oneapi/milestones/1"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request PATCH 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/milestones/4914?access_token=xxxx' \
      --data-raw '{
          "title": "title",
          "due_on": "2025-01-01"
      }'


5. Create a Milestone for a Repository
--------------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/milestones``

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
| title\*      | body  | string    | Milestone Name                    |
+--------------+-------+-----------+-----------------------------------+
| description  | body  | string    | Milestone Description             |
+--------------+-------+-----------+-----------------------------------+
| due_on\*     | body  | string    | Milestone due date                |
+--------------+-------+-----------+-----------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "closed_issues": 0,
          "created_at": "2024-10-08T10:58:16+08:00",
          "description": "你好中国",
          "due_on": "2024-11-08",
          "number": 4914,
          "open_issues": 0,
          "repository_id": 4066481,
          "state": "active",
          "title": "你好中国",
          "updated_at": "2024-10-08T10:58:16+08:00",
          "url": "https://gitcode.com/dengmengmian/oneapi/milestones/1"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request POST 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/milestones?access_token=xxxx' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "title": "title",
          "due_on": "2025-01-01"
      }'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/milestone/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
