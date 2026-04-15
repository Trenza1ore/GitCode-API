Release API Documentation
=========================


1. Update Repository Release
----------------------------

Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}/releases/{id}``

Parameters
~~~~~~~~~~

+--------------+--------------------------------+----------+-----------+
| Parameter    | Description                    | Type     | Data Type |
+==============+================================+==========+===========+
| access_token | personal access token          | formData | string    |
+--------------+--------------------------------+----------+-----------+
| owner\*      | Repository Ownership Path      | path     | string    |
|              | (Company, Organization, or     |          |           |
|              | Personal Path)                 |          |           |
+--------------+--------------------------------+----------+-----------+
| repo\*       | Repository Path(path)          | path     | string    |
+--------------+--------------------------------+----------+-----------+
| id\*         | release id                     | path     | Long      |
+--------------+--------------------------------+----------+-----------+
| tag_name\*   | Tag name                       | formData | string    |
+--------------+--------------------------------+----------+-----------+
| name\*       | Release name                   | formData | string    |
+--------------+--------------------------------+----------+-----------+
| body\*       | Release description            | formData | string    |
+--------------+--------------------------------+----------+-----------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "id": 1,
          "tag_name": "v1.0.217",
          "target_commitish": "930401b0dd58a809fce34da091b8aa3d6083cb33",
          "prerelease": false,
          "name": "release1 名称",
          "body": "release1 描述",
          "author": {
              "id": "26593",
              "login": "fenglonghui",
              "name": "龙辉",
              "avatar_url": "https://cdn-img.gitcode.com/de/af/61d5ea0ffc926181d235ba5a66f58dc51734500a1eda9b0d429d71300c20a149.png?time=1732777805505",
              "html_url": "https://gitcode.com/fenglonghui",
              "type": "User",
              "url": "https://api.gitcode.com/api/v5/users/fenglonghui"
          },
          "created_at": "2025-01-16T19:58:07+08:00",
          "assets": [
              {
                  "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.zip",
                  "name": "serde-v1.0.217.zip"
              },
              {
                  "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.tar.gz",
                  "name": "serde-v1.0.217.tar.gz"
              },
              {
                  "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.tar.bz2",
                  "name": "serde-v1.0.217.tar.bz2"
              },
              {
                  "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.tar",
                  "name": "serde-v1.0.217.tar"
              }
          ]
      }

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PATCH 'https://api.gitcode.com/api/v5/repos/rust-learning/serde/releases/1?access_token=***' \
      --header 'Content-Type: application/json' \
      --data-raw '{"tag_name":"v1.0.217", "name": "release1 名称", "body": "release1 描述"}'


2. Get Repository Release by Tag Name
-------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/releases/tags/{tag}``


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
| tag\*        | Tag name                          | path  | string    |
+--------------+-----------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "tag_name": "v1.0.217",
          "target_commitish": "930401b0dd58a809fce34da091b8aa3d6083cb33",
          "prerelease": false,
          "name": "learn serde",
          "body": "learn serde 描述",
          "author": {
              "id": "26593",
              "login": "fenglonghui",
              "name": "龙辉",
              "avatar_url": "https://cdn-img.gitcode.com/de/af/61d5ea0ffc926181d235ba5a66f58dc51734500a1eda9b0d429d71300c20a149.png?time=1732777805505",
              "html_url": "https://gitcode.com/fenglonghui",
              "type": "User",
              "url": "https://api.gitcode.com/api/v5/users/fenglonghui"
          },
          "created_at": "2025-01-16T19:58:07+08:00",
          "assets": [
              {
                  "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.zip",
                  "name": "serde-v1.0.217.zip"
              },
              {
                  "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.tar.gz",
                  "name": "serde-v1.0.217.tar.gz"
              },
              {
                  "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.tar.bz2",
                  "name": "serde-v1.0.217.tar.bz2"
              },
              {
                  "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.tar",
                  "name": "serde-v1.0.217.tar"
              }
          ]
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/repos/rust-learning/serde/releases/tags/v1.0.217?access_token=***'


3. Get All Releases of a Repository
-----------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/releases``


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


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "tag_name": "v1.0.217",
              "target_commitish": "930401b0dd58a809fce34da091b8aa3d6083cb33",
              "prerelease": false,
              "name": "release1 名称",
              "body": "release1 描述",
              "author": {
                  "id": "26593",
                  "login": "fenglonghui",
                  "name": "龙辉",
                  "avatar_url": "https://cdn-img.gitcode.com/de/af/61d5ea0ffc926181d235ba5a66f58dc51734500a1eda9b0d429d71300c20a149.png?time=1732777805505",
                  "html_url": "https://gitcode.com/fenglonghui",
                  "type": "User",
                  "url": "https://api.gitcode.com/api/v5/users/fenglonghui"
              },
              "created_at": "2025-01-16T19:58:07+08:00",
              "assets": [
                  {
                      "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.zip",
                      "name": "serde-v1.0.217.zip"
                  },
                  {
                      "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.tar.gz",
                      "name": "serde-v1.0.217.tar.gz"
                  },
                  {
                      "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.tar.bz2",
                      "name": "serde-v1.0.217.tar.bz2"
                  },
                  {
                      "browser_download_url": "https://gitcode.com/rust-learning/serde/-/archive/v1.0.217/serde-v1.0.217.tar",
                      "name": "serde-v1.0.217.tar"
                  }
              ]
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/repos/rust-learning/serde/releases?access_token=***'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/release/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
