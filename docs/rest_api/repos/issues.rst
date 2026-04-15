Issues API Documentation
========================


1. Create an Issue
------------------

Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/issues``

Parameters
~~~~~~~~~~

+----------------+------------------------------+----------+-----------+
| Parameter      | Description                  | Type     | Data Type |
+================+==============================+==========+===========+
| access_token\* | personal access token        | query    | string    |
+----------------+------------------------------+----------+-----------+
| owner\*        | Repository Owner Path        | path     | string    |
|                | (Organization or User Path)  |          |           |
+----------------+------------------------------+----------+-----------+
| repo\*         | Repository Path              | formData | string    |
+----------------+------------------------------+----------+-----------+
| title\*        | title                        | formData | string    |
+----------------+------------------------------+----------+-----------+
| body           | Issue Description            | formData | string    |
+----------------+------------------------------+----------+-----------+
| assignee       | assignee                     | formData | string    |
+----------------+------------------------------+----------+-----------+
| milestone      | milestone ID                 | formData | int       |
+----------------+------------------------------+----------+-----------+
| labels         | Comma-separated list of      | formData | string    |
|                | label names.                 |          |           |
+----------------+------------------------------+----------+-----------+
| security_hole  | Whether the issue is private | formData | string    |
|                | (default is false)           |          |           |
+----------------+------------------------------+----------+-----------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 152642,
        "html_url": "https://test.gitcode.net/dengmengmian/test01/issues/15",
        "number": 15,
        "state": "opened",
        "title": "半月据",
        "body": "节油料被引系活力级少本化段维家住实。常气前步证时第样日所阶效温界到量。个导土机技亲布接增论始高世收圆流级集。此般区才听党机达两收文斗公加白。代军前分写第图美市与道及间。",
        "user": {
          "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
          "events_url": null,
          "followers_url": null,
          "following_url": null,
          "gists_url": null,
          "html_url": "https://test.gitcode.net/dengmengmian",
          "id": "661ce4eab470b1430d456154",
          "login": "dengmengmian",
          "member_role": null,
          "name": "麻凡_",
          "organizations_url": null,
          "received_events_url": null,
          "remark": null,
          "repos_url": null,
          "starred_url": null,
          "subscriptions_url": null,
          "type": null,
          "url": null
        },
        "assignee": null,
        "repository": {
          "id": 152642,
          "full_name": "dengmengmian/test01",
          "path": "test01",
          "name": "test01",
          "description": "",
          "created_at": "2024-04-18T14:35:15.479+08:00",
          "updated_at": "2024-04-18T14:35:15.479+08:00"
        },
        "created_at": "2024-04-18T14:35:15.479+08:00",
        "updated_at": "2024-04-18T14:35:15.479+08:00",
        "finished_at": null,
        "labels": [
          {
            "id": 382379,
            "name": "enim",
            "color": "#428BCA"
          },
          {
            "id": 382378,
            "name": "proident",
            "color": "#428BCA"
          },
          {
            "id": 382377,
            "name": "qui",
            "color": "#428BCA"
          }
        ],
        "stage": "New",
        "severity": "Major"
      }

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request 'https://api.gitcode.com/api/v5/repos/xiaogang_test/issues?access_token=token' \
      --form 'title="title"' \
      --form 'body="body"' \
      --form 'repo="test222"'


2. Update an Issue
------------------


Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/issues/{number}``


Parameters
~~~~~~~~~~

+----------------+------------------------------+----------+-----------+
| Parameter      | Description                  | Type     | Data Type |
+================+==============================+==========+===========+
| access_token\* | personal access token        | query    | string    |
+----------------+------------------------------+----------+-----------+
| owner\*        | Repository Owner Path        | path     | string    |
|                | (Organization or User Path)  |          |           |
+----------------+------------------------------+----------+-----------+
| repo\*         | Repository Path              | formData | string    |
+----------------+------------------------------+----------+-----------+
| number\*       | Issue number in the          | path     | string    |
|                | repository                   |          |           |
+----------------+------------------------------+----------+-----------+
| title\*        | title                        | formData | string    |
+----------------+------------------------------+----------+-----------+
| body           | Issue Description            | formData | string    |
+----------------+------------------------------+----------+-----------+
| state          | Issue state，reopen、close   | formData | string    |
+----------------+------------------------------+----------+-----------+
| assignee       | assignee                     | formData | string    |
+----------------+------------------------------+----------+-----------+
| milestone      | milestone ID                 | formData | int       |
+----------------+------------------------------+----------+-----------+
| labels         | Comma-separated list of      | formData | string    |
|                | label names.                 |          |           |
+----------------+------------------------------+----------+-----------+
| security_hole  | Whether the issue is private | formData | string    |
|                | (default is false).          |          |           |
+----------------+------------------------------+----------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 152467,
        "html_url": "https://test.gitcode.net/dengmengmian/test01/issues/14",
        "number": 14,
        "state": "closed",
        "title": "取属且阶",
        "body": "速军间问备题意自系建技至速。那照与受证们老则使六么信。联不格决白转数特先到接单备心样本及。比论受感此中成要则片会受争里领周局。",
        "user": {
          "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
          "events_url": null,
          "followers_url": null,
          "following_url": null,
          "gists_url": null,
          "html_url": "https://test.gitcode.net/dengmengmian",
          "id": "661ce4eab470b1430d456154",
          "login": "dengmengmian",
          "member_role": null,
          "name": "麻凡_",
          "organizations_url": null,
          "received_events_url": null,
          "remark": null,
          "repos_url": null,
          "starred_url": null,
          "subscriptions_url": null,
          "type": null,
          "url": null
        },
        "assignee": {
          "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
          "events_url": null,
          "followers_url": null,
          "following_url": null,
          "gists_url": null,
          "html_url": "https://test.gitcode.net/dengmengmian",
          "id": "661ce4eab470b1430d456154",
          "login": "dengmengmian",
          "member_role": null,
          "name": "麻凡_",
          "organizations_url": null,
          "received_events_url": null,
          "remark": null,
          "repos_url": null,
          "starred_url": null,
          "subscriptions_url": null,
          "type": null,
          "url": null
        },
        "repository": {
          "id": 152467,
          "full_name": "dengmengmian/test01",
          "path": "test01",
          "name": "test01",
          "description": "",
          "created_at": "2024-04-16T14:38:43.464+08:00",
          "updated_at": "2024-04-18T18:27:21.955+08:00"
        },
        "created_at": "2024-04-16T14:38:43.464+08:00",
        "updated_at": "2024-04-18T18:27:21.955+08:00",
        "finished_at": "2024-04-16T14:49:45.166+08:00",
        "labels": [
          {
            "id": 382389,
            "name": "ad",
            "color": "#428BCA"
          },
          {
            "id": 382388,
            "name": "id",
            "color": "#428BCA"
          }
        ],
        "stage": "New",
        "severity": "Major"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PATCH 'https://api.gitcode.com/api/v5/repos/xiaogang_test/issues/1?access_token=token' \
      --form 'title="title"' \
      --form 'body="body"' \
      --form 'repo="test222"'


3. Get a Issue of a Repository
------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{number}``


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
| number\*       | issue number                    | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 152212,
        "html_url": "https://test.gitcode.net/dengmengmian/test01/issues/3",
        "number": 3,
        "state": "opened",
        "title": "查员种金交片",
        "body": "而很资七图数指反系并物众示易今高。运边月发红条亲才调二心点上米面世其分。由众计比维选作小指件每酸一见基历。向九又中国层合感内两米或自很转的。",
        "user": {
          "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
          "events_url": null,
          "followers_url": null,
          "following_url": null,
          "gists_url": null,
          "html_url": "https://test.gitcode.net/dengmengmian",
          "id": "661ce4eab470b1430d456154",
          "login": "dengmengmian",
          "member_role": null,
          "name": "麻凡_",
          "organizations_url": null,
          "received_events_url": null,
          "remark": null,
          "repos_url": null,
          "starred_url": null,
          "subscriptions_url": null,
          "type": null,
          "url": null
        },
        "assignee": null,
        "repository": {
          "id": 280713,
          "full_name": "dengmengmian / test01",
          "path": "test01",
          "name": "test01",
          "description": "",
          "created_at": "2024-04-15T16:27:45.090+08:00",
          "updated_at": "2024-04-15T16:27:45.090+08:00",
          "assigner": null,
          "pushed_at": null,
          "paas": null,
          "assignees_number": null,
          "testers_number": null,
          "assignee": null,
          "testers": null
        },
        "created_at": "2024-04-15T21:58:21.188+08:00",
        "updated_at": "2024-04-15T21:58:21.188+08:00",
        "finished_at": null,
        "labels": [],
        "priority": null,
        "issue_type": null,
        "issue_state": "opened",
        "issue_state_detail": null,
        "stage": "New",
        "severity": "Major"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/issues/1?access_token=token'


4. Get All Issues of a Repository
---------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues``


Parameters
~~~~~~~~~~

+----------------+------------------------------------+-------+-----------+
| Parameter      | Description                        | Type  | Data Type |
+================+====================================+=======+===========+
| access_token\* | personal access token              | query | string    |
+----------------+------------------------------------+-------+-----------+
| owner\*        | Repository Owner Path              | path  | string    |
|                | (Organization or User Path)        |       |           |
+----------------+------------------------------------+-------+-----------+
| repo\*         | Repository Path(path)              | path  | string    |
+----------------+------------------------------------+-------+-----------+
| state          | Issue state: open, closed， all.   | query | string    |
|                | Default: all                       |       |           |
+----------------+------------------------------------+-------+-----------+
| labels         | Comma-separated list of label      | query | string    |
|                | names.                             |       |           |
+----------------+------------------------------------+-------+-----------+
| sort           | sort: created，updated. Default:   | query | string    |
|                | created                            |       |           |
+----------------+------------------------------------+-------+-----------+
| direction      | asc/desc, Default: desc            | query | string    |
+----------------+------------------------------------+-------+-----------+
| since          | since, eg:                         | query | string    |
|                | 2024-11-10T08:10:30.000+08:00（The |       |           |
|                | plus sign (+) should be            |       |           |
|                | URL-encoded as %2B.）              |       |           |
+----------------+------------------------------------+-------+-----------+
| page           | Current Page Number，default:1     | query | int       |
+----------------+------------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum            | query | int       |
|                | 100,default:20                     |       |           |
+----------------+------------------------------------+-------+-----------+
| created_at     | created at ,eg:                    | query | string    |
|                | 2024-11-10T08:10:30.000+08:00      |       |           |
+----------------+------------------------------------+-------+-----------+
| milestone      | milestone name, none means issues  | query | string    |
|                | without a milestone                |       |           |
+----------------+------------------------------------+-------+-----------+
| assignee       | assignee                           | query | string    |
+----------------+------------------------------------+-------+-----------+
| creator        | creator                            | query | string    |
+----------------+------------------------------------+-------+-----------+
| created_after  | created after, eg:                 | query | string    |
|                | 2024-11-10T08:10:30.000+08:00      |       |           |
+----------------+------------------------------------+-------+-----------+
| created_before | created before, eg:                | query | string    |
|                | 2024-11-10T08:10:30.000+08:00      |       |           |
+----------------+------------------------------------+-------+-----------+
| updated_after  | updated after , eg:                | query | string    |
|                | 2024-11-10T08:10:30.000+08:00      |       |           |
+----------------+------------------------------------+-------+-----------+
| updated_before | updated before, eg:                | query | string    |
|                | 2024-11-10T08:10:30.000+08:00      |       |           |
+----------------+------------------------------------+-------+-----------+


Response
~~~~~~~~

header
''''''

============ ================== =========
头部名       Description        Data Type
============ ================== =========
total_count  issue count        Integer
total_page   total page         Integer
all_issues   all issues count   Integer
open_issues  open issues count  Integer
close_issues close issues count Integer
============ ================== =========

response body
'''''''''''''

.. container:: highlight

   .. code:: text

      [
        {
          "id": 152642,
          "html_url": "https://test.gitcode.net/dengmengmian/test01/issues/15",
          "number": "15",
          "state": "opened",
          "title": "半月据",
          "body": "节油料被引系活力级少本化段维家住实。常气前步证时第样日所阶效温界到量。个导土机技亲布接增论始高世收圆流级集。此般区才听党机达两收文斗公加白。代军前分写第图美市与道及间。",
          "user": {
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
            "events_url": null,
            "followers_url": null,
            "following_url": null,
            "gists_url": null,
            "html_url": "https://test.gitcode.net/dengmengmian",
            "id": "661ce4eab470b1430d456154",
            "login": "dengmengmian",
            "member_role": null,
            "name": "麻凡_",
            "organizations_url": null,
            "received_events_url": null,
            "remark": null,
            "repos_url": null,
            "starred_url": null,
            "subscriptions_url": null,
            "type": null,
            "url": null
          },
          "assignee": {
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
            "events_url": null,
            "followers_url": null,
            "following_url": null,
            "gists_url": null,
            "html_url": "https://test.gitcode.net/dengmengmian",
            "id": "661ce4eab470b1430d456154",
            "login": "dengmengmian",
            "member_role": null,
            "name": "麻凡_",
            "organizations_url": null,
            "received_events_url": null,
            "remark": null,
            "repos_url": null,
            "starred_url": null,
            "subscriptions_url": null,
            "type": null,
            "url": null
          },
          "repository": {
            "id": 280713,
            "full_name": "dengmengmian / test01",
            "path": "test01",
            "name": "test01",
            "description": "",
            "created_at": "2024-04-15T16:27:45.090+08:00",
            "updated_at": "2024-04-15T16:27:45.090+08:00",
            "assigner": null,
            "pushed_at": null,
            "paas": null,
            "assignees_number": null,
            "testers_number": null,
            "assignee": null,
            "testers": null
          },
          "created_at": "2024-04-18T14:35:15.479+08:00",
          "updated_at": "2024-04-20T15:20:30.111+08:00",
          "finished_at": null,
          "labels": [
            {
              "id": 382379,
              "name": "enim",
              "color": "#428BCA"
            },
            {
              "id": 382378,
              "name": "proident",
              "color": "#428BCA"
            },
            {
              "id": 382377,
              "name": "qui",
              "color": "#428BCA"
            }
          ],
          "priority": null,
          "issue_type": null,
          "issue_state": "opened",
          "issue_state_detail": null
        },
        {
          "id": 152467,
          "html_url": "https://test.gitcode.net/dengmengmian/test01/issues/14",
          "number": "14",
          "state": "closed",
          "title": "取属且阶",
          "body": "速军间问备题意自系建技至速。那照与受证们老则使六么信。联不格决白转数特先到接单备心样本及。比论受感此中成要则片会受争里领周局。",
          "user": {
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
            "events_url": null,
            "followers_url": null,
            "following_url": null,
            "gists_url": null,
            "html_url": "https://test.gitcode.net/dengmengmian",
            "id": "661ce4eab470b1430d456154",
            "login": "dengmengmian",
            "member_role": null,
            "name": "麻凡_",
            "organizations_url": null,
            "received_events_url": null,
            "remark": null,
            "repos_url": null,
            "starred_url": null,
            "subscriptions_url": null,
            "type": null,
            "url": null
          },
          "assignee": {
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
            "events_url": null,
            "followers_url": null,
            "following_url": null,
            "gists_url": null,
            "html_url": "https://test.gitcode.net/dengmengmian",
            "id": "661ce4eab470b1430d456154",
            "login": "dengmengmian",
            "member_role": null,
            "name": "麻凡_",
            "organizations_url": null,
            "received_events_url": null,
            "remark": null,
            "repos_url": null,
            "starred_url": null,
            "subscriptions_url": null,
            "type": null,
            "url": null
          },
          "repository": {
            "id": 280713,
            "full_name": "dengmengmian / test01",
            "path": "test01",
            "name": "test01",
            "description": "",
            "created_at": "2024-04-15T16:27:45.090+08:00",
            "updated_at": "2024-04-15T16:27:45.090+08:00",
            "assigner": null,
            "pushed_at": null,
            "paas": null,
            "assignees_number": null,
            "testers_number": null,
            "assignee": null,
            "testers": null
          },
          "created_at": "2024-04-16T14:38:43.464+08:00",
          "updated_at": "2024-04-18T18:27:21.955+08:00",
          "finished_at": "2024-04-16T14:49:45.166+08:00",
          "labels": [
            {
              "id": 382389,
              "name": "ad",
              "color": "#428BCA"
            },
            {
              "id": 382388,
              "name": "id",
              "color": "#428BCA"
            }
          ],
          "priority": null,
          "issue_type": null,
          "issue_state": "closed",
          "issue_state_detail": null
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/issues?access_token=token'


5. Get All Comments of an Issue in a Repository
-----------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{number}/comments``


Parameters
~~~~~~~~~~

+--------------+------------------------------------+-------+-----------+
| Parameter    | Description                        | Type  | Data Type |
+==============+====================================+=======+===========+
| access_token | personal access token              | query | string    |
+--------------+------------------------------------+-------+-----------+
| owner\*      | Repository Ownership Path          | path  | string    |
|              | (Company, Organization, or         |       |           |
|              | Personal Path)                     |       |           |
+--------------+------------------------------------+-------+-----------+
| repo\*       | Repository Path(path)              | path  | string    |
+--------------+------------------------------------+-------+-----------+
| number\*     | issue number                       | path  | string    |
+--------------+------------------------------------+-------+-----------+
| page         | Current Page Number，default:1     | query | int       |
+--------------+------------------------------------+-------+-----------+
| per_page     | Items Per Page, Maximum            | query | int       |
|              | 100,default:20                     |       |           |
+--------------+------------------------------------+-------+-----------+
| order        | Sorting Order: asc(default),desc   | query | string    |
+--------------+------------------------------------+-------+-----------+
| since        | since, eg:                         | query | string    |
|              | 2024-11-10T08:10:30.000+08:00（The |       |           |
|              | plus sign (+) should be            |       |           |
|              | URL-encoded as %2B.）              |       |           |
+--------------+------------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 271624,
          "body": "Comment Content。",
          "user": {
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
            "events_url": null,
            "followers_url": null,
            "following_url": null,
            "gists_url": null,
            "html_url": "https://test.gitcode.net/dengmengmian",
            "id": "661ce4eab470b1430d456154",
            "login": "dengmengmian",
            "member_role": null,
            "name": "麻凡_",
            "organizations_url": null,
            "received_events_url": null,
            "remark": null,
            "repos_url": null,
            "starred_url": null,
            "subscriptions_url": null,
            "type": null,
            "url": null
          },
          "target": {
            "issue": {
              "id": 152134,
              "title": "",
              "nubmer": 1
            }
          },
          "created_at": "2024-04-19T17:50:18.199+08:00",
          "updated_at": "2024-04-19T17:50:18.199+08:00"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/issues/1/comments?access_token=token'


6. Get All Issue Comments of a Repository
-----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/comments``


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
| sort         | Either created or updated.        | query | string    |
|              | Default: created                  |       |           |
+--------------+-----------------------------------+-------+-----------+
| direction    | Either asc or desc. Ignored       | query | string    |
|              | without the sort parameter.       |       |           |
+--------------+-----------------------------------+-------+-----------+
| since        | Only comments updated at or after | query | string    |
|              | this time are returned. This is a |       |           |
|              | timestamp in ISO 8601 format:     |       |           |
|              | YYYY-MM-DDTHH:MM:SSZ              |       |           |
+--------------+-----------------------------------+-------+-----------+
| page         | Current Page Number，default:1    | query | int       |
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
          "id": 272201,
          "body": "daetete",
          "user": {
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
            "events_url": null,
            "followers_url": null,
            "following_url": null,
            "gists_url": null,
            "html_url": "https://test.gitcode.net/dengmengmian",
            "id": "661ce4eab470b1430d456154",
            "login": "dengmengmian",
            "member_role": null,
            "name": "麻凡_",
            "organizations_url": null,
            "received_events_url": null,
            "remark": null,
            "repos_url": null,
            "starred_url": null,
            "subscriptions_url": null,
            "type": null,
            "url": null
          },
          "target": {
            "issue": {
              "id": 152642,
              "title": "半月据",
              "nubmer": 15
            }
          },
          "created_at": "2024-04-20T15:20:30.104+08:00",
          "updated_at": null
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/issues/comments?access_token=token'


7. Get Pull Requests Associated with an Issue
---------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{number}/pull_requests``


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
| number\*     | issue number                      | path  | string    |
+--------------+-----------------------------------+-------+-----------+
| mode         | 1 (Enhanced mode, returns the     | query | Integer   |
|              | mergeable status of the PR when   |       |           |
|              | the above parameters are passed); |       |           |
|              | 0 (Default, does not return the   |       |           |
|              | mergeable status).                |       |           |
+--------------+-----------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 67585,
          "html_url": "https://api.gitcode.net/test/test/merge_requests/1",
          "diff_url": "https://api.gitcode.net/test/test/merge_requests/1/diffs",
          "number": 1,
          "state": "opened",
          "title": "1",
          "body": "new: 新增文件 test.txt 1",
          "created_at": "2024-04-12T17:50:55.253+08:00",
          "updated_at": "2024-04-20T15:58:30.657+08:00",
          "merged_at": null,
          "closed_at": null,
          "head": {
            "ref": "develop",
            "sha": "061c446d55aae78c7a0f096b2d2dd0d6a1afb170",
            "repo": {
              "path": "paopao1",
              "name": "paopao1"
            },
            "assigner": {
              "login": "test",
              "name": "test"
            }
          },
          "base": {
            "ref": "main",
            "sha": "667d4ac032b2faa13d019753ac218b4f78338273",
            "repo": {
              "path": "paopao1",
              "name": "paopao1"
            },
            "assigner": null
          },
          "assignees": [
            {
              "id": "65803cddcf1e2d1aa3d2e99f",
              "login": "test",
              "name": null,
              "avatar_url": null,
              "html_url": "https://api.gitcode.net/test"
            }
          ],
          "testers": [
            {
              "id": "65803cddcf1e2d1aa3d2e99f",
              "login": "test",
              "name": "test",
              "avatar_url": null,
              "html_url": "https://api.gitcode.net/test"
            }
          ],
          "labels": [
            {
              "id": 383707,
              "color": "#CCCCCC",
              "name": "wontfix",
              "repository_id": null,
              "url": null,
              "created_at": "2024-04-19",
              "updated_at": "2024-04-19",
              "text_color": "#333333"
            }
          ],
          "can_merge_check": true
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/issues/1/pull_requests?access_token=token'


8. Get All Labels of an Issue in an Enterprise
----------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/enterprises/{enterprise}/issues/{issue_id}/labels``


Parameters
~~~~~~~~~~

============ ====================================== ===== =========
Parameter    Description                            Type  Data Type
============ ====================================== ===== =========
access_token personal access token                  query string
enterprise\* enterprise path                        path  string
issue_id\*   Global Issue ID                        path  string
page         Current Page Number，default:1         query int
per_page     Items Per Page, Maximum 100,default:20 query int
============ ====================================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "color": "#008672",
          "name": "help wanted",
          "id": 381445,
          "url": ""
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/enterprises/xiaogang_test/issues/1/labels?access_token=token'


9. Create an Issue Label
------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{number}/labels``


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
| number\*       | issue number                    | path  | string    |
+----------------+---------------------------------+-------+-----------+
| labels\*       | labels, eg: [“feat”, “bug”]     | body  | array     |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "color": "#008672",
          "name": "help wanted",
          "id": 381445,
          "title": "help wanted",
          "type": null,
          "textColor": "#FFFFFF"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/issues/1/labels?access_token=token' \
      --header 'Content-Type: application/json' \
      --data '["bug","feat"]'


10. Delete an Issue Label
-------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{number}/labels/{name}``


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
| number\*       | issue number, i.e., the         | path  | string    |
|                | sequence number of the issue in |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+
| name\*         | label name (For bulk deletion,  | path  | string    |
|                | separate the items with an      |       |           |
|                | English comma, e.g.,            |       |           |
|                | bug,feature.)                   |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

``204``


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/issues/1/labels/bug?access_token=token'


11. Create an Issue Comment
---------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/{number}/comments``


Parameters
~~~~~~~~~~

+----------------+------------------------------+----------+-----------+
| Parameter      | Description                  | Type     | Data Type |
+================+==============================+==========+===========+
| access_token\* | personal access token        | query    | string    |
+----------------+------------------------------+----------+-----------+
| owner\*        | Repository Owner Path        | path     | string    |
|                | (Organization or User Path)  |          |           |
+----------------+------------------------------+----------+-----------+
| repo\*         | Repository Path(path)        | path     | string    |
+----------------+------------------------------+----------+-----------+
| number\*       | issue number                 | path     | string    |
+----------------+------------------------------+----------+-----------+
| body\*         | The contents of the comment. | formdata | string    |
+----------------+------------------------------+----------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 271624,
        "body": "Comment Content。",
        "user": {
          "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
          "events_url": null,
          "followers_url": null,
          "following_url": null,
          "gists_url": null,
          "html_url": "https://test.gitcode.net/dengmengmian",
          "id": "661ce4eab470b1430d456154",
          "login": "dengmengmian",
          "member_role": null,
          "name": "麻凡_",
          "organizations_url": null,
          "received_events_url": null,
          "remark": null,
          "repos_url": null,
          "starred_url": null,
          "subscriptions_url": null,
          "type": null,
          "url": null
        },
        "target": {
          "issue": {
            "id": 152134,
            "title": "",
            "nubmer": 1
          }
        },
        "created_at": null,
        "updated_at": null
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/issues/1/comments?access_token=token' \
      --form 'body="1"'


12. Get the Events Log of a Issue
---------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/issues/{number}/operate_logs``


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
| repo\*         | Repository Path(path)           | query | string    |
+----------------+---------------------------------+-------+-----------+
| number\*       | issue number                    | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 272199,
          "user": {
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
            "events_url": null,
            "followers_url": null,
            "following_url": null,
            "gists_url": null,
            "html_url": "https://test.gitcode.net/dengmengmian",
            "id": "661ce4eab470b1430d456154",
            "login": "dengmengmian",
            "member_role": null,
            "name": "麻凡_",
            "organizations_url": null,
            "received_events_url": null,
            "remark": null,
            "repos_url": null,
            "starred_url": null,
            "subscriptions_url": null,
            "type": null,
            "url": null
          },
          "content": "Create issue mr links: **new: 新增文件 1.text** #1",
          "created_at": "2024-04-20T15:20:24.009+08:00",
          "action_type": "add_issue_mr_link",
          "update_at": "2024-04-20T15:20:24.009+08:00",
          "title": "new: 新增文件 1.text",
          "body": "new: 新增文件 1.text ",
          "head": {
            "ref": "develop",
            "sha": "dd954d3a779edc86dae5b4b60c7f24dd0f195bf4",
            "repo": {
              "path": "test01",
              "name": "test01"
            },
            "assigner": {
              "login": "dengmengmian",
              "name": "麻凡_"
            }
          },
          "base": {
            "ref": "main",
            "sha": "32cff0d8faaa0c044d0f94957e656051986e8403",
            "repo": {
              "path": "test01",
              "name": "test01"
            },
            "assigner": null
          },
          "issue_id": "152642"
        },
        {
          "id": 272198,
          "user": {
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
            "events_url": null,
            "followers_url": null,
            "following_url": null,
            "gists_url": null,
            "html_url": "https://test.gitcode.net/dengmengmian",
            "id": "661ce4eab470b1430d456154",
            "login": "dengmengmian",
            "member_role": null,
            "name": "麻凡_",
            "organizations_url": null,
            "received_events_url": null,
            "remark": null,
            "repos_url": null,
            "starred_url": null,
            "subscriptions_url": null,
            "type": null,
            "url": null
          },
          "content": "changed milestone to testew",
          "created_at": "2024-04-20T15:20:09.305+08:00",
          "action_type": "milestone",
          "update_at": "2024-04-20T15:20:09.305+08:00",
          "title": null,
          "body": null,
          "head": null,
          "base": null,
          "issue_id": "152642"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/enterprises/xiaogang_test/issues/1/operate_logs?access_token=token'


13. Get All Issues of an Enterprise
-----------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/enterprises/{enterprise}/issues``


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
| enterprise\*   | Enterprise Path(path/login)     | path  | string    |
+----------------+---------------------------------+-------+-----------+
| state          | state: open, closed, all        | query | string    |
|                | Default: open                   |       |           |
+----------------+---------------------------------+-------+-----------+
| labels         | Comma-separated list of label   | query | string    |
|                | names.                          |       |           |
+----------------+---------------------------------+-------+-----------+
| sort           | sort: created, updated_at.      | query | string    |
|                | Default: created_at             |       |           |
+----------------+---------------------------------+-------+-----------+
| direction      | asc/desc, Default: desc         | query | string    |
+----------------+---------------------------------+-------+-----------+
| since          | since                           | query | string    |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number，default:1  | query | int       |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum         | query | int       |
|                | 100,default:20                  |       |           |
+----------------+---------------------------------+-------+-----------+
| milestone      | milestone name, none means      | query | string    |
|                | issues without a milestone, and |       |           |
|                | \* means all issues with a      |       |           |
|                | milestone.                      |       |           |
+----------------+---------------------------------+-------+-----------+
| assignee       | assignee, none means issues     | query | string    |
|                | without a assignee, and \*      |       |           |
|                | means all issues with a         |       |           |
|                | assignee.的                     |       |           |
+----------------+---------------------------------+-------+-----------+
| creator        | creator                         | query | string    |
+----------------+---------------------------------+-------+-----------+
| program        | The project name. none means no | query | string    |
|                | associated project, and \*      |       |           |
|                | means all issues with an        |       |           |
|                | associated project.             |       |           |
+----------------+---------------------------------+-------+-----------+
| created_at     | created at                      | query | string    |
+----------------+---------------------------------+-------+-----------+
| created_before | created before                  | query | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 340035,
          "html_url": "https://gitcode.com/xiaogang_test/test222/issues/7",
          "number": "7",
          "state": "open",
          "title": "2222",
          "body": "2222",
          "user": {
            "id": "65f96506b3a9e65264980447",
            "login": "xiaogang",
            "name": "xiaogang"
          },
          "repository": {
            "id": 249609,
            "full_name": "xiaogang_test/test222",
            "human_name": "测试组织 / test222",
            "path": "test222",
            "name": "test222",
            "url": "https://gitcode.com/xiaogang_test/test222",
            "assigner": {},
            "paas": ""
          },
          "created_at": "2024-11-20T15:40:35+08:00",
          "updated_at": "2024-11-20T15:40:35+08:00",
          "labels": [],
          "issue_state": "未提单",
          "priority": 0,
          "issue_type": "需求",
          "issue_state_detail": {
            "title": "未提单",
            "serial": 1,
            "id": 222
          },
          "issue_type_detail": {
            "title": "需求",
            "id": 629,
            "is_system": false
          },
          "comments": 0,
          "parent_id": 0,
          "url": "https://gitcode.com/api/v5/repos/xiaogang_test/test222/issues/7"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/enterprises/Hello_worldsss/issues?state=open&direction=desc&page=1&per_page=20&access_token=xxxx&sort=created_at' \


14. Get All Issues of the Authorized User
-----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/user/issues``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| filter         | filter: assigned, created, all. | query | string    |
|                | Default: assigned               |       |           |
+----------------+---------------------------------+-------+-----------+
| state          | state: open , closed. Default:  | query | string    |
|                | open                            |       |           |
+----------------+---------------------------------+-------+-----------+
| labels         | Comma-separated list of label   | query | string    |
|                | names.                          |       |           |
+----------------+---------------------------------+-------+-----------+
| sort           | sort: created, updated_at.      | query | string    |
|                | Default: created_at             |       |           |
+----------------+---------------------------------+-------+-----------+
| direction      | asc/desc, Default: desc         | query | string    |
+----------------+---------------------------------+-------+-----------+
| since          | since                           | query | string    |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number，default:1  | query | int       |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum         | query | int       |
|                | 100,default:20                  |       |           |
+----------------+---------------------------------+-------+-----------+
| schedule       | schedule                        | query | string    |
+----------------+---------------------------------+-------+-----------+
| deadline       | deadline                        | query | string    |
+----------------+---------------------------------+-------+-----------+
| created_at     | created at                      | query | string    |
+----------------+---------------------------------+-------+-----------+
| finished_at    | finished at                     | query | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 490786,
          "html_url": "https://gitcode.com/gitcode-dev/gitcode-TestTask/issues/319",
          "number": "319",
          "state": "open",
          "title": "评论中附件图片的大小从 2M 放开到 10M，允许用户上传更大尺寸的图片附件",
          "body": "### 提测内容\n            \n如题： https://gitcode.com/gitcode-dev/releases-log/issues/617\n### 需求文档地址\n            \nhttps://gitcode.com/gitcode-dev/releases-log/issues/617\n### UI设计图地址\n            \n无\n### 技术方案地址\n            \n无\n### 影响范围\n            \n\n### 涉及上线服务\n            \ngitcode-fe\n### 研发人员\n            \n刘奥林\n### pr文件改动diffs\n            \nhttps://gitcode.com/gitcode-dev/gitcode-fe/merge_requests/3661/diffs\n### 依赖项\n            \n\n### API调整\n            \n\n### 数据库调整\n            \n\n### nacos配置调整\n            \n\n### 运维调整\n            \n\n",
          "assignee": {
            "avatar_url": "https://cdn-img.gitcode.com/db/cf/dbc07f37245cab6693ef7a3ba7eb101634f480c263fa294f6b366e4a0fe60a45.png?time=1720429708203",
            "html_url": "https://gitcode.com/yinlin",
            "id": "303745",
            "login": "yinlin",
            "name": "yinlin-昵称",
            "type": "User"
          }
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/issues?access_token=xxx=created_at&direction=desc&page=1&per_page=20' \


15. Update an Issue Comment
---------------------------


Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/comments/{id}``


Parameters
~~~~~~~~~~

+----------------+------------------------------+----------+-----------+
| Parameter      | Description                  | Type     | Data Type |
+================+==============================+==========+===========+
| access_token\* | personal access token        | query    | string    |
+----------------+------------------------------+----------+-----------+
| owner\*        | Repository Owner Path        | path     | string    |
|                | (Organization or User Path)  |          |           |
+----------------+------------------------------+----------+-----------+
| repo\*         | Repository Path(path)        | path     | string    |
+----------------+------------------------------+----------+-----------+
| id\*           | comment ID                   | path     | string    |
+----------------+------------------------------+----------+-----------+
| body\*         | Comment Content              | formDate | string    |
+----------------+------------------------------+----------+-----------+


Response
~~~~~~~~

无


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PATCH 'https://api.gitcode.com/api/v5/repos/Hello_worldsss/IK_001_01/pulls/comments/1478704?access_token=xxx' \
      --header 'Content-Type: application/json' \
      --data '{
          "body":"0913更新评论"
      }'


16. Delete an Issue Comment
---------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/comments/{id}``


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
| id\*           | the ID of a comment             | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/repos/Hello_worldsss/IK_001_01/issues/comments/1486664?access_token=xxx'


17. Get an Issue Comment of a Repository
----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/issues/comments/{id}``


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
| id\*           | the ID of a comment             | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 1495484,
        "body": "测试 issue 评论",
        "comment_type": "DiscussionNote",
        "user": {
          "id": "268",
          "login": "dengmengmian",
          "name": "麻凡",
          "type": "User"
        },
        "target": {
          "issue": {
            "id": 494561,
            "title": "测试 issue 评论",
            "number": "494561"
          }
        },
        "created_at": "2024-10-08T19:52:19+08:00",
        "updated_at": "2024-10-08T19:52:19+08:00"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/issues/comments/1495484?access_token=yuBy'


18. Get Issues of a Organization for the Current User
-----------------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/orgs/{org}/issues``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| filter         | filter: assigned, created, all. | query | string    |
|                | Default: assigned               |       |           |
+----------------+---------------------------------+-------+-----------+
| state          | state: open, closed, Default:   | query | string    |
|                | open                            |       |           |
+----------------+---------------------------------+-------+-----------+
| labels         | Comma-separated list of label   | query | string    |
|                | names.                          |       |           |
+----------------+---------------------------------+-------+-----------+
| sort           | sort: created, updated_at.      | query | string    |
|                | Default ：created_at            |       |           |
+----------------+---------------------------------+-------+-----------+
| direction      | asc/desc, default: desc         | query | string    |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number，default:1  | query | integer   |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum         | query | integer   |
|                | 100,default:20                  |       |           |
+----------------+---------------------------------+-------+-----------+
| created_at     | created at                      | query | string    |
+----------------+---------------------------------+-------+-----------+
| org\*          | Organization Path (path/login)  | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 495900,
          "html_url": "https://gitcode.com/Go-Tribe/test01/issues/1",
          "number": "1",
          "state": "open",
          "title": "1",
          "body": "1",
          "repository": {
            "id": 4016571,
            "full_name": "Go-Tribe/test01",
            "human_name": "gotribe / test01",
            "path": "test01",
            "name": "test01",
            "url": "https://gitcode.com/Go-Tribe/test01",
            "owner": {
              "id": "650d67fbae6d795139b49b41",
              "login": "dengmengmian",
              "name": "麻凡"
            }
          },
          "created_at": "2024-10-12T18:27:27+08:00",
          "updated_at": "2024-10-12T18:27:27+08:00",
          "labels": [],
          "priority": 0,
          "comments": 0,
          "parent_id": 0
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/orgs/go-tribe/issues?filter=all&page=1&per_page=2&state=all&sort=created_at&access_token=token' \
      --header 'Content-Type: application/json' \
      --data-raw '{}'


19. Get All Comments for an Enterprise Issue
--------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/enterprises/{enterprise}/issues/{number}/comments``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access token\* | Personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| enterprise\*   | Repository Owner Path           | path  | string    |
|                | (Organization or User Path)     |       |           |
+----------------+---------------------------------+-------+-----------+
| number\*       | Global Issue ID                 | path  | int       |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number，default:1  | query | int       |
+----------------+---------------------------------+-------+-----------+
| per_page       | Number of items per page:       | query | int       |
|                | maximum 100, default 20         |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "body": "etst",
          "created_at": "2024-12-10T16:02:21+08:00",
          "id": 1535981,
          "target": {
            "issue": {
              "id": 471521,
              "iid": 1,
              "title": "bbbbb"
            }
          },
          "updated_at": "2024-12-10T16:02:21+08:00",
          "user": {
            "id": 287,
            "login": "csdn_fenglh",
            "name": "fenglh",
            "type": "User"
          }
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/enterprises/owner-test/issues/471521/comments?access_token=your_token'


20. Get a Specific Issue for an Enterprise
------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/enterprises/{enterprise}/issues/{number}``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access token\* | User’s authorization code       | query | string    |
+----------------+---------------------------------+-------+-----------+
| enterprise\*   | Path to the repository owner    | path  | string    |
|                | (organization or user)          |       |           |
+----------------+---------------------------------+-------+-----------+
| number\*       | Globally unique ID of the issue | path  | int       |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "id": 471521,
          "html_url": "https://test.gitcode.net/owner-test/wonderful1/issues/1",
          "number": "1",
          "state": "open",
          "title": "bbbbb",
          "body": "sdfsdf",
          "user": {
              "html_url": "https://test.gitcode.net/csdn_fenglh",
              "id": "654c61e5560ed95fd216cf31",
              "login": "csdn_fenglh",
              "name": "fenglh"
          },
          "repository": {
              "id": 686738,
              "full_name": "owner-test/wonderful1",
              "path": "wonderful1",
              "name": "wonderful1",
              "description": "My test code repository",
              "created_at": "2024-10-16T15:51:35+08:00",
              "updated_at": "2024-10-16T15:51:35+08:00",
              "assigner": {},
              "paas": ""
          },
          "created_at": "2024-12-10T16:02:12+08:00",
          "updated_at": "2024-12-10T16:02:21+08:00",
          "finished_at": "",
          "labels": [],
          "issue_state": "To Do",
          "priority": 0,
          "issue_state_detail": {
              "title": "To Do",
              "serial": 0
          }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/enterprises/owner-test/issues/471521?access_token=your_token'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/issues/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
