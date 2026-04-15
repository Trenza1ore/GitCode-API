Search API Documentation
========================


1. Search Users
---------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/search/users``

Parameters
~~~~~~~~~~

+----------------+--------------------------------------+-------+-----------+
| Parameter      | Description                          | Type  | Data Type |
+================+======================================+=======+===========+
| access_token\* | personal access token                | query | string    |
+----------------+--------------------------------------+-------+-----------+
| page           | Current Page Number Limit: Maximum   | query | int       |
|                | 100                                  |       |           |
+----------------+--------------------------------------+-------+-----------+
| per_page       | Items per Page Limit: Maximum 50     | query | int       |
+----------------+--------------------------------------+-------+-----------+
| q\*            | keywords                             | query | string    |
+----------------+--------------------------------------+-------+-----------+
| sort           | Sorting                              | query | string    |
|                | Fields，joined_at(注册时间)，Default |       |           |
|                | Sorting: Best Match                  |       |           |
+----------------+--------------------------------------+-------+-----------+
| order          | Sorting Order (Default: desc)        | query | string    |
+----------------+--------------------------------------+-------+-----------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "avatar_url": "https://cdn-img.gitcode.com/bb/bf/b1b0bff5bafab700603248485bc4a236061f84433741855a9ce8b0c42c8.png",
              "created_at": "2024-11-15T00:00:00+08:00",
              "html_url": "https://gitcode.com/wu_com",
              "id": "25235036",
              "login": "wu_com",
              "name": "wu_com"
          },
          {
              "avatar_url": "https://cdn-img.gitcode.com/ad/ec/a8670853d9137e2c34efbc14904985a7cc5998929bfebca9ceb8626e170.png",
              "created_at": "2024-11-15T00:00:00+08:00",
              "html_url": "https://gitcode.com/wu5567488",
              "id": "25153392",
              "login": "wu5567488",
              "name": "wu5567488"
          }
      ]

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/search/users?q=wu_nian&sort=joined_at&page=1&per_page=2' \
      --header 'Authorization: Bearer {your-token}'


2. Search Issues
----------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/search/issues``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number Limit:      | query | int       |
|                | Maximum 100                     |       |           |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items per Page Limit: Maximum   | query | int       |
|                | 50                              |       |           |
+----------------+---------------------------------+-------+-----------+
| q\*            | keywords                        | query | string    |
+----------------+---------------------------------+-------+-----------+
| sort           | Sorting                         | query | string    |
|                | Fields，created_at(created      |       |           |
|                | time)、last_push_at(update      |       |           |
|                | time)，Default Sorting: Best    |       |           |
|                | Match                           |       |           |
+----------------+---------------------------------+-------+-----------+
| order          | Sorting Order (Default: desc)   | query | string    |
+----------------+---------------------------------+-------+-----------+
| repo           | Repository Path                 | query | string    |
+----------------+---------------------------------+-------+-----------+
| state          | 筛选指定状态的 issues,          | query | string    |
|                | open(开启)、closed(完成)        |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "id": 548499,
              "html_url": "https://gitcode.com/youlai/vue3-element-admin/issues/1",
              "number": "1",
              "state": "open",
              "title": "test",
              "body": "test",
              "repository": {
                  "id": 3771502,
                  "full_name": "youlai/vue3-element-admin",
                  "human_name": "有来开源组织 / vue3-element-admin",
                  "path": "vue3-element-admin",
                  "name": "vue3-element-admin",
                  "url": "https://gitcode.com/youlai/vue3-element-admin",
                  "owner": {
                      "avatar_url": "https://cdn-img.gitcode.com/fc/ae/3f96c31289ae838297c61f385af9c2e6357216a1906205f56d50f3e268319d8b.png?time=1724590827689",
                      "html_url": "https://gitcode.com/u013737132",
                      "id": "6553a045ac27540b6bfcb436",
                      "login": "u013737132",
                      "name": "有来技术",
                      "type": "User"
                  }
              },
              "created_at": "2024-11-07T18:11:23+08:00",
              "updated_at": "2024-11-07T18:11:23+08:00",
              "labels": [],
              "priority": 0,
              "comments": 0,
              "parent_id": 0
          },
          {
              "id": 518776,
              "html_url": "https://gitcode.com/openUBMC-test/openubmc-ci/issues/4",
              "number": "4",
              "state": "open",
              "title": "test_1",
              "body": "11111",
              "repository": {
                  "id": 4261097,
                  "full_name": "openUBMC-test/openubmc-ci",
                  "human_name": "openUBMC-test / openubmc-ci",
                  "path": "openubmc-ci",
                  "name": "openubmc-ci",
                  "url": "https://gitcode.com/openUBMC-test/openubmc-ci",
                  "owner": {
                      "avatar_url": "https://cdn-img.gitcode.com/fd/ab/256f0d7a9b2b771a883a9a2975f6bb8804dbcc53df334a63a508306f86fe6c2c.jpg",
                      "html_url": "https://gitcode.com/levi3053",
                      "id": "671af08b9a767f4c7b6b0681",
                      "login": "levi3053",
                      "name": "BellllllYu@N.L¡",
                      "type": "User"
                  }
              },
              "created_at": "2024-11-01T14:12:21+08:00",
              "updated_at": "2024-11-01T14:15:00+08:00",
              "labels": [],
              "priority": 0,
              "comments": 2,
              "parent_id": 0
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/search/issues?q=test&sort=created_at&page=1&per_page=2' \
      --header 'Authorization: Bearer {your-token}'


3. Search Repositories
----------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/search/repositories``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number Limit:      | query | int       |
|                | Maximum 100                     |       |           |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items per Page Limit: Maximum   | query | int       |
|                | 50                              |       |           |
+----------------+---------------------------------+-------+-----------+
| q\*            | keywords                        | query | string    |
+----------------+---------------------------------+-------+-----------+
| sort           | Sorting                         | query | string    |
|                | Fields，last_push_at(update     |       |           |
|                | time)、stars_count(star         |       |           |
|                | count)、forks_count(fork        |       |           |
|                | count)，Default Sorting: Best   |       |           |
|                | Match                           |       |           |
+----------------+---------------------------------+-------+-----------+
| order          | Sorting Order (Default: desc)   | query | string    |
+----------------+---------------------------------+-------+-----------+
| owner          | Repository Owner Path           | query | string    |
|                | (Organization or User Path)     |       |           |
+----------------+---------------------------------+-------+-----------+
| fork           | Forked Repositories and Search  | query | string    |
|                | Visibility,Forked repositories  |       |           |
|                | are not included in search      |       |           |
|                | results by default.             |       |           |
+----------------+---------------------------------+-------+-----------+
| language       | Filtering Repositories by       | query | string    |
|                | Programming Language            |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "id": 1431191,
              "full_name": "gh_mirrors/al/allure2",
              "human_name": "GitHub 加速计划 / al / allure2",
              "url": "https://api.gitcode.com/api/v5/repos/gh_mirrors/al/allure2",
              "namespace": {
                  "id": 2192652,
                  "type": "enterprise",
                  "name": "al",
                  "path": "al",
                  "html_url": "https://gitcode.com/al"
              },
              "path": "allure2",
              "name": "allure2",
              "description": "Allure Report is a flexible, lightweight multi-language test reporting tool. It provides clear graphical reports and allows everyone involved in the development process to extract the maximum of information from the everyday testing process",
              "status": "开始",
              "ssh_url_to_repo": "git@gitcode.com:gh_mirrors/al/allure2.git",
              "http_url_to_repo": "https://gitcode.com/gh_mirrors/al/allure2.git",
              "web_url": "https://gitcode.com/gh_mirrors/al/allure2",
              "created_at": "2023-12-18T00:42:15.557+08:00",
              "updated_at": "2024-11-05T10:54:59.948+08:00",
              "homepage": "https://gitcode.com/gh_mirrors/al/allure2",
              "members": [
                  "Gitcode-Assistant",
                  "coco_gitcode",
                  "gitshumei"
              ],
              "forks_count": 0,
              "stargazers_count": 9,
              "relation": "",
              "permission": {
                  "push": false
              },
              "internal": false,
              "open_issues_count": 0,
              "has_issue": false,
              "watchers_count": 4,
              "enterprise": {
                  "id": 2192652,
                  "path": "al",
                  "html_url": "https://gitcode.com/al",
                  "type": "enterprise"
              },
              "default_branch": "main",
              "fork": false,
              "pushed_at": "2024-08-06T23:34:38.476+08:00",
              "owner": {
                  "id": "69090",
                  "login": "coco_gitcode",
                  "name": "GitCode优质项目",
                  "type": "User"
              },
              "issue_template_source": "project",
              "private": false,
              "public": true
          },
          {
              "id": 1401745,
              "full_name": "gh_mirrors/pr/printf",
              "human_name": "GitHub 加速计划 / pr / printf",
              "url": "https://api.gitcode.com/api/v5/repos/gh_mirrors/pr/printf",
              "namespace": {
                  "id": 2192766,
                  "type": "enterprise",
                  "name": "pr",
                  "path": "pr",
                  "html_url": "https://gitcode.com/pr"
              },
              "path": "printf",
              "name": "printf",
              "description": "Tiny, fast, non-dependent and fully loaded printf implementation for embedded systems. Extensive test suite passing.",
              "status": "开始",
              "ssh_url_to_repo": "git@gitcode.com:gh_mirrors/pr/printf.git",
              "http_url_to_repo": "https://gitcode.com/gh_mirrors/pr/printf.git",
              "web_url": "https://gitcode.com/gh_mirrors/pr/printf",
              "created_at": "2023-12-16T20:28:57.687+08:00",
              "updated_at": "2024-09-27T21:48:26.980+08:00",
              "homepage": "https://gitcode.com/gh_mirrors/pr/printf",
              "members": [
                  "Gitcode-Assistant",
                  "coco_gitcode",
                  "gitshumei"
              ],
              "forks_count": 0,
              "stargazers_count": 8,
              "relation": "",
              "permission": {
                  "push": false
              },
              "internal": false,
              "open_issues_count": 0,
              "has_issue": false,
              "watchers_count": 0,
              "enterprise": {
                  "id": 2192766,
                  "path": "pr",
                  "html_url": "https://gitcode.com/pr",
                  "type": "enterprise"
              },
              "default_branch": "master",
              "fork": false,
              "pushed_at": "2024-08-10T00:28:30.350+08:00",
              "owner": {
                  "id": "69090",
                  "login": "coco_gitcode",
                  "name": "GitCode优质项目",
                  "type": "User"
              },
              "issue_template_source": "project",
              "private": false,
              "public": true
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/search/repositories?q=test&sort=stars_count&page=1&per_page=2' \
      --header 'Authorization: Bearer {your-token}'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/search/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
