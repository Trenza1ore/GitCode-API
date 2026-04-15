Tag API Documentation
=====================


1. Update a Label for a Repository
----------------------------------

Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}/labels/{original_name}``

+-----------------+-----------------------------+----------+-----------+
| Parameter       | Description                 | Type     | Data Type |
+=================+=============================+==========+===========+
| access_token\*  | personal access token       | query    | string    |
+-----------------+-----------------------------+----------+-----------+
| owner\*         | Repository Ownership Path   | path     | string    |
|                 | (Company, Organization, or  |          |           |
|                 | Personal Path)              |          |           |
+-----------------+-----------------------------+----------+-----------+
| repo\*          | Repository Path(path)       | path     | string    |
+-----------------+-----------------------------+----------+-----------+
| original_name\* | original name               | path     | string    |
+-----------------+-----------------------------+----------+-----------+
| name            | name                        | formData | string    |
+-----------------+-----------------------------+----------+-----------+
| color           | color                       | formData | string    |
+-----------------+-----------------------------+----------+-----------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "id": 12738100,
          "name": "list",
          "color": "#ED4014"
      }

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request PATCH 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/labels/bug?access_token=xxxx' \
      --form 'name="list"'


2. Get All Labels of a Repository
---------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/labels``

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| owner\*        | Repository Ownership Path       | path  | string    |
|                | (Company, Organization, or      |       |           |
|                | Personal Path)                  |       |           |
+----------------+---------------------------------+-------+-----------+
| repo\*         | Repository Path(path)           | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "id": 12738107,
              "name": "wontfix",
              "color": "#CCCCCC",
              "repository_id": 4066481
          },
          {
              "id": 12738106,
              "name": "question",
              "color": "#D876E3",
              "repository_id": 4066481
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/labels?access_token=xxxxx'


3. Create a Label for a Repository
----------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/labels``

+----------------+------------------------------+----------+-----------+
| Parameter      | Description                  | Type     | Data Type |
+================+==============================+==========+===========+
| access_token\* | personal access token        | query    | string    |
+----------------+------------------------------+----------+-----------+
| owner\*        | Repository Ownership Path    | path     | string    |
|                | (Company, Organization, or   |          |           |
|                | Personal Path)               |          |           |
+----------------+------------------------------+----------+-----------+
| repo\*         | Repository Path(path)        | path     | string    |
+----------------+------------------------------+----------+-----------+
| name\*         | new name                     | formData | string    |
+----------------+------------------------------+----------+-----------+
| color\*        | color, eg: #fff              | formData | string    |
+----------------+------------------------------+----------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "id": 12738109,
          "name": "测试1",
          "color": "#fff"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request POST 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/labels?access_token=xxxx' \
      --form 'name="测试"' \
      --form 'color="#fff"'


4. Delete a Label from a Repository
-----------------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/labels/{name}``

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| owner\*        | Repository Ownership Path       | path  | string    |
|                | (Company, Organization, or      |       |           |
|                | Personal Path)                  |       |           |
+----------------+---------------------------------+-------+-----------+
| repo\*         | Repository Path(path)           | path  | string    |
+----------------+---------------------------------+-------+-----------+
| name\*         | 标签名称                        | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

无


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request DELETE 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/labels/list?access_token=yuBy'


5. Delete All Labels of an Issue
--------------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{number}/labels``

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| owner\*        | Repository Ownership Path       | path  | string    |
|                | (Company, Organization, or      |       |           |
|                | Personal Path)                  |       |           |
+----------------+---------------------------------+-------+-----------+
| repo\*         | Repository Path(path)           | path  | string    |
+----------------+---------------------------------+-------+-----------+
| number\*       | issue number                    | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

无


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request DELETE 'https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{number}/labels?access_token=token'


6. Replace All Labels of an Issue
---------------------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{number}/labels``

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| owner\*        | Repository Ownership Path       | path  | string    |
|                | (Company, Organization, or      |       |           |
|                | Personal Path)                  |       |           |
+----------------+---------------------------------+-------+-----------+
| repo\*         | Repository Path(path)           | path  | string    |
+----------------+---------------------------------+-------+-----------+
| number\*       | issue number                    | path  | string    |
+----------------+---------------------------------+-------+-----------+
| body\*         | labels，eg: [“feat”, “bug”]     | body  | array     |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

无


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request PUT 'https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{number}/labels?access_token=token'\
      --header 'Content-Type: application/json' \
      --data-raw '["feat", "bug"]'


7. Get All Labels of an Enterprise(v5)
--------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/enterprises/{enterprise}/labels``

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| enterprise\*   | Repository Ownership Path       | path  | string    |
|                | (Company, Organization, or      |       |           |
|                | Personal Path)                  |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "id": 471,
              "name": "aaaaa",
              "color": "#2865E0",
              "created_at": "2024-11-22T11:25:36.769+08:00",
              "updated_at": "2024-11-22T11:25:36.769+08:00"
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/enterprises/xiaogang_test/labels?access_token=token'


8. Get the List of Labels for an Enterprise(v8)
-----------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v8/enterprises/{enterprise}/labels``

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| enterprise\*   | Repository Ownership Path       | path  | string    |
|                | (Company, Organization, or      |       |           |
|                | Personal Path)                  |       |           |
+----------------+---------------------------------+-------+-----------+
| search         | keywords                        | query | string    |
+----------------+---------------------------------+-------+-----------+
| direction      | asc/desc                        | query | string    |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number             | query | string    |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum 100     | query | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "id": 382218,
              "name": "bug",
              "color": "#e03529"
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v8/enterprises/xiaogang_test/labels?access_token=token'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/labels/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
