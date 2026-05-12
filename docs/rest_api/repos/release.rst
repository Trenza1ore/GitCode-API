Release API Documentation
=========================

1. Create Repository Release
----------------------------

Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/releases``

Parameters
~~~~~~~~~~

+------------------+-------------------------------------------+----------+-----------+
| Parameter        | Description                               | Type     | Data Type |
+==================+===========================================+==========+===========+
| owner\*          | Repository ownership path (company,       | path     | string    |
|                  | organization, or personal path).          |          |           |
+------------------+-------------------------------------------+----------+-----------+
| repo\*           | Repository path.                          | path     | string    |
+------------------+-------------------------------------------+----------+-----------+
| access_token\*   | User access token (personal access        | query    | string    |
|                  | token).                                   |          |           |
+------------------+-------------------------------------------+----------+-----------+
| tag_name\*       | Tag name for the release.                 | formData | string    |
+------------------+-------------------------------------------+----------+-----------+
| name\*           | Release title.                            | formData | string    |
+------------------+-------------------------------------------+----------+-----------+
| body\*           | Release description.                      | formData | string    |
+------------------+-------------------------------------------+----------+-----------+
| target_commitish | Branch name or commit SHA. If the tag     | formData | string    |
|                  | is missing, pass this to create it;       |          |           |
|                  | if omitted, use default branch tip.       |          |           |
+------------------+-------------------------------------------+----------+-----------+
| release_status   | Release status: ``pre`` (pre-release)     | formData | string    |
|                  | or ``latest`` (latest release).           |          |           |
+------------------+-------------------------------------------+----------+-----------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "tag_name": "v1.0.218",
        "target_commitish": "930401b0dd58a809fce34da091b8aa3d6083cb33",
        "prerelease": false,
        "name": "Serde 1.0.218",
        "body": "Patch release: dependency and docs updates.",
        "author": {
            "id": "26593",
            "login": "fenglonghui",
            "name": "龙辉",
            "avatar_url": "https://cdn-img.gitcode.com/de/af/61d5ea0ffc926181d235ba5a66f58dc51734500a1eda9b0d429d71300c20a149.png?time=1732777805505",
            "html_url": "https://gitcode.com/fenglonghui",
            "type": "User",
            "url": "https://api.gitcode.com/api/v5/users/fenglonghui"
        },
        "created_at": "2026-05-01T14:22:11+08:00",
        "assets": [
            {
                "browser_download_url": "https://gitcode.com/rust-learning/serde/-/releases/v1.0.218/downloads/checksums.txt",
                "name": "checksums.txt",
                "type": "text/plain"
            }
        ],
        "release_status": "latest"
      }

Demo
~~~~

.. container:: highlight

   .. code:: text

        curl --location --request POST \
        'https://api.gitcode.com/api/v5/repos/rust-learning/serde/releases?access_token=***' \
        --header 'Content-Type: application/json' \
        --header 'Accept: application/json' \
        --data-raw '{
          "tag_name": "v1.0.218",
          "name": "Serde 1.0.218",
          "body": "Patch release: dependency and docs updates.",
          "target_commitish": "main",
          "release_status": "latest"
        }'


2. Update Repository Release
----------------------------

Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}/releases/{tag}``

Parameters
~~~~~~~~~~

+--------------+--------------------------------+----------+-----------+
| Parameter    | Description                    | Type     | Data Type |
+==============+================================+==========+===========+
| access_token | personal access token          | query    | string    |
+--------------+--------------------------------+----------+-----------+
| owner\*      | Repository Ownership Path      | path     | string    |
|              | (Company, Organization, or     |          |           |
|              | Personal Path)                 |          |           |
+--------------+--------------------------------+----------+-----------+
| repo\*       | Repository Path(path)          | path     | string    |
+--------------+--------------------------------+----------+-----------+
| tag\*        | Tag name                       | path     | string    |
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

      curl --location --request PATCH 'https://api.gitcode.com/api/v5/repos/rust-learning/serde/releases/v1.0.217?access_token=***' \
      --header 'Content-Type: application/json' \
      --data-raw '{"tag_name":"v1.0.217", "name": "release1 名称", "body": "release1 描述"}'


3. Get URL and Request Headers for Release Attachment Upload
------------------------------------------------------------

Returns a pre-signed object storage URL and a header map. Upload the attachment with HTTP **PUT** to the returned ``url``, sending the returned ``headers`` unchanged (Huawei OBS-style fields such as ``x-obs-meta-project-id``).

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/releases/{tag}/upload_url``

Parameters
~~~~~~~~~~

+------------------+-------------------------------------------+-------+-----------+
| Parameter        | Description                               | Type  | Data Type |
+==================+===========================================+=======+===========+
| owner\*          | Repository ownership path (company,       | path  | string    |
|                  | organization, or personal path).          |       |           |
+------------------+-------------------------------------------+-------+-----------+
| repo\*           | Repository path.                          | path  | string    |
+------------------+-------------------------------------------+-------+-----------+
| tag\*            | Tag name for the release.                 | path  | string    |
+------------------+-------------------------------------------+-------+-----------+
| access_token\*   | User access token (personal access        | query | string    |
|                  | token).                                   |       |           |
+------------------+-------------------------------------------+-------+-----------+
| file_name\*      | Name of the file to upload.               | query | string    |
+------------------+-------------------------------------------+-------+-----------+

Response
~~~~~~~~

The JSON body contains:

- ``url`` — Pre-signed URL; upload bytes with **PUT** to this URL (per upstream API docs).
- ``headers`` — Headers that must accompany that **PUT** (for example ``x-obs-meta-project-id``, ``x-obs-acl``, ``x-obs-callback``, ``Content-Type``).

.. container:: highlight

   .. code:: text

      {
        "url": "https://gitcode-release.obs.cn-south-1.myhuaweicloud.com/v1/buckets/rg-abc123/objects/serde-v1.0.217-notes.pdf?AWSAccessKeyId=DUMMYKEY&Expires=1714521600&Signature=dummySignatureValue%3D",
        "headers": {
            "x-obs-meta-project-id": "4066481",
            "x-obs-acl": "public-read",
            "x-obs-callback": "https://api.gitcode.com/api/v5/internal/releases/attach-callback",
            "Content-Type": "application/pdf"
        }
      }

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET \
      'https://api.gitcode.com/api/v5/repos/rust-learning/serde/releases/v1.0.217/upload_url?access_token=***&file_name=release-notes.pdf' \
      --header 'Accept: application/json'


4. Get All Releases of a Repository
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


5. Get the Latest Release of a Repository
-----------------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/releases/latest``

Parameters
~~~~~~~~~~

+----------------+-------------------------------------------+-------+-----------+
| Parameter      | Description                               | Type  | Data Type |
+================+===========================================+=======+===========+
| owner\*        | Repository ownership path (company,       | path  | string    |
|                | organization, or personal path).          |       |           |
+----------------+-------------------------------------------+-------+-----------+
| repo\*         | Repository path.                          | path  | string    |
+----------------+-------------------------------------------+-------+-----------+
| access_token\* | User access token (personal access        | query | string    |
|                | token).                                   |       |           |
+----------------+-------------------------------------------+-------+-----------+
| type           | Release selection type: ``updated``       | query | string    |
|                | (last updated) or ``latest``.             |       |           |
+----------------+-------------------------------------------+-------+-----------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

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
          ],
          "release_status": "latest"
      }

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/repos/rust-learning/serde/releases/latest?access_token=***&type=latest' \
      --header 'Accept: application/json'


6. Get Single Release of a Repository
-------------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/releases/{tag}``

Parameters
~~~~~~~~~~

+-------------------+-------------------------------------------+-------+-----------+
| Parameter         | Description                               | Type  | Data Type |
+===================+===========================================+=======+===========+
| owner\*           | Repository ownership path (company,       | path  | string    |
|                   | organization, or personal path).          |       |           |
+-------------------+-------------------------------------------+-------+-----------+
| repo\*            | Repository path.                          | path  | string    |
+-------------------+-------------------------------------------+-------+-----------+
| tag\*             | Tag name.                                 | path  | string    |
+-------------------+-------------------------------------------+-------+-----------+
| access_token\*    | User access token (personal access        | query | string    |
|                   | token).                                   |       |           |
+-------------------+-------------------------------------------+-------+-----------+
| temp_download_url | Whether to return temporary download      | query | string    |
|                   | URLs for source packages and              |       |           |
|                   | attachments. Defaults to ``false``.       |       |           |
+-------------------+-------------------------------------------+-------+-----------+

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
          ],
          "release_status": "latest"
      }

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/repos/rust-learning/serde/releases/v1.0.217?access_token=***&temp_download_url=false' \
      --header 'Accept: application/json'


7. Get Repository Release by Tag Name
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

8. Download Release Attachment from a Repository
------------------------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/releases/{tag}/attach_files/{file_name}/download``

Parameters
~~~~~~~~~~

+----------------+-------------------------------------------+-------+-----------+
| Parameter      | Description                               | Type  | Data Type |
+================+===========================================+=======+===========+
| owner\*        | Repository ownership path (company,       | path  | string    |
|                | organization, or personal path).          |       |           |
+----------------+-------------------------------------------+-------+-----------+
| repo\*         | Repository path.                          | path  | string    |
+----------------+-------------------------------------------+-------+-----------+
| tag\*          | Tag name.                                 | path  | string    |
+----------------+-------------------------------------------+-------+-----------+
| file_name\*    | Attachment name.                          | path  | string    |
+----------------+-------------------------------------------+-------+-----------+
| access_token\* | User access token (personal access        | query | string    |
|                | token).                                   |       |           |
+----------------+-------------------------------------------+-------+-----------+

Response
~~~~~~~~

Returns the attachment bytes with a ``*/*`` response content type.

.. container:: highlight

   .. code:: text

      {}

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET \
      'https://api.gitcode.com/api/v5/repos/rust-learning/serde/releases/v1.0.217/attach_files/checksums.txt/download?access_token=***' \
      --header 'Accept: */*'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/release/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
.. Well, that page is not updated, so I'll have to edit by hand QAQ
