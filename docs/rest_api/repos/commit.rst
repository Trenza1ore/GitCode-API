Commit API Documentation
========================


1. Get All Commits of a Repository
----------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/commits``

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
| sha          | query | string    | Starting SHA value of the commit  |
+--------------+-------+-----------+-----------------------------------+
| path         | query | string    | Commits containing the specified  |
|              |       |           | file                              |
+--------------+-------+-----------+-----------------------------------+
| author       | query | string    | author username/login             |
+--------------+-------+-----------+-----------------------------------+
| since        | query | string    | since                             |
+--------------+-------+-----------+-----------------------------------+
| until        | query | string    | until                             |
+--------------+-------+-----------+-----------------------------------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "url": "https://api.gitcode.com/api/v5/repos/mactribe/test02/commits/66a12f572722ebe2cad44f44d48e253a0f027e09",
              "sha": "66a12f572722ebe2cad44f44d48e253a0f027e09",
              "html_url": "https://test.gitcode.net/mactribe/test02/commits/detail/66a12f572722ebe2cad44f44d48e253a0f027e09",
              "comments_url": "https://api.gitcode.com/api/v5/repos/mactribe/test02/commits/66a12f572722ebe2cad44f44d48e253a0f027e09/comments",
              "commit": {
                  "author": {
                      "date": "2024-09-25T08:14:59+08:00",
                      "email": "my@dengmengmian.com"
                  },
                  "committer": {
                      "date": "2024-09-25T08:14:59+08:00",
                      "email": "my@dengmengmian.com"
                  },
                  "tree": {
                      "sha": "6214a5921eda7f5148f249587b74201d5946a6d4",
                      "url": "https://api.gitcode.com/api/v5/repos/mactribe/test02/git/trees/6214a5921eda7f5148f249587b74201d5946a6d4"
                  },
                  "message": "feat:所有issue number 都改为 string Type"
              },
              "author": {
                  "email": "my@dengmengmian.com",
                  "login": "dengmengmian(麻凡)",
                  "type": "User"
              },
              "committer": {
                  "date": "2024-09-25T08:14:59+08:00",
                  "email": "my@dengmengmian.com",
                  "type": "User"
              },
              "parents": [
                  {
                      "sha": "0c41318014c472534a2abc2e0aa498fd49d046f1",
                      "url": "https://api.gitcode.com/api/v5/repos/mactribe/test02/commits/0c41318014c472534a2abc2e0aa498fd49d046f1"
                  }
              ]
          },
      ]

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/repos/mactribe/test02/commits?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data-raw '{}'


2. Get a Specific Commit of a Repository
----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/commits/{sha}``

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
| sha\*          | path  | string    | Commit SHA value or branch name |
+----------------+-------+-----------+---------------------------------+
| show_diff      | query | boolean   | Default is false; when true,    |
|                |       |           | returns the files field, which  |
|                |       |           | includes up to 100 changed file |
|                |       |           | names in the local commit       |
+----------------+-------+-----------+---------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "url": "https://gitcode.com/api/v5/repos/daming_1/zhu_di/commits/7ffc0a0deb709143f6be12a55e218fab9233ca37",
          "sha": "7ffc0a0deb709143f6be12a55e218fab9233ca37",
          "html_url": "https://gitcode.com/daming_1/zhu_di/commit/7ffc0a0deb709143f6be12a55e218fab9233ca37",
          "comments_url": "https://gitcode.com/api/v5/repos/daming_1/zhu_di/commits/7ffc0a0deb709143f6be12a55e218fab9233ca37/comments",
          "commit": {
              "author": {
                  "name": "占分",
                  "date": "2024-04-14T07:25:11+00:00",
                  "email": "7543745+centking@user.noreply.gitcode.com"
              },
              "committer": {
                  "name": "Gitee",
                  "date": "2024-04-14T07:25:11+00:00",
                  "email": "noreply@gitcode.com"
              },
              "message": "提交信息测试"
          },
          "stats": {
              "additions": 1,
              "deletions": 1,
              "total": 2
          },
            "files": [
              {
                   "filename": "pom.xml",
                  "raw_url": "https://raw.gitcode.com/test-owner/test-repo/raw/b0e267d8bbed9b568623528c216f8f8489689a61/pom.xml",
                  "content_url": "https://gitcode.com/test-owner/test-repo/blob/b0e267d8bbed9b568623528c216f8f8489689a61/pom.xml"
              }
          ]
      }


Demo
~~~~

.. container:: highlight

   .. code:: text


      curl --location 'https://api.gitcode.com/api/v5/repos/test-owner/test-repo/commits/786eae93d33ca08fae6962b2b04e54f40bbe3b3c?access_token=token&show_diff=true'


3. Compare Commits
------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/compare/{base}...{head}``

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
| base\*       | path  | string    | Comparison starting point: commit |
|              |       |           | SHA, branch name, or tag name     |
+--------------+-------+-----------+-----------------------------------+
| head\*       | path  | string    | Comparison ending point: commit   |
|              |       |           | SHA, branch name, or tag name     |
+--------------+-------+-----------+-----------------------------------+
| straight     | query | boolean   | Whether to perform a direct       |
|              |       |           | comparison. Default is false      |
+--------------+-------+-----------+-----------------------------------+
| suffix       | query | string    | Filter files by suffix, e.g.,     |
|              |       |           | ``.txt``. Only affects ``files``  |
+--------------+-------+-----------+-----------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "base_commit": {
              "url": "https://api.gitcode.com/api/v5/repos/owner-test/secure-issue/commits/17922544024484084e2b6218eb0d46d76f354ffa",
              "sha": "17922544024484084e2b6218eb0d46d76f354ffa",
              "html_url": "https://test.gitcode.net/owner-test/secure-issue/commit/17922544024484084e2b6218eb0d46d76f354ffa",
              "comments_url": "https://test.gitcode.net/api/v5/repos/owner-test/secure-issue/commits/17922544024484084e2b6218eb0d46d76f354ffa/comments",
              "commit": {
                  "author": {
                      "name": "malongge5",
                      "date": "2024-08-13T11:34:35Z",
                      "email": "malongge5@noreply.gitcode.com"
                  },
                  "committer": {
                      "name": "malongge5",
                      "date": "2024-08-13T11:34:35Z",
                      "email": "malongge5@noreply.gitcode.com"
                  },
                  "tree": {
                      "sha": "4e12f62b7fe2f78cb7c1b088e8f7e797a8c898a3",
                      "url": "https://api.gitcode.com/repos/owner-test/secure-issue/git/trees/4e12f62b7fe2f78cb7c1b088e8f7e797a8c898a3"
                  },
                  "message": "new: 新增文件 test.py \n "
              },
              "author": {
                  "name": "malongge5",
                  "id": 953,
                  "login": "malongge5",
                  "type": "User"
              },
              "committer": {
                  "name": "malongge5",
                  "id": 953,
                  "login": "malongge5",
                  "type": "User"
              },
              "parents": [
                  {
                      "sha": "7ea40eef5f96c3f263f17438b294a6ea9b771cc5",
                      "url": "https://api.gitcode.com/api/v5/repos/owner-test/secure-issue/commits/7ea40eef5f96c3f263f17438b294a6ea9b771cc5"
                  }
              ]
          },
          "merge_base_commit": {
              "url": "https://api.gitcode.com/api/v5/repos/owner-test/secure-issue/commits/17922544024484084e2b6218eb0d46d76f354ffa",
              "sha": "17922544024484084e2b6218eb0d46d76f354ffa",
              "html_url": "https://test.gitcode.net/owner-test/secure-issue/commit/17922544024484084e2b6218eb0d46d76f354ffa",
              "comments_url": "https://test.gitcode.net/api/v5/repos/owner-test/secure-issue/commits/17922544024484084e2b6218eb0d46d76f354ffa/comments",
              "commit": {
                  "author": {
                      "name": "malongge5",
                      "date": "2024-08-13T11:34:35Z",
                      "email": "malongge5@noreply.gitcode.com"
                  },
                  "committer": {
                      "name": "malongge5",
                      "date": "2024-08-13T11:34:35Z",
                      "email": "malongge5@noreply.gitcode.com"
                  },
                  "tree": {
                      "sha": "4e12f62b7fe2f78cb7c1b088e8f7e797a8c898a3",
                      "url": "https://api.gitcode.com/repos/owner-test/secure-issue/git/trees/4e12f62b7fe2f78cb7c1b088e8f7e797a8c898a3"
                  },
                  "message": "new: 新增文件 test.py \n "
              },
              "author": {
                  "name": "malongge5",
                  "id": 953,
                  "login": "malongge5",
                  "type": "User"
              },
              "committer": {
                  "name": "malongge5",
                  "id": 953,
                  "login": "malongge5",
                  "type": "User"
              },
              "parents": [
                  {
                      "sha": "7ea40eef5f96c3f263f17438b294a6ea9b771cc5",
                      "url": "https://api.gitcode.com/api/v5/repos/owner-test/secure-issue/commits/7ea40eef5f96c3f263f17438b294a6ea9b771cc5"
                  }
              ]
          },
          "commits": [
              {
                  "sha": "97fd5a05e18bcd5b633a279fd7d395784d272321",
                  "commit": {
                      "author": {
                          "name": "malongge5",
                          "date": "2024-09-09T07:29:23Z",
                          "email": "malongge5@noreply.gitcode.com"
                      },
                      "committer": {
                          "name": "malongge5",
                          "date": "2024-09-09T07:29:23Z",
                          "email": "malongge5@noreply.gitcode.com"
                      },
                      "message": "new: 新增文件 bbb.rs \n "
                  },
                  "author": {
                      "name": "malongge5",
                      "id": 953,
                      "login": "malongge5"
                  },
                  "committer": {
                      "name": "malongge5",
                      "id": 953,
                      "login": "malongge5"
                  }
              }
          ],
          "files": [
              {
                  "sha": "6533e5c4585eb91faa9331b8de6b22f9ff31d387",
                  "filename": "bbb.rs",
                  "status": "added",
                  "additions": 3,
                  "deletions": 0,
                  "changes": 3,
                  "blob_url": "https://test.gitcode.net/owner-test/secure-issue/blob/6533e5c4585eb91faa9331b8de6b22f9ff31d387/bbb.rs",
                  "raw_url": "https://test.gitcode.net/owner-test/secure-issue/raw/6533e5c4585eb91faa9331b8de6b22f9ff31d387/bbb.rs",
                  "patch": "@@ -0,0 +1,3 @@\n+\n+\n+println!(\"hello\")\n\\ No newline at end of file\n",
                  "truncated": false
              }
          ],
          "truncated": false
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com//api/v5/repos/owner-test/secure-issue/compare/17922544024484084e2b6218eb0d46d76f354ffa...97fd5a05e18bcd5b633a279fd7d395784d272321?access_token=xxxx'


4. Create a Commit Comment
--------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/commits/{sha}/comments``


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
| sha\*          | path  | string    | commit id                       |
+----------------+-------+-----------+---------------------------------+
| body\*         | body  | string    | Comment Content                 |
+----------------+-------+-----------+---------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "id":"12312sadsa",
          "body":"content",
          "created_at": "2024-03-28T11:19:33+08:00",
          "updated_at": "2024-03-28T11:19:33+08:00"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/commits/7b8ee8f1046519582a2765e55c2b91288dd197de/comments?access_token' \
      --header 'Content-Type: application/json' \
      --data '{
          "body":"1111"
      }'


5. Delete a Commit Comment
--------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/comments/{id}``


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
| id\*           | path  | string    | the ID of a comment             |
+----------------+-------+-----------+---------------------------------+


Response
~~~~~~~~

无


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/comments/1492393?access_token=?'


6. Get Commit Comments of a Repository
--------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/comments``


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
| page           | query | integer   | Current Page Number             |
+----------------+-------+-----------+---------------------------------+
| per_page       | query | integer   | Items Per Page, Maximum 100     |
+----------------+-------+-----------+---------------------------------+
| order          | query | string    | Sorting Order:                  |
|                |       |           | asc(default),desc               |
+----------------+-------+-----------+---------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "body": "",
          "created_at": "2024-11-06T09:43:23+08:00",
          "id": 1492393,
          "target": {},
          "updated_at": "2024-11-06T15:18:04+08:00",
          "user": {
              "id": 496,
              "login": "xiaogang",
              "name": "xiaogang",
              "type": "User"
          }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/comments?access_token=?'


7. Get a Specific Commit Comment of a Repository
------------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/comments/{id}``


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
| id\*           | path  | string    | the ID of a comment             |
+----------------+-------+-----------+---------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "body": "阿福时间看风景",
          "created_at": "2024-11-06T09:43:23+08:00",
          "id": 1492393,
          "target": {},
          "updated_at": "2024-11-06T15:18:04+08:00",
          "user": {
              "id": 496,
              "login": "xiaogang",
              "name": "xiaogang",
              "type": "User"
          }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/comments/1507446?access_token=?'


8. Update a Commit Comment
--------------------------


Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}/comments/{id}``


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
| id\*           | path  | string    | the ID of a comment             |
+----------------+-------+-----------+---------------------------------+
| body\*         | body  | string    | Comment Content                 |
+----------------+-------+-----------+---------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "body": "",
          "created_at": "2024-11-06T09:43:23+08:00",
          "id": 1492393,
          "target": {},
          "updated_at": "2024-11-14T18:44:53+08:00",
          "user": {
              "id": 496,
              "login": "xiaogang",
              "name": "xiaogang",
              "type": "User"
          }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PATCH 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/comments/1507446?access_token=?' \
      --header 'Content-Type: application/json' \
      --data '{
          "body":"body"
      }'


9. Get Code Contribution Statistics
-----------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/{owner}/{repo}/repository/commit_statistics``


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
| branch_name\*  | query | string    | branch name                     |
+----------------+-------+-----------+---------------------------------+
| author         | query | string    | author username                 |
+----------------+-------+-----------+---------------------------------+
| only_self      | query | Boolean   | only self                       |
+----------------+-------+-----------+---------------------------------+
| since          | query | string    | since                           |
+----------------+-------+-----------+---------------------------------+
| until          | query | string    | until                           |
+----------------+-------+-----------+---------------------------------+

**Note: author takes precedence over only_self.**


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "commits": [
              {
                  "author_name": "tester",
                  "date": "2024-11-12"
              },
              ... ...,
              {
                  "author_name": "tester",
                  "date": "2024-01-15"
              }
          ],
          "statistics": [
              {
                  "project_id": 1359,
                  "branch": "main",
                  "user_name": "tester",
                  "nick_name": "测试",
                  "add_lines": 4370,
                  "delete_lines": 351,
                  "commit_count": 123
              }
          ],
          "total": 1
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/gitcode-repo/hub-service/repository/commit_statistics?branch_name=main&access_token=your_token&only_self=true&since=2024-11-11%2010%3A45%3A53'


10. Get a Single Commit Comment
-------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/commits/{ref}/comments``


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
| ref\*          | path  | string    | commit sha                      |
+----------------+-------+-----------+---------------------------------+
| page           | query | integer   | Current Page Number             |
+----------------+-------+-----------+---------------------------------+
| per_page       | query | integer   | Items Per Page, Maximum 100     |
+----------------+-------+-----------+---------------------------------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "body": "11111",
              "created_at": "2024-11-19T11:22:50+08:00",
              "id": 13837749,
              "updated_at": "2024-11-19T11:22:50+08:00",
              "user": {
                  "id": 173794,
                  "login": "xiaogang",
                  "name": "肖刚",
                  "type": "User"
              }
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/comments/1507446?access_token=?'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/commit/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
