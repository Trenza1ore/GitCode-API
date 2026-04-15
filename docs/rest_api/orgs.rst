Organization API
================


1. List the organizations a user belongs to
-------------------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/users/{username}/orgs``

Parameters
~~~~~~~~~~

============== ============================== ===== =========
Parameter      Description                    Type  Data Type
============== ============================== ===== =========
access_token\* personal access token          query string
username\*     username(username/login)       path  string
page           Current Page Number，default:1 query string
per_page       Items Per Page,maximum is 100  query string
============== ============================== ===== =========

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 133039,
          "login": "openharmony",
          "name": "OpenHarmony",
          "avatar_url": null,
          "repos_url": null,
          "events_url": null,
          "members_url": null,
          "description": "OpenHarmony是由开放原子开源基金会（OpenAtom Foundation）孵化及运营的开源项目，目标是面向全场景、全连接、全智能时代，搭建一个智能终端设备操作系统的框架和平台，促进万物互联产业的繁荣发展。",
          "follow_count": 3
        }
      ]

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/users/user1/orgs?access_token=xxx'


2. List the organizations an authorized user belongs to
-------------------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/users/orgs``


Parameters
~~~~~~~~~~

============== ============================== ===== =========
Parameter      Description                    Type  Data Type
============== ============================== ===== =========
access_token\* personal access token          query string
page           Current Page Number，default:1 query string
per_page       Items Per Page, maximum is 100 query string
admin          Filter by Admin Permissions    query boolean
============== ============================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 133039,
          "login": "openharmony",
          "path": "openharmony",
          "name": "OpenHarmony",
          "avatar_url": null,
          "repos_url": null,
          "events_url": null,
          "members_url": null,
          "description": "OpenHarmony是由开放原子开源基金会（OpenAtom Foundation）孵化及运营的开源项目，目标是面向全场景、全连接、全智能时代，搭建一个智能终端设备操作系统的框架和平台，促进万物互联产业的繁荣发展。",
          "follow_count": 3
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/users/orgs?access_token=xxx'


3. Get details of an organization member
----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/orgs/{org}/members/{username}``


Parameters
~~~~~~~~~~

============== ============================== ===== =========
Parameter      Description                    Type  Data Type
============== ============================== ===== =========
access_token\* personal access token          query string
org\*          Organization Path (path/login) path  string
username\*     username(username/login)       path  string
============== ============================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 133039,
        "path": "openharmony",
        "name": "",
        "url": "",
        "avatar_url": null,
        "user": {
          "id": "64dc3b13b8b9504cec223ab1",
          "login": "theo6789",
          "name": "TheoCui",
          "avatar_url": null,
          "html_url": "https://gitcode.com/theo6789"
        }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/orgs/xiaogang_test/members/xiapgang?access_token=xxx'


4. Get information about an organization
----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/orgs/{org}``


Parameters
~~~~~~~~~~

============== ============================== ===== =========
Parameter      Description                    Type  Data Type
============== ============================== ===== =========
access_token\* personal access token          query string
org\*          Organization Path (path/login) path  string
============== ============================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 6486504,
        "login": "openharmony",
        "name": "OpenHarmony",
        "avatar_url": "",
        "repos_url": "https://api.gitcode.com/openharmony/repos",
        "events_url": "https://api.gitcode.com/openharmony/events",
        "members_url": "https://api.gitcode.com/openharmony/members{/member}",
        "description": "OpenHarmony是由开放原子开源基金会（OpenAtom Foundation）孵化及运营的开源项目，目标是面向全场景、全连接、全智能时代，搭建一个智能终端设备操作系统的框架和平台，促进万物互联产业的繁荣发展。\r\n",
        "enterprise": "openharmony",
        "follow_count": 40819,
        "gitee": {
          "follows": 43454
        }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/orgs/xiaogang_test?access_token=xxx'


5. Get the repo list of an organization
---------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/orgs/{org}/repos``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| org\*          | Organization Path (path/login)  | path  | string    |
+----------------+---------------------------------+-------+-----------+
| type           | Filter Repository by Type,      | query | string    |
|                | which can be: all, public,      |       |           |
|                | private. Default: all           |       |           |
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
          "id": 29724198,
          "full_name": "openharmony/.gitee",
          "namespace": {
            "id": 6486504,
            "type": "group",
            "name": "OpenHarmony",
            "path": "openharmony",
            "html_url": "https://gitcode.com/openharmony"
          },
          "path": ".gitee",
          "name": ".gitee",
          "description": "",
          "private": false,
          "public": true,
          "internal": false,
          "fork": false,
          "html_url": "https://gitcode.com/openharmony/.gitee.git",
          "forks_count": 4,
          "stargazers_count": 0,
          "watchers_count": 1,
          "default_branch": "master",
          "open_issues_count": 0,
          "license": null,
          "project_creator": "landwind",
          "pushed_at": "2024-02-06T18:25:26+08:00",
          "created_at": "2023-06-16T10:55:42+08:00",
          "updated_at": "2024-03-29T14:59:46+08:00",
          "status": "开始"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/orgs/xiaogang_test/repos?access_token=xxx'


6. Create a repository for an organization
------------------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/orgs/{org}/repos``

+-----------------------+-----------------------+----------+-----------+
| Parameter             | Description           | Type     | Data Type |
+=======================+=======================+==========+===========+
| access_token\*        | personal access token | query    | string    |
+-----------------------+-----------------------+----------+-----------+
| org\*                 | Organization Path     | path     | string    |
|                       | (path/login)          |          |           |
+-----------------------+-----------------------+----------+-----------+
| name\*                | Repository Name       | body     | string    |
+-----------------------+-----------------------+----------+-----------+
| description           | Repository            | body     | string    |
|                       | Description           |          |           |
+-----------------------+-----------------------+----------+-----------+
| homepage              | homepage              | body     | string    |
+-----------------------+-----------------------+----------+-----------+
| has_issues            | Allow Issues to Be    | body     | boolean   |
|                       | Created               |          |           |
|                       | (Enabled/Disabled).   |          |           |
|                       | Default: true         |          |           |
+-----------------------+-----------------------+----------+-----------+
| has_wiki              | Provide Wiki          | body     | boolean   |
|                       | (Enabled/Disabled).   |          |           |
|                       | Default: true         |          |           |
+-----------------------+-----------------------+----------+-----------+
| can_comment           | Allow Users to        | body     | boolean   |
|                       | Comment on            |          |           |
|                       | Repositories.         |          |           |
|                       | Default: true         |          |           |
+-----------------------+-----------------------+----------+-----------+
| public                | Repository Open       | body     | int       |
|                       | Source Type: 0        |          |           |
|                       | (Private), 1          |          |           |
|                       | (External Open        |          |           |
|                       | Source), 2 (Internal  |          |           |
|                       | Open Source). Note:   |          |           |
|                       | This is mutually      |          |           |
|                       | exclusive with        |          |           |
|                       | private and is        |          |           |
|                       | primarily based on    |          |           |
|                       | public                |          |           |
+-----------------------+-----------------------+----------+-----------+
| private               | Repository Visibility | body     | boolean   |
|                       | (Public or Private).  |          |           |
|                       | Default: Public       |          |           |
|                       | (false) . Note: This  |          |           |
|                       | is mutually exclusive |          |           |
|                       | with public and is    |          |           |
|                       | primarily based on    |          |           |
|                       | public.               |          |           |
+-----------------------+-----------------------+----------+-----------+
| auto_init             | If the value is true, | body     | boolean   |
|                       | the repository will   |          |           |
|                       | be initialized with a |          |           |
|                       | README. Default: Not  |          |           |
|                       | Initialized (false)   |          |           |
+-----------------------+-----------------------+----------+-----------+
| gitignore_template    | gitignore template    | body     | string    |
+-----------------------+-----------------------+----------+-----------+
| license_template      | license template      | body     | string    |
+-----------------------+-----------------------+----------+-----------+
| path                  | Repository Path       | body     | string    |
+-----------------------+-----------------------+----------+-----------+
| default_branch        | Default Branch Name   | formData | string    |
|                       | when Initializing a   |          |           |
|                       | Repository.Default:   |          |           |
|                       | main                  |          |           |
+-----------------------+-----------------------+----------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 34171993,
        "full_name": "daming_1/test_create_project_2",
        "human_name": "daming/test_create_project_2",
        "url": "https://gitcode.com/api/v5/repos/daming_1/test_create_project_2",

        "path": "test_create_project_2",
        "name": "test_create_project_2",

        "description": "Description",
        "private": false,
        "public": true,
        "namespace": {
          "id": 74962,
          "name": "group1111",
          "path": "group11111",
          "develop_mode": "normal",
          "region": null,
          "cell": "default",
          "kind": "group",
          "full_path": "group11111",
          "full_name": "group1111",
          "parent_id": null,
          "visibility_level": 20,
          "enable_file_control": false,
          "owner_id": null
        },
        "empty_repo": null,
        "starred": null,
        "visibility": "public",
        "owner": null,
        "creator": null,
        "forked_from_project": null,
        "item_type": null,
        "main_repository_language": null,
        "homepage": "http://www.baidi.com"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request POST 'https://api.gitcode.com/api/v5/orgs/xiaogang_test/repos?access_token=xxx'
      --header 'Content-Type: application/json' \
      --data-raw '{
          "name": "test"
      }'


7. Get a specific member of a enterprise
----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/enterprises/{enterprise}/members/{username}``


Parameters
~~~~~~~~~~

============== =========================== ===== =========
Parameter      Description                 Type  Data Type
============== =========================== ===== =========
access_token\* personal access token       query string
enterprise\*   Enterprise Path(path/login) path  string
username\*     username(username/login)    path  string
============== =========================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "user": {
          "avatar_url": "https://cdn-img.gitcode.com/ec/fb/430ecf07b9ee91bbbbf341d92a36783d06e69086f82ce8cf5a6406f79f1c9cf4.png",
          "html_url": "https://gitcode.com/dengmengmian",
          "id": "268",
          "login": "dengmengmian",
          "name": "dengmengmian"
        },
        "url": "https://gitcode.com/dengmengmian",
        "active": true,
        "role": "admin",
        "enterprise": {
          "id": 0,
          "url": "https://gitcode.com/dengmengmian"
        }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/enterprises/go-tribe/members/dengmengmian?access_token=xxx'


8. Get the member profile of an authorized user in an organization
------------------------------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/user/memberships/orgs/{org}``


Parameters
~~~~~~~~~~

============== =========================== ===== =========
Parameter      Description                 Type  Data Type
============== =========================== ===== =========
access_token\* personal access token       query string
org\*          Enterprise Path(path/login) path  string
============== =========================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 1783195,
        "path": "Go-Tribe",
        "name": "gotribe",
        "url": "https://gitcode.com/Go-Tribe",
        "avatar_url": "https://cdn-img.gitcode.com/bb/eb/b3b4e25b54add3c80961d3ba2e3724d03998eae467c99ab898ea39e48cb1b4f6.png?time1717675394237",
        "user": {
          "id": "650d67fbae6d795139b49b41",
          "login": "dengmengmian",
          "name": "麻凡",
          "avatar_url": "https://cdn-img.gitcode.com/ec/fb/430ecf07b9ee91bbbbf341d92a36783d06e69086f82ce8cf5a6406f79f1c9cf4.png",
          "html_url": "https://gitcode.com/dengmengmian"
        },
        "active": true,
        "role": "admin",
        "organization": {
          "id": 1783195,
          "login": "Go-Tribe",
          "name": "gotribe"
        }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/user/memberships/orgs/go-tribe?access_token=xxx'


9.List all members of an organization
-------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/orgs/{org}/members``


Parameters
~~~~~~~~~~

============== ======================================== ===== =========
Parameter      Description                              Type  Data Type
============== ======================================== ===== =========
access_token\* personal access token                    query string
org\*          Enterprise Path(path/login)              path  string
page           Current Page Number，default:1           query int
per_page       Items Per Page, Maximum 100,default:20   query int
role           Filter Members by Role(all/admin/member) query string
============== ======================================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "avatar_url": "https://cdn-img.gitcode.com/ec/fb/430ecf07b9ee91bbbbf341d92a36783d06e69086f82ce8cf5a6406f79f1c9cf4.png",
          "followers_url": "https://api.gitcode.com/api/v5users/dengmengmian/followers",
          "html_url": "https://gitcode.com/dengmengmian",
          "id": "268",
          "login": "dengmengmian",
          "member_role": "admin",
          "name": "麻凡",
          "type": "User",
          "url": "https://api.gitcode.com/api/v5/dengmengmian"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/orgs/go-tribe/members?access_token=xxxx&page=1&pre_page=10&role=all'


10. List all members of a enterprise
------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/enterprises/{enterprise}/members``


Parameters
~~~~~~~~~~

============== ======================================== ===== =========
Parameter      Description                              Type  Data Type
============== ======================================== ===== =========
access_token\* personal access token                    query string
org\*          Enterprise Path(path/login)              path  string
page           Current Page Number，default:1           query int
per_page       Items Per Page, Maximum 100,default:20   query int
role           Filter Members by Role(all/admin/member) query string
============== ======================================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "user": {
            "avatar_url": "https://cdn-img.gitcode.com/ec/fb/430ecf07b9ee91bbbbf341d92a36783d06e69086f82ce8cf5a6406f79f1c9cf4.png",
            "html_url": "https://gitcode.com/dengmengmian",
            "id": "268",
            "login": "dengmengmian",
            "name": "麻凡",
            "url": "https://api.gitcode.com/api/v5/dengmengmian"
          },
          "url": "https://api.gitcode.com/api/v5/enterprises/go-tribe/members/dengmengmian",
          "active": true,
          "role": "admin"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/enterprises/go-tribe/members?access_token=yuBy&page=1&pre_page=10&role=all'


11. Remove a member from an organization managed by the authorized user
-----------------------------------------------------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/orgs/{org}/memberships/{username}``


Parameters
~~~~~~~~~~

============== ============================== ===== =========
Parameter      Description                    Type  Data Type
============== ============================== ===== =========
access_token\* personal access token          query string
org\*          Organization Path (path/login) path  string
username\*     username(username/login)       path  string
============== ============================== ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {}


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/orgs/tiandi/memberships/yinlin?access_token=******'


12. List all followers of a specific organization
-------------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/orgs/{owner}/followers``


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
          "id": 496,
          "login": "xiaogang",
          "name": "xiaogang",
          "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/bc/cd/6bc422546cdf276c147f267030d83a43e927fec67ca66f0b22f7e03556206fa3.jpg",
          "watch_at": "2024-11-13T16:15:53.287+08:00"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/orgs/xiaogang_test/followers' \
      --header 'PRIVATE-TOKEN: your_token'


13. Get extended issue configuration
------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/orgs/{org}/issue/extend/settings``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| org\*          | Repository Ownership Path       | path  | string    |
|                | (Company or Organization Path)  |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "type_name": "需求",
              "type_id": 4,
              "type_desc": "定义和Description产品或项目中需要实现的新功能或改进",
              "status": [
                  {
                      "status_name": "未提单",
                      "status_id": 11,
                      "status_desc": "需求尚未正式提交，仍处于概念或讨论阶段，未进入系统管理流程",
                      "gitcode_issue_status": 0
                  },
                  ... ...
                  {
                      "status_name": "修复中",
                      "status_id": 20,
                      "status_desc": "需求的解决方案在实施过程中发现问题，正在进行修复工作",
                      "gitcode_issue_status": 0
                  }
              ]
          },
          ... ...
          {
              "type_name": "咨询",
              "type_id": 36138,
              "type_desc": "",
              "status": [
                  {
                      "status_name": "未提单",
                      "status_id": 11,
                      "status_desc": "需求尚未正式提交，仍处于概念或讨论阶段，未进入系统管理流程",
                      "gitcode_issue_status": 0
                  },
                  ... ...
                  {
                      "status_name": "已完成",
                      "status_id": 14,
                      "status_desc": "需求的所有相关工作已结束，成果已交付，进入归档状态",
                      "gitcode_issue_status": 1
                  }
              ]
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/orgs/openharmony/issue/extend/settings?access_token=your_token'


14. Invite an Organization Member
---------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/orgs/{org}/memberships/{username}``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| org\*          | Repository Ownership Path       | path  | string    |
|                | (Company, Organization, or      |       |           |
|                | Personal Path)                  |       |           |
+----------------+---------------------------------+-------+-----------+
| username\*     | username/login                  | path  | string    |
+----------------+---------------------------------+-------+-----------+
| permission     | Member permissions: pull        | body  | string    |
|                | code(pull), push code(push),    |       |           |
|                | maintainer(admin). Default:     |       |           |
|                | push, customized (custom role)  |       |           |
+----------------+---------------------------------+-------+-----------+
| role_id        | Role ID. Required if            | body  | string    |
|                | ‘permission’ is set to          |       |           |
|                | ‘customized’                    |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "followers_url": "https://api.gitcode.com/api/v5/users/xiaogang2/followers",
        "html_url": "https://gitcode.com/xiaogang2",
        "id": "65ffca965079ba0d1c00f6f2",
        "login": "xiaogang2",
        "name": "肖刚2",
        "type": "User",
        "url": "https://api.gitcode.com/api/v5/xiaogang2",
        "permissions": {
          "admin": false,
          "customized": true,
          "push": true,
          "pull": true
        }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location POST 'https://api.gitcode.com/api/v5/orgs/xiaogang_test/memberships/xiaogang2?access_toke=?' \
      --data '{
          "permission":"push"
          }'


15. Modify Enterprise Member Permissions
----------------------------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/enterprises/{enterprise}/members/{username}``


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
| username\*     | Username (username/login)       | path  | string    |
+----------------+---------------------------------+-------+-----------+
| role\*         | Enterprise role (viewer、       | body  | string    |
|                | tester、 developer、            |       |           |
|                | maintainer、 admin)             |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "active": true,
          "role": "member",
          "url": "https://api.gitcode.com/api/v5/enterprises/litestabc/members/malongge5",
          "user": {
              "id": 953,
              "login": "malongge5",
              "url": "https://api.gitcode.com/api/v5/malongge5",
              "html_url": "https://gitcode.com/malongge5"
          }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/enterprises/litestabc/members/malongge5?access_token=?' \
      --header 'Content-Type: application/json' \
      --data-raw '{"role":"developer"}'


16. Update the organizational information managed by authorized users
---------------------------------------------------------------------


Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/orgs/{org}?access_toke=?``


Parameters
~~~~~~~~~~

============== ================================= ========= =========
Parameter      Description                       Type      Data Type
============== ================================= ========= =========
access_token\* Personal access token             query     string
org\*          Repository Owner Path(path/login) path      string
name           Repository Owner Name             form-data string
email          Repository Owner Email            form-data string
location       Repository Owner Location         form-data string
description    Repository Owner Description      form-data string
html_url       Repository Owner Site             form-data string
============== ================================= ========= =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text


      {
          "email": "123@qq.com",
          "name": "组织",
          "description": "233333",
          "html_url": "www.baidu.com",
          "id": 138108,
          "path": "xiaogang444
      }

Response Fields Description
^^^^^^^^^^^^^^^^^^^^^^^^^^^

=============== ======= ============================
Field           Type    Description
=============== ======= ============================
``id``          integer Repository Owner Id
``path``        string  Repository Owner Path
``name``        string  Repository Owner Name
``email``       string  Repository Owner Email
``location``    string  Repository Owner Location
``description`` string  Repository Owner Description
``html_url``    string  Repository Owner Site
=============== ======= ============================


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PATCH 'https://api.gitcode.com/api/v5/orgs/test444?access_token=?' \
      --form 'name="组织"'


17. Exit an organization
------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/user/memberships/orgs/{org}?access_toke=?``


Parameters
~~~~~~~~~~

============== ================================= ===== =========
Parameter      Description                       Type  Data Type
============== ================================= ===== =========
access_token\* Personal access token             query string
org\*          Repository Owner Path(path/login) path  string
============== ================================= ===== =========


Response
~~~~~~~~

None


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/user/memberships/orgs/xiaogang_test?access_token=?' \

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/orgs/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
