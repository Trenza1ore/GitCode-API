Branch API Documentation
========================


1. Get All Branches of a Repository
-----------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/branches``

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
| sort           | Sorting Fields name/updated     | query | string    |
+----------------+---------------------------------+-------+-----------+
| direction      | asc/desc                        | quey  | string    |
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
          "name": "main",
          "commit": {
            "commit": {
              "author": {
                "name": "Lzm_0916",
                "date": "2024-04-16T08:41:20.000Z",
                "email": "Lzm_0916@noreply.gitcode.com"
              },
              "committer": {
                "name": "Lzm_0916",
                "date": "2024-04-16T08:41:20.000Z",
                "email": "Lzm_0916@noreply.gitcode.com"
              },
              "message": "提交测试类"
            },
            "sha": "1d45587145552af003cd32cc6fde9ac9d9e5fd42",
            "url": "https://test.gitcode.net/api/v5/repos/Lzm_0916/test/commits/1d45587145552af003cd32cc6fde9ac9d9e5fd42"
          },
          "protected": true
        }
      ]

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'http://api.gitcode.com/api/v5/repos/dengmengmian/test03/branches?access_token={your-token}' \


2. Create a Branch
------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/branches``


Parameters
~~~~~~~~~~

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
| refs\*         | Branch Starting Point Name,     | body  | string    |
|                | Default: main                   |       |           |
+----------------+---------------------------------+-------+-----------+
| branch_name\*  | new branch                      | body  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "name": "gitcode",
        "commit": {
          "commit": {
            "author": {
              "name": "dengmengmian",
              "date": "2024-09-10T08:29:18Z",
              "email": "dengmengmian@noreply.gitcode.com"
            },
            "committer": {
              "name": "dengmengmian",
              "date": "2024-09-10T08:29:18Z",
              "email": "dengmengmian@noreply.gitcode.com"
            },
            "message": "test"
          },
          "sha": "1af35823b8bbcaf68776cd6cb0ecbf88cfdec905",
          "url": "https://test.gitcode.net/api/v5/repos/dengmengmian/test03/commits/1af35823b8bbcaf68776cd6cb0ecbf88cfdec905"
        },
        "protected": false
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'http://api.gitcode.com/api/v5/repos/dengmengmian/test03/branches?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "refs": "main",
          "branch_name": "gitcode"
      }'


3. Get a Branch
---------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/branches/{branch}``


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
| branch\*       | branch                          | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "name": "dev",
        "commit": {
          "id": "b6d44deb0ca73d7a50916d0fea02c72edd6c924e",
          "message": "\ndev新增文件\n\nCreated-by: csdntest13\nAuthor-id: 494\nMR-id: 68629\nCommit-by: csdntest13\nMerged-by: csdntest13\nE2E-issues: \nDescription: 提交信息\n\nSee merge request: One/One!56",
          "parent_ids": [
            "13956ffeb5e5e1ce60c2ed91d3e579fc50b1f167",
            "3e42dcb9c09b39972c65536dad71651322470f28"
          ],
          "authored_date": "2024-04-15T14:38:50.000Z",
          "author_name": "csdntest13",
          "author_iam_id": null,
          "author_email": "csdntest13@noreply.gitcode.com",
          "author_user_name": null,
          "committed_date": "2024-04-15T14:38:50.000Z",
          "committer_name": "csdntest13",
          "committer_email": "csdntest13@noreply.gitcode.com",
          "committer_user_name": null,
          "open_gpg_verified": null,
          "verification_status": null,
          "gpg_primary_key_id": null,
          "short_id": "b6d44deb",
          "created_at": "2024-04-15T14:38:50.000Z",
          "title": "merge refs/merge-requests/56/head into dev",
          "author_avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
          "committer_avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
          "relate_url": null
        },
        "merged": false,
        "protected": false,
        "developers_can_push": false,
        "developers_can_merge": false,
        "can_push": true,
        "default": false
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'http://api.gitcode.com/api/v5/repos/dengmengmian/test03/branches/main?access_token={your-token}' \


4. Create a Protected Branch Rule
---------------------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/branches/setting/new``


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
| wildcard\*     | wildcard                        | body  | string    |
+----------------+---------------------------------+-------+-----------+
| pusher\*       | pusher: develop, admin,         | body  | string    |
|                | empty(Prohibit Pushes from      |       |           |
|                | Anyone)                         |       |           |
+----------------+---------------------------------+-------+-----------+
| merger\*       | merger: develop, admin,         | body  | string    |
|                | empty(Prohibit merge from       |       |           |
|                | Anyone)                         |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      HTTP status 200 No Content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/branches/setting/new'?access_token={your-token} \
      --header 'Content-Type: application/json' \
      --data '{
          "wildcard":"dev12",
          "pusher":"zhanghq2;xiaogang;admin",
          "merger":"zhanghq2;xiaogang;admin"
      }'


5. Delete a Protected Branch Rule
---------------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/branches/{wildcard}/setting'``


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
| wildcard\*     | wildcard                        | path  | string    |
+----------------+---------------------------------+-------+-----------+

.. container:: highlight

   .. code:: text

      HTTP status 200 No Content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/repos/tiandi/YanF4/branches/test/setting?access_token={your-token}' \


6. Get List of Protected Branch Rules
-------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/protect_branches``


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


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "name": "main",
          "updated_at": "2024-09-18T10:15:48.471+08:00",
          "push_users": [],
          "merge_users": [],
          "merged": false,
          "developers_can_push": false,
          "developers_can_merge": false,
          "committer_can_push": false,
          "committer_can_merge": false,
          "master_can_push": true,
          "master_can_merge": true,
          "maintainer_can_push": true,
          "maintainer_can_merge": true,
          "owner_can_push": true,
          "owner_can_merge": true,
          "no_one_can_push": false,
          "no_one_can_merge": false
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/test-org/test-repo/protect_branches?access_token=token'


7. Update a Protected Branch Rule
---------------------------------


Request
~~~~~~~

``PUT /repos/{owner}/{repo}/branches/{wildcard}/setting``


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
| wildcard\*     | protected branch wildcard       | path  | string    |
+----------------+---------------------------------+-------+-----------+
| pusher\*       | pusher: develop, admin,         | body  | string    |
|                | empty(Prohibit Pushes from      |       |           |
|                | Anyone)                         |       |           |
+----------------+---------------------------------+-------+-----------+
| merger\*       | merger: develop, admin,         | body  | string    |
|                | empty(Prohibit merge from       |       |           |
|                | Anyone)                         |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

无


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/branches/dev4/setting?access_token=token' \
      --header 'Content-Type: application/json' \
      --data '{
          "pusher":"develop",
          "merger":"develop"
      }'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/branch/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
