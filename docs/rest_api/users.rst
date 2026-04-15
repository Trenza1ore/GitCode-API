User API Documentation
======================


1. Get a user
-------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/users/{username}``

Parameters
~~~~~~~~~~

============ ===================== ===== =========
Parameter    Description           Type  Data Type
============ ===================== ===== =========
access_token personal access token query string
username\*   username              path  string
============ ===================== ===== =========

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "avatar_url": "https://cdn-img.gitcode.com/ec/fb/430ecf07b9ee91bbbbf341d92a36783d06e69086f82ce8cf5a6406f79f1c9cf4.png",
        "followers_url": "https://api.gitcode.com/api/v5users/dengmengmian/followers",
        "html_url": "https://gitcode.com/dengmengmian",
        "id": "650d67fbae6d795139b49b41",
        "login": "dengmengmian",
        "name": "麻凡",
        "type": "User",
        "url": "https://api.gitcode.com/api/v5/dengmengmian",
        "bio": "Nacos是由阿里巴巴开源的服务治理中间件，集成了动态服务发现、配置管理和服务元数据管理功能，广泛应用于微服务架构中，简化服务治理过程。",
        "blog": "https://www.dengmengmian.com",
        "company": "开发者",
        "email": "my@dengmengmian.com",
        "followers": 0,
        "following": 6,
        "top_languages": ["Python", "Shell"]
      }

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/users/dengmengmian' \
      --header 'Authorization: Bearer {your-token}'


2. Get the profile of the authorized user
-----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/user``


Parameters
~~~~~~~~~~

============== ===================== ===== =========
Parameter      Description           Type  Data Type
============== ===================== ===== =========
access_token\* personal access token query string
============== ===================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "avatar_url": "https://cdn-img.gitcode.com/fa/be/2fa2be6d3ffd01599dbc0a3c71ee9ec4cadb82f63a7a8489187645064ad95e59.png?time=1694709764757",
        "followers_url": "https://api.gitcode.com/api/v5users/gitcode-xxm/followers",
        "html_url": "https://gitcode.com/gitcode-xxm",
        "id": "64e5ed8f7e20aa73efcbc302",
        "login": "gitcode-xxm",
        "name": "xxm",
        "type": "User",
        "url": "https://api.gitcode.com/api/v5/gitcode-xxm",
        "bio": "a PM ",
        "blog": "https://gitcode.com",
        "company": "",
        "email": "xiongjiamu@163.com",
        "followers": 8,
        "following": 35,
        "top_languages": ["Python", "Markdown", "C++", "C", "HTML"]
      }


DEMO
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/user' \
      --header 'Authorization: Bearer {your-token}'


3. Get all emails of the authorized user
----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/emails``


Parameters
~~~~~~~~~~

============== ===================== ===== =========
Parameter      Description           Type  Data Type
============== ===================== ===== =========
access_token\* personal access token query string
============== ===================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "email": "my@dengmengmian.com",
          "state": "confirmed"
        },
        {
          "email": "xxxx@qq.com",
          "state": "confirmed"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/emails?access_token={your-token}' \


4. Get the personal activity of a user
--------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/users/{username}/events``


Parameters
~~~~~~~~~~

============== ===================== ===== =========
Parameter      Description           Type  Data Type
============== ===================== ===== =========
username       username              path  string
access_token\* personal access token query string
year           Start Year（2024）    query string
next           End Date              query string
============== ===================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "events": {
          "2024-08-27": [
            {
              "action": 5,
              "action_name": "pushed to",
              "author": {
                "id": 704,
                "iam_id": "5c340cab034d455992541f00f9936fb4",
                "username": "dengmengmian",
                "state": "active",
                "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
                "email": "",
                "name": "dengmengmian",
                "name_cn": "dengmengmian",
                "web_url": "https://test.gitcode.net/dengmengmian"
              },
              "author_id": 704,
              "author_username": "dengmengmian",
              "created_at": "2024-08-27T10:34:05.093Z",
              "project": {
                "main_repository_language": [null, null],
                "star_count": 0,
                "forks_count": 0,
                "develop_mode": "normal",
                "stared": false
              },
              "project_id": 507167,
              "project_name": "mactribe/midsommarcartoon",
              "push_data": {
                "commit_count": 1,
                "action": "pushed",
                "ref_type": "branch",
                "commit_from": "2ce472fec073f77804c3480ccf128219a6172e54",
                "commit_to": "14b742fe434797fb073ba536804011f735f2f430",
                "ref": "main",
                "commit_title": "文件title"
              },
              "_links": {
                "project": "https://test.gitcode.net/mactribe/midsommarcartoon",
                "action_type": ""
              }
            },
            {
              "action": 5,
              "action_name": "pushed to",
              "author": {
                "id": 704,
                "iam_id": "5c340cab034d455992541f00f9936fb4",
                "username": "dengmengmian",
                "state": "active",
                "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/fa/fe/f32a9fecc53e890afbd48fd098b0f6c5f20f062581400c76c85e5baab3f0d5b2.png",
                "email": "",
                "name": "dengmengmian",
                "name_cn": "dengmengmian",
                "web_url": "https://test.gitcode.net/dengmengmian"
              },
              "author_id": 704,
              "author_username": "dengmengmian",
              "created_at": "2024-08-27T10:31:17.494Z",
              "project": {
                "main_repository_language": [null, null],
                "star_count": 0,
                "forks_count": 0,
                "develop_mode": "normal",
                "stared": false
              },
              "project_id": 507167,
              "project_name": "mactribe/midsommarcartoon",
              "push_data": {
                "commit_count": 1,
                "action": "pushed",
                "ref_type": "branch",
                "commit_from": "ee25b0353dae9bf19f5e3e733e651e7870020386",
                "commit_to": "2ce472fec073f77804c3480ccf128219a6172e54",
                "ref": "main",
                "commit_title": "文件title"
              },
              "_links": {
                "project": "https://test.gitcode.net/mactribe/midsommarcartoon",
                "action_type": ""
              }
            }
          ]
        },
        "next": "2024-08-01T10:10:40.370Z"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/users/dengmengmian/events?access_token={your-token}&year=2024&next=2024-09-05T13%3A48%3A47.370Z'


5. Get the public repositories of a user
----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/users/{username}/repos``


Parameters
~~~~~~~~~~

+----------------+--------------------------------------------------------------------------------------------+-------+-----------+
| Parameter      | Description                                                                                | Type  | Data Type |
+================+============================================================================================+=======+===========+
| access_token\* | personal access token                                                                      | query | string    |
+----------------+--------------------------------------------------------------------------------------------+-------+-----------+
| username\*     | username(username/login)                                                                   | path  | string    |
+----------------+--------------------------------------------------------------------------------------------+-------+-----------+
| type           | 用户创建的仓库(owner)，用户个人仓库(personal)，用户为仓库成员(member)，所有(all)。Default: | query | string    |
|                | 所有(all) Repository Ownership Types: Owner(Repositories created by the user),             |       |           |
|                | Personal(The user’s personal repositories), Member(Repositories where the user is a        |       |           |
|                | member), All(All repositories).Default: all                                                |       |           |
+----------------+--------------------------------------------------------------------------------------------+-------+-----------+
| sort           | Sorting Options: Created(Sort by creation time), Updated(Sort by update time), Pushed(Sort | query | string    |
|                | by last pushed time), Full Name(Sort by repository’s full name). Default: full_name        |       |           |
+----------------+--------------------------------------------------------------------------------------------+-------+-----------+
| direction      | If the sort parameter is set to full_name, the sorting will be in ascending order (asc).   | query | string    |
|                | Otherwise, it will be in descending order (desc).                                          |       |           |
+----------------+--------------------------------------------------------------------------------------------+-------+-----------+
| page           | Current Page Number                                                                        | query | int       |
+----------------+--------------------------------------------------------------------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum 100                                                                | query | int       |
+----------------+--------------------------------------------------------------------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 2734882,
          "full_name": "dengmengmian/manifest",
          "human_name": "dengmengmian / manifest",
          "url": "https://api.gitcode.com/api/v5/repos/dengmengmian/manifest",
          "namespace": {
            "id": 199940,
            "type": "user",
            "name": "dengmengmian",
            "path": "dengmengmian",
            "html_url": "https://gitcode.com/dengmengmian"
          },
          "path": "manifest",
          "name": "manifest",
          "description": "manifest",
          "status": "开始",
          "ssh_url_to_repo": "git@gitcode.com:dengmengmian/manifest.git",
          "http_url_to_repo": "https://gitcode.com/dengmengmian/manifest.git",
          "web_url": "https://gitcode.com/dengmengmian/manifest",
          "homepage": "https://gitcode.com/dengmengmian/manifest",
          "members": ["dengmengmian"],
          "assignee": [
            {
              "id": "268",
              "login": "dengmengmian",
              "name": "麻凡",
              "avatar_url": "https://cdn-img.gitcode.com/ec/fb/430ecf07b9ee91bbbbf341d92a36783d06e69086f82ce8cf5a6406f79f1c9cf4.png",
              "html_url": "https://gitcode.com/dengmengmian",
              "type": "User"
            }
          ],
          "forks_count": 0,
          "stargazers_count": 0,
          "project_labels": [],
          "relation": "master",
          "permission": {
            "pull": true,
            "push": true,
            "admin": true
          },
          "internal": false,
          "open_issues_count": 0,
          "has_issue": false,
          "watched": false,
          "watchers_count": 0,
          "assignees_number": 1,
          "enterprise": {
            "id": 199940,
            "path": "dengmengmian",
            "html_url": "https://gitcode.com/dengmengmian",
            "type": "user"
          },
          "default_branch": "master",
          "fork": false,
          "owner": {
            "id": "268",
            "login": "dengmengmian",
            "name": "麻凡",
            "type": "User"
          },
          "assigner": {
            "id": "268",
            "login": "dengmengmian",
            "name": "麻凡",
            "type": "User"
          },
          "issue_template_source": "project",
          "private": false,
          "public": true,
          "gitee": {
            "star": 10,
            "fork": 15,
            "watch": 1
          }
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/users/dengmengmian/repos?access_token=yuBy&type=all&sort=full_name&page=1&pre_page=20'


6. Create a personal project repository
---------------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/user/repos``


Parameters
~~~~~~~~~~

+-----------------------+-----------------------+----------+-----------+
| Parameter             | Description           | Type     | Data Type |
+=======================+=======================+==========+===========+
| access_token\*        | personal access token | query    | string    |
+-----------------------+-----------------------+----------+-----------+
| name\*                | Repository Name       | formData | string    |
+-----------------------+-----------------------+----------+-----------+
| description           | Repository            | formData | string    |
|                       | Description           |          |           |
+-----------------------+-----------------------+----------+-----------+
| has_issues            | Allow Issues to Be    | formData | boolean   |
|                       | Created               |          |           |
|                       | (Enabled/Disabled).   |          |           |
|                       | Default: true         |          |           |
+-----------------------+-----------------------+----------+-----------+
| has_wiki              | Provide Wiki          | formData | boolean   |
|                       | (Enabled/Disabled).   |          |           |
|                       | Default: true         |          |           |
+-----------------------+-----------------------+----------+-----------+
| auto_init             | If the value is true, | formData | boolean   |
|                       | the repository will   |          |           |
|                       | be initialized with a |          |           |
|                       | README. Default: Not  |          |           |
|                       | Initialized (false)   |          |           |
+-----------------------+-----------------------+----------+-----------+
| gitignore_template    | gitignore template    | formData | string    |
+-----------------------+-----------------------+----------+-----------+
| license_template      | license template      | formData | string    |
+-----------------------+-----------------------+----------+-----------+
| path                  | Repository Path       | formData | string    |
+-----------------------+-----------------------+----------+-----------+
| private               | Is Private            | formData | boolean   |
+-----------------------+-----------------------+----------+-----------+
| default_branch        | Default Branch Name   | formData | string    |
|                       | when Initializing a   |          |           |
|                       | Repository.Default:   |          |           |
|                       | main                  |          |           |
+-----------------------+-----------------------+----------+-----------+

\*表示必填项。


Response
~~~~~~~~

返回 “success” 表示成功，其他为失败

.. container:: highlight

   .. code:: text

      {
        "id": 4106383,
        "full_name": "dengmengmian/wunian-prj",
        "human_name": "dengmengmian / wunian-prj",
        "url": "https://api.gitcode.com/api/v5/user/repos",
        "namespace": {
          "id": 199940,
          "name": "dengmengmian",
          "path": "dengmengmian",
          "develop_mode": "normal",
          "kind": "user",
          "full_path": "dengmengmian",
          "full_name": "dengmengmian",
          "visibility_level": 20,
          "enable_file_control": false,
          "owner_id": 268
        },
        "path": "wunian-prj",
        "name": "wunian-prj",
        "description": "wunian-prj",
        "private": true,
        "public": false,
        "visibility": "private"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request POST 'https://api.gitcode.com/api/v5/user/repos?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data-raw '{
        "name": "wunian-prj",
        "description": "wunian-prj",
        "has_issues": true,
        "has_wiki": true,
        "can_comment": true,
        "public": 0,
        "private": true,
        "auto_init": true,
        "gitignore_template": "string",
        "license_template": "string",
        "path": "wunian-prj"
      }'


7. List all repositories of the authorized user
-----------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/user/repos``


Parameters
~~~~~~~~~~

+----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------+-----------+
| Parameter      | Description                                                                                                                                                                                                                                                                       | Type  | Data Type |
+================+===================================================================================================================================================================================================================================================================================+=======+===========+
| access_token\* | personal access token                                                                                                                                                                                                                                                             | query | string    |
+----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------+-----------+
| visibility     | 公开(public)、私有(private)或者所有(all)，Default: 所有(all)                                                                                                                                                                                                                      | query | string    |
+----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------+-----------+
| affiliation    | owner(授权用户拥有的仓库)、collaborator(授权用户为仓库成员)、organization_member(授权用户为仓库所在组织并有访问仓库权限)、enterprise_member(授权用户所在企业并有访问仓库权限)、admin(所有有权限的，包括所管理的组织中所有仓库、所管理的企业的所有仓库)。可以用逗号分隔符组合。如: | query | string    |
|                | owner, organization_member 或 owner, collaborator, organization_member                                                                                                                                                                                                            |       |           |
+----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------+-----------+
| type           | 筛选用户仓库: 其创建(owner)、个人(personal)、其为成员(member)、公开(public)、私有(private)，不能与 affiliation 参数一并使用，否则会报 422 错误，与visibility参数一起使用，visibility参数拥有更高的优先级                                                                          | query | string    |
+----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------+-----------+
| sort           | 排序方式: 创建时间(created)，update time(updated)，最后推送时间(pushed)，仓库所属与名称(full_name)。Default: full_name                                                                                                                                                            | query | string    |
+----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------+-----------+
| direction      | 如果sort参数为full_name，用升序(asc)。否则降序(desc)                                                                                                                                                                                                                              | query | string    |
+----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------+-----------+
| q              | keywords                                                                                                                                                                                                                                                                          | query | string    |
+----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------+-----------+
| page           | Current Page Number                                                                                                                                                                                                                                                               | query | int       |
+----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum 100,default:20 100                                                                                                                                                                                                                                        | query | int       |
+----------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------+-----------+

\*表示必填项。


Response
~~~~~~~~

返回 “success” 表示成功，其他为失败

.. container:: highlight

   .. code:: text

      [
        {
          "id": 4028329,
          "full_name": "tiandi/test_yf_repo",
          "human_name": "洪门 / test_yf_repo",
          "url": "https://api.gitcode.com/api/v5/repos/tiandi/test_yf_repo",
          "namespace": {
            "id": 1420034,
            "type": "enterprise",
            "name": "洪门",
            "path": "tiandi",
            "html_url": "https://gitcode.com/tiandi"
          },
          "path": "test_yf_repo",
          "name": "test_yf_repo",
          "description": "",
          "status": "开始",
          "ssh_url_to_repo": "git@gitcode.com:tiandi/test_yf_repo.git",
          "http_url_to_repo": "https://gitcode.com/tiandi/test_yf_repo.git",
          "web_url": "https://gitcode.com/tiandi/test_yf_repo",
          "homepage": "https://gitcode.com/tiandi/test_yf_repo",
          "members": ["aron1"],
          "assignee": [
            {
              "id": "332008",
              "login": "aron1",
              "name": "yanfan",
              "avatar_url": "https://cdn-img.gitcode.com/bd/ca/0115343247b338d0c53589a145501e84a58464272f2fb09b372cc3d2311b2b39.png?time=1722525295285",
              "html_url": "https://gitcode.com/aron1",
              "type": "User"
            }
          ],
          "forks_count": 0,
          "stargazers_count": 0,
          "project_labels": [],
          "relation": "master",
          "permission": {
            "pull": true,
            "push": true,
            "admin": true
          },
          "internal": false,
          "open_issues_count": 0,
          "has_issue": false,
          "watched": false,
          "watchers_count": 0,
          "assignees_number": 1,
          "enterprise": {
            "id": 1420034,
            "path": "tiandi",
            "html_url": "https://gitcode.com/tiandi",
            "type": "enterprise"
          },
          "default_branch": "main",
          "fork": false,
          "owner": {
            "id": "444601",
            "login": "yanfan",
            "name": "yanfan是随时随地送达啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊实打实",
            "type": "User"
          },
          "assigner": {
            "id": "444601",
            "login": "yanfan",
            "name": "yanfan是随时随地送达啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊啊实打实",
            "type": "User"
          },
          "private": true,
          "public": false
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/user/repos?access_token={your-token}&visibility=private&affiliation=owner%2Ccollaborator%2Corganization_member&sort=created&direction=desc&q=yf&page=1&per_page=2'


8. Get a specific repository of a user
--------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}``

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

      {
          "id": 4250980,
          "full_name": "aron1/Model10123001",
          "human_name": "aron1 / Model10123001tewteewtewteewtewteewtewteewtewteewtewteewtewteewtewteewtewteewtewteewtewteewtewteewtew",
          "url": "https://api.gitcode.com/api/v5/repos/aron1/Model10123001",
          "namespace": {
              "id": 1364544,
              "name": "aron1",
              "path": "aron1",
              "html_url": "https://gitcode.com/aron1"
          },
          "path": "Model10123001",
          "name": "Model10123001tewteewtewteewtewteewtewteewtewteewtewteewtewteewtewteewtewteewtewteewtewteewtewteewtew",
          "description": "",
          "status": "关闭",
          "ssh_url_to_repo": "git@gitcode.com:aron1/Model10123001.git",
          "http_url_to_repo": "https://gitcode.com/aron1/Model10123001.git",
          "web_url": "https://gitcode.com/aron1/Model10123001",
          "readme_url": "https://gitcode.com/aron1/Model10123001/blob/main/README.md",
          "created_at": "2024-10-22T22:14:06.922+08:00",
          "updated_at": "2024-12-02T18:37:23.426+08:00",
          "creator": {
              "id": "660ba866683c570b25be06c8",
              "arts_id": "332008",
              "username": "aron1",
              "nickname": "yanfan",
              "email": "aron1@noreply.gitcode.com",
              "photo": "https://cdn-img.gitcode.com/bd/ca/0115343247b338d0c53589a145501e84a58464272f2fb09b372cc3d2311b2b39.png?time=1722525295285"
          },
          "members": [
              "aron1"
          ],
          "forks_count": 0,
          "stargazers_count": 1,
          "project_labels": [],
          "license": "Apache_License_v2.0",
          "internal": false,
          "open_issues_count": 0,
          "watchers_count": 0,
          "assignees_number": 0,
          "enterprise": {
              "id": 1364544,
              "path": "aron1",
              "html_url": "https://gitcode.com/aron1",
              "type": "user"
          },
          "default_branch": "main",
          "fork": false,
          "owner": {
              "id": "332008",
              "login": "aron1",
              "name": "yanfan",
              "type": "User"
          },
          "assigner": {
              "id": "332008",
              "login": "aron1",
              "name": "yanfan",
              "type": "User"
          },
          "issue_template_source": "project",
          "private": true,
          "public": false
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang/test?access_token=?'


9. Add a public key
-------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/user/keys``


Parameters
~~~~~~~~~~

============== ===================== ===== =========
Parameter      Description           Type  Data Type
============== ===================== ===== =========
access_token\* personal access token query string
key\*          Public Key Content    body  string
title\*        Public Key Name       body  string
============== ===================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 311915,
        "title": "555555",
        "key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIa6IyTGuI8V5wrhANDFyezQqL73dY9ctLGHgpOggp7E Gitee",
        "created_at": "2024-11-14T03:34:40.318+00:00",
        "url": "https://api.gitcode.com/v5/user/keys/311915"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/user/keys?access_token=?' \
      --header 'Content-Type: application/json;charset=UTF-8' \
      --data '{
          "key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIa6IyTGuI8V5wrhANDFyezQqL73dY9ctLGHgpOggp7E Gitee SSH Key",
          "title": "555555"
      }'


10. List all public keys of the authorized user
-----------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/user/keys``


Parameters
~~~~~~~~~~

============== ====================================== ===== =========
Parameter      Description                            Type  Data Type
============== ====================================== ===== =========
access_token\* personal access token                  query string
page           Current Page Number                    query int
per_page       Items Per Page, Maximum 100,default:20 query int
============== ====================================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 308357,
          "title": "xiaogang@csdn.net\r\n",
          "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCwT9UXXtGfLa16tbxV+0RQ6m+BaAG2wJvqApr+juVNEmnM0lKNt1tyxY/V9SsCRf38UprPLTp71+btRpFIH9TLrGhkvT3tJOouYDXVUpSaigi7OO+6eLc+Cn0TZSLj4RmwVe/w93kmsCUzgqkeHk14K3S+2oCCm1rbpBAvpPhSKHhAH9LcTBecDoZ+NA2dsEDyfsloVH5cMJQO9n2W1QYduMuuaVHHpehSdDohN7cDI799Rwofaqqyz6ZJrc6eBjSVi1W+JPDTT6NW0+eFBYXo3KWybffixH4cAWdbS1Ms5Pe9Xh+G4WqFuhFh9zCoXlRUUrArLo5pYfpy5gv4iUVmniM0Pb0/Y5x8RJyGaPdS/2c68s8LQsm/9Ees8aeE5TcT5isDEvh+wy7jp1xi5nONk9QvOy7EdYYeHQtkw/0rklsz7UvAIjjHObNNYpY6RLQRT+dqN/lAb7stT047FSxqcNMCX/cybapLygs1y2ClcgU42p16RfgCH0NKA5emRhM= xiaogang@csdn.net",
          "created_at": "2024-07-23T10:29:42.119+00:00",
          "url": "https://api.gitcode.com/v5/user/keys/308357"
        },
        {
          "id": 311915,
          "title": "555555",
          "key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIa6IyTGuI8V5wrhANDFyezQqL73dY9ctLGHgpOggp7E Gitee",
          "created_at": "2024-11-14T03:34:40.318+00:00",
          "url": "https://api.gitcode.com/v5/user/keys/311915"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/user/keys?access_token=?'


11. Delete a public key
-----------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/user/keys/{id}``


Parameters
~~~~~~~~~~

============== ===================== ===== =========
Parameter      Description           Type  Data Type
============== ===================== ===== =========
access_token\* personal access token query string
id\*           Public Key ID         path  string
============== ===================== ===== =========


Response
~~~~~~~~

无


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/user/keys/311914?access_token=?'


12. Get a specific public key
-----------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/user/keys/{id}``


Parameters
~~~~~~~~~~

============== ===================== ===== =========
Parameter      Description           Type  Data Type
============== ===================== ===== =========
access_token\* personal access token query string
id\*           Public Key ID         path  string
============== ===================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 308357,
          "title": "xiaogang@csdn.net\r\n",
          "key": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCwT9UXXtGfLa16tbxV+0RQ6m+BaAG2wJvqApr+juVNEmnM0lKNt1tyxY/V9SsCRf38UprPLTp71+btRpFIH9TLrGhkvT3tJOouYDXVUpSaigi7OO+6eLc+Cn0TZSLj4RmwVe/w93kmsCUzgqkeHk14K3S+2oCCm1rbpBAvpPhSKHhAH9LcTBecDoZ+NA2dsEDyfsloVH5cMJQO9n2W1QYduMuuaVHHpehSdDohN7cDI799Rwofaqqyz6ZJrc6eBjSVi1W+JPDTT6NW0+eFBYXo3KWybffixH4cAWdbS1Ms5Pe9Xh+G4WqFuhFh9zCoXlRUUrArLo5pYfpy5gv4iUVmniM0Pb0/Y5x8RJyGaPdS/2c68s8LQsm/9Ees8aeE5TcT5isDEvh+wy7jp1xi5nONk9QvOy7EdYYeHQtkw/0rklsz7UvAIjjHObNNYpY6RLQRT+dqN/lAb7stT047FSxqcNMCX/cybapLygs1y2ClcgU42p16RfgCH0NKA5emRhM= xiaogang@csdn.net",
          "created_at": "2024-07-23T10:29:42.119+00:00",
          "url": "https://api.gitcode.com/v5/user/keys/308357"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location  'https://api.gitcode.com/api/v5/user/keys/311914?access_token=?'


13. Obtain a namespace for authorized users
-------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/user/namespace?access_token=?``


Parameters
~~~~~~~~~~

============== ===================== ===== =========
Parameter      Description           Type  Data Type
============== ===================== ===== =========
access_token\* personal access token query string
path\*         Namespace path        query string
============== ===================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "id": 138108,
          "path": "xiaogang_test",
          "name": "aaasfd/sda/fsdaf/sdfsa",
          "html_url": "https://gitcode.com/xiaogang_test",
          "type": "group"
      }

Response Fields Description
^^^^^^^^^^^^^^^^^^^^^^^^^^^

============ ======= ========================
Field        Type    Description
============ ======= ========================
``id``       integer Namespace Id
``path``     string  Namespace path
``name``     string  Namespace name
``html_url`` string  Namespace access address
``type``     string  Namespace type
============ ======= ========================


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location  'GET https://api.gitcode.com/api/v5/user/namespace?access_token=?&path=xiaogang_test'


14. List the repository where authorized user star has been listed
------------------------------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/user/starred??access_token=?``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| sort           | created/last_push Sort by       | query | string    |
|                | warehouse creation time         |       |           |
|                | (created) or last push time     |       |           |
|                | (updated), default: creation    |       |           |
|                | time                            |       |           |
+----------------+---------------------------------+-------+-----------+
| direction      | asc/desc, Sort direction,       | query | string    |
|                | default: descending order       |       |           |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number             | query | int       |
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
              "id": 777621,
              "full_name": "xiaogang/private-new2",
              "human_name": "xiaogang / private-new2",
              "url": "https://api.gitcode.com/api/v5/repos/xiaogang/private-new2",
              "namespace": {
                  "id": 137117,
                  "type": "user",
                  "name": "xiaogang",
                  "path": "xiaogang",
                  "html_url": "https://gitcode.com/xiaogang"
              },
              "path": "private-new2",
              "name": "private-new2",
              "parentfull_name": "xiaogang_test/private-new",
              "description": "特朗普",
              "status": "开始",
              "ssh_url_to_repo": "ssh://git@gitcode.com:2222/xiaogang/private-new2.git",
              "http_url_to_repo": "https://gitcode.com/xiaogang/private-new2.git",
              "web_url": "https://gitcode.com/xiaogang/private-new2",
              "created_at": "2024-12-11T17:41:14.536+08:00",
              "updated_at": "2024-12-11T17:41:14.536+08:00",
              "homepage": "https://gitcode.com/xiaogang/private-new2",
              "members": [
                  "xiaogang"
              ],
              "parent": {
                  "full_name": "xiaogang_test/private-new",
                  "human_name": "xiaogang_test / private-new"
              },
              "forks_count": 0,
              "stargazers_count": 1,
              "relation": "master",
              "permission": {
                  "pull": true,
                  "push": true,
                  "admin": true
              },
              "internal": false,
              "open_issues_count": 0,
              "has_issue": false,
              "has_issues": false,
              "watchers_count": 0,
              "enterprise": {
                  "id": 137117,
                  "path": "xiaogang",
                  "html_url": "https://gitcode.com/xiaogang",
                  "type": "user"
              },
              "default_branch": "main",
              "fork": true,
              "pushed_at": "2024-12-20T19:14:34.979+08:00",
              "owner": {
                  "id": "496",
                  "login": "xiaogang",
                  "name": "肖刚",
                  "type": "User"
              },
              "issue_template_source": "project",
              "project_creator": "xiaogang",
              "private": false,
              "public": true
          }
      ]


Response Fields Description
^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------------------------+---------+-----------------------------+
| Field                       | Type    | Description                 |
+=============================+=========+=============================+
| ``id``                      | integer | Repository Id               |
+-----------------------------+---------+-----------------------------+
| ``full_name``               | string  | Full path of the repository |
+-----------------------------+---------+-----------------------------+
| ``human_name``              | string  | Full name of the repository |
+-----------------------------+---------+-----------------------------+
| ``url``                     | string  | URL to access repository    |
+-----------------------------+---------+-----------------------------+
| ``path``                    | string  | Repository path             |
+-----------------------------+---------+-----------------------------+
| ``name``                    | string  | Repository name             |
+-----------------------------+---------+-----------------------------+
| ``parentfull_name``         | string  | Full name of the parent     |
|                             |         | repository                  |
+-----------------------------+---------+-----------------------------+
| ``description``             | string  | Repository description      |
+-----------------------------+---------+-----------------------------+
| ``status``                  | string  | Repository status           |
+-----------------------------+---------+-----------------------------+
| ``ssh_url_to_repo``         | string  | SSH URL to the repository   |
+-----------------------------+---------+-----------------------------+
| ``http_url_to_repo``        | string  | HTTP URL to the repository  |
+-----------------------------+---------+-----------------------------+
| ``web_url``                 | string  | Web URL to access the       |
|                             |         | repository                  |
+-----------------------------+---------+-----------------------------+
| ``created_at``              | string  | Repository creation time    |
+-----------------------------+---------+-----------------------------+
| ``updated_at``              | string  | Repository last update time |
+-----------------------------+---------+-----------------------------+
| ``homepage``                | string  | Repository homepage         |
+-----------------------------+---------+-----------------------------+
| ``members``                 | array   | Members of the repository   |
+-----------------------------+---------+-----------------------------+
| ``forks_count``             | integer | Number of forks             |
+-----------------------------+---------+-----------------------------+
| ``stargazers_count``        | integer | Number of stars             |
+-----------------------------+---------+-----------------------------+
| ``relation``                | string  | Current user’s role         |
|                             |         | relative to the repository  |
+-----------------------------+---------+-----------------------------+
| ``permission``              | object  | User permissions            |
+-----------------------------+---------+-----------------------------+
| ``internal``                | boolean | Whether it is an internal   |
|                             |         | open-source repository      |
+-----------------------------+---------+-----------------------------+
| ``open_issues_count``       | integer | Number of open issue        |
+-----------------------------+---------+-----------------------------+
| ``has_issues``              | boolean | Whether issue functionality |
|                             |         | is enabled                  |
+-----------------------------+---------+-----------------------------+
| ``watchers_count``          | integer | Number of watchers          |
+-----------------------------+---------+-----------------------------+
| ``default_branch``          | string  | Default branch              |
+-----------------------------+---------+-----------------------------+
| ``fork``                    | boolean | Whether it is a forked      |
|                             |         | repository                  |
+-----------------------------+---------+-----------------------------+
| ``pushed_at``               | string  | Time of the last code push  |
+-----------------------------+---------+-----------------------------+
| ``issue_template_source``   | string  | Source of the issue         |
|                             |         | template project: Use the   |
|                             |         | repository’s Issue Template |
|                             |         | as a template; enterprise:  |
|                             |         | Use enterprise work items   |
|                             |         | as a template               |
+-----------------------------+---------+-----------------------------+
| ``project_creator``         | string  | Creator of the repository   |
+-----------------------------+---------+-----------------------------+
| ``private``                 | boolean | Whether it is a private     |
|                             |         | repository                  |
+-----------------------------+---------+-----------------------------+
| ``public``                  | boolean | Whether it is a public      |
|                             |         | repository                  |
+-----------------------------+---------+-----------------------------+
| ``namespace``               | object  | Namespace to which the      |
|                             |         | repository belongs          |
+-----------------------------+---------+-----------------------------+
| ``parent``                  | object  | Information about the       |
|                             |         | parent repository (if any)  |
+-----------------------------+---------+-----------------------------+
| ``enterprise``              | object  | Enterprise information of   |
|                             |         | the repository              |
+-----------------------------+---------+-----------------------------+
| ``owner``                   | object  | Information about the       |
|                             |         | repository owner            |
+-----------------------------+---------+-----------------------------+


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location  'GET https://api.gitcode.com/api/v5/user/namespace?access_token=?&path=xiaogang_test'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/users/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
