Repository API
==============


1. Get a tree
-------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/git/trees/{sha}``

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
| sha\*          | Can be a branch name (e.g.,     | path  | string    |
|                | master), a commit SHA, or a     |       |           |
|                | directory tree SHA              |       |           |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number             | query | int       |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum 100     | query | int       |
+----------------+---------------------------------+-------+-----------+
| recursive      | Set to 1 to recursively         | query | int       |
|                | retrieve the directory          |       |           |
+----------------+---------------------------------+-------+-----------+

Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "tree": [
              {
                  "sha": "5259c4b24f015ffdc3663e81837a730c2a108e1f",
                  "name": "b",
                  "type": "tree",
                  "path": "a/b",
                  "mode": "040000",
                  "md5": "a7e86136543b019d72468ceebf71fb8e"
              }
          ]
      }

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/git/trees/main?access_token=?'


2. Retrieve Contents Under a Specific Repository Path
-----------------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/contents/{path}``


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
| path\*         | Path of the File                | path  | string    |
+----------------+---------------------------------+-------+-----------+
| ref            | Branch, tag, or commit.         | query | string    |
|                | Default: Repository’s default   |       |           |
|                | branch (main)                   |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "type": "file",
          "encoding": "base64",
          "size": 19,
          "name": "Note2.md",
          "path": "Note2.md",
          "content": "JXU2RDRCJXU4QkQ1d2ViaG9vaw==",
          "sha": "e5699fe1b360d6c799ee58b24fb5a670b1e14851",
          "url": "https://gitcode.com/api/v5/repos/daming_1/zhu_di/contents/Note2.md",
          "html_url": "https://gitcode.com/daming_1/zhu_di/blob/master/Note2.md",
          "download_url": "https://gitcode.com/daming_1/zhu_di/raw/master/Note2.md",
          "_links": {
              "self": "https://gitcode.com/api/v5/repos/daming_1/zhu_di/contents/Note2.md",
              "html": "https://gitcode.com/daming_1/zhu_di/blob/master/Note2.md"
          }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/contents/1.txt?access_token=?&ref=main'


3. Get File List
----------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/file_list``


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
| ref_name       | ref(Branch, tag, or commit)     | query | string    |
+----------------+---------------------------------+-------+-----------+
| file_name      | file name                       | query | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          "abc/test.rs",
          "bcd/test.rs"
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/owner-test/secure-issue/file_list?access_token=******&file_name=%2Ftest.rs&ref_name=main'


4. Create File
--------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/contents/{path}``

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
| path\*         | file path                       | path  | string    |
+----------------+---------------------------------+-------+-----------+
| content\*      | File content, must be Base64    | body  | string    |
|                | encoded.                        |       |           |
+----------------+---------------------------------+-------+-----------+
| message\*      | commit message                  | body  | string    |
+----------------+---------------------------------+-------+-----------+
| branch         | branch                          | body  | string    |
+----------------+---------------------------------+-------+-----------+
| author[name]   | author name                     | body  | string    |
+----------------+---------------------------------+-------+-----------+
| author[email]  | author email                    | body  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "commit": {
              "sha": "668cb104692b30d537b07f3721df9956d073d343",
              "author": {
                  "name": "GitCode2023",
                  "email": "13328943+gitcode_admin@user.noreply.gitcode.com",
                  "date": "2024-04-11T09:15:20+00:00"
              },
              "committer": {
                  "name": "Gitee",
                  "email": "noreply@gitcode.com",
                  "date": "2024-04-11T09:15:20+00:00"
              },
              "message": "22222"
              "parents": [
                  {
                          "sha":
            "0117aa5c6bc8e33d18ad8911afa3cbb54a1faabe"
                  }
              ]
          }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang/test/contents/xg8.txt?access_token=?' \
      --header 'Content-Type: application/json;charset=UTF-8' \
      --data-raw '{
          "content":"你好你好",
          "message":"api提交",
          "author[name]":"xg1",
          "author[email]":"xg1@qq.com",
          "committer[name]":"xg2",
          "committer[email]":"xg2@qq.com"
      }'


5. Update File
--------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/contents/{path}``

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
| path\*         | file path                       | path  | string    |
+----------------+---------------------------------+-------+-----------+
| content\*      | File content, must be Base64    | body  | string    |
|                | encoded.                        |       |           |
+----------------+---------------------------------+-------+-----------+
| sha\*          | 文件的 Blob SHA                 | body  | string    |
+----------------+---------------------------------+-------+-----------+
| branch         | branch                          | body  | string    |
+----------------+---------------------------------+-------+-----------+
| message\*      | commit message                  | body  | string    |
+----------------+---------------------------------+-------+-----------+
| author[name]   | author name                     | body  | string    |
+----------------+---------------------------------+-------+-----------+
| author[email]  | author email                    | body  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "content": {
              "name": "Note2.md",
              "path": "Note2.md",
              "url": "https://gitcode.com/api/v5/repos/daming_1/zhu_di/contents/Note2.md",
              "html_url": "https://gitcode.com/daming_1/zhu_di/blob/master/Note2.md",
              "download_url": "https://gitcode.com/daming_1/zhu_di/raw/master/Note2.md",
              "_links": {
                  "self": "https://gitcode.com/api/v5/repos/daming_1/zhu_di/contents/Note2.md",
                  "html": "https://gitcode.com/daming_1/zhu_di/blob/master/Note2.md"
              }
          }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/xiaogang/test/contents/xg8.txt?access_token=?' \
      --header 'Content-Type: application/json;charset=UTF-8' \
      --data '{
          "content":"你好你好",
          "message":"api提交",
          "sha":"e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
      }'


6. Delete File
--------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/contents/{path}``

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
| path\*         | file path                       | path  | string    |
+----------------+---------------------------------+-------+-----------+
| sha\*          | file Blob SHA                   | body  | string    |
+----------------+---------------------------------+-------+-----------+
| branch         | branch name                     | body  | string    |
+----------------+---------------------------------+-------+-----------+
| message\*      | commit message                  | body  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "commit": {
              "sha": "2a90c33ede2c1eafc5943727fd57129d870ad2e4",
              "author": {
                  "name": "xiaogang",
                  "email": "1150456356@qq.com",
                  "date": "2024-11-25T02:11:56.000Z"
              },
              "committer": {
                  "name": "xiaogang",
                  "email": "1150456356@qq.com",
                  "date": "2024-11-25T02:11:56.000Z"
              },
              "message": "api删除文件",
              "tree": "791f24a0da8c8458e40da3243bde183d59773514",
              "parents": [
                  "33e9ee7ccd32835a0fb9f2af99264931c06fbe11"
              ]
          }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/repos/testyl001/test001/contents/1/2/3/4/5/test.md?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data '{
          "sha": "52cfcc97f43188d16050e6395d456fc61f085eb9",
          "message": "删除文件",
          "branch": "branch01"
      }'


7. Get File Blob
----------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/git/blobs/{sha}``

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
| sha\*          | blob sha                        | path  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "sha":"e5699fe1b360d6c799ee58b24fb5a670b1e14851",
          "size":19,
          "url":"https://gitcode.com/api/v5/repos/daming_1/zhu_di/git/blobs/e5699fe1b360d6c799ee58b24fb5a670b1e14851",
          "content":"JXU2RDRCJXU4QkQ1d2ViaG9vaw==",
          "encoding":"base64"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/git/blobs/e69de29bb2d1d6434b8b29ae775ad8c2e48c5391?access_token=?' \


8. Get Repository Languages
---------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/languages``


Parameters
~~~~~~~~~~

+----------------+------------------------------+----------+-----------+
| Parameter      | Description                  | Type     | Data Type |
+================+==============================+==========+===========+
| access_token\* | personal access token        | formData | string    |
+----------------+------------------------------+----------+-----------+
| owner\*        | Repository Owner Path        | path     | string    |
|                | (Organization or User Path)  |          |           |
+----------------+------------------------------+----------+-----------+
| repo\*         | Repository Path(path)        | path     | string    |
+----------------+------------------------------+----------+-----------+


Response
~~~~~~~~

Map\ ``<语言名称, 百分比>``

.. container:: highlight

   .. code:: text

      {
          "Shell": 49.77,
          "Python": 50.23
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/languages?access_token=?' \


9. Get Repository Contributors
------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/contributors``


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
| type           | Contributor                     | query | string    |
|                | Type(committers/authors)        |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "name": "dengmengmian",
              "contributions": 3,
              "email": "my@dengmengmian.com"
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/contributors?access_token=xxxx&type=committers'


10. Set Repository Modules
--------------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/module/setting``


Parameters
~~~~~~~~~~

+-----------------------+-----------------------+----------+-----------+
| Parameter             | Description           | Type     | Data Type |
+=======================+=======================+==========+===========+
| access_token\*        | personal access token | formData | string    |
+-----------------------+-----------------------+----------+-----------+
| owner\*               | Repository Owner Path | path     | string    |
|                       | (Organization or User |          |           |
|                       | Path)                 |          |           |
+-----------------------+-----------------------+----------+-----------+
| repo\*                | Repository Path(path) | path     | string    |
+-----------------------+-----------------------+----------+-----------+
| has_wiki              | wiki                  | body     | boolean   |
+-----------------------+-----------------------+----------+-----------+
| has_issue             | issue                 | body     | boolean   |
+-----------------------+-----------------------+----------+-----------+
| has_security          | security issue        | body     | boolean   |
+-----------------------+-----------------------+----------+-----------+
| has_merge_request     | merge request         | body     | boolean   |
+-----------------------+-----------------------+----------+-----------+
| has_fork              | fork allowed          | body     | boolean   |
+-----------------------+-----------------------+----------+-----------+
| has_analysis          | analysis              | body     | boolean   |
+-----------------------+-----------------------+----------+-----------+
| has_discussion        | discussion            | body     | boolean   |
+-----------------------+-----------------------+----------+-----------+


Response
~~~~~~~~

   When the response returns “success”, it indicates the operation was
   successful. Any other response would indicate failure.

.. container:: highlight

   .. code:: text

      {
          "msg": "success",
          "code": 1
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/testyl001/test001/module/setting?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data '{
          "has_wiki": true,
      }'


11. Update Repository Settings
------------------------------


Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}``

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
| name\*         | Repository Name                 | body  | string    |
+----------------+---------------------------------+-------+-----------+
| description    | Repository Description          | body  | string    |
+----------------+---------------------------------+-------+-----------+
| homepage       | homepage, eg:                   | body  | string    |
|                | https://gitcode.com             |       |           |
+----------------+---------------------------------+-------+-----------+
| path           | Repository Path                 | body  | string    |
+----------------+---------------------------------+-------+-----------+
| private        | private: true/false             | body  | boolean   |
+----------------+---------------------------------+-------+-----------+
| default_branch | default branch                  | body  | string    |
+----------------+---------------------------------+-------+-----------+
| lfs_enabled    | lfs enabled                     | body  | boolean   |
+----------------+---------------------------------+-------+-----------+


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

      curl --location --request PATCH 'https://api.gitcode.com/api/v5/repos/testyl001/test001?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data '{
          "name": "test002",
          "description": "1"
      }'


12. Modify Repository Code Review Settings
------------------------------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/reviewer``


Parameters
~~~~~~~~~~

+------------------+-------------------------------+-------+-----------+
| Parameter        | Description                   | Type  | Data Type |
+==================+===============================+=======+===========+
| access_token\*   | personal access token         | query | string    |
+------------------+-------------------------------+-------+-----------+
| owner\*          | Repository Owner Path         | path  | string    |
|                  | (Organization or User Path)   |       |           |
+------------------+-------------------------------+-------+-----------+
| repo\*           | Repository Path(path)         | path  | string    |
+------------------+-------------------------------+-------+-----------+
| assignees        | aprroval username, can        | body  | string    |
|                  | provide multiple values,      |       |           |
|                  | separated by commas. eg:      |       |           |
|                  | (username1,username2)         |       |           |
+------------------+-------------------------------+-------+-----------+
| testers          | tester username, can provide  | body  | string    |
|                  | multiple values, separated by |       |           |
|                  | commas. eg:                   |       |           |
|                  | (username1,username2)         |       |           |
+------------------+-------------------------------+-------+-----------+
| assignees_number | Minimum number of approvals   | body  | int       |
+------------------+-------------------------------+-------+-----------+
| testers_number   | Minimum number of testers     | body  | int       |
+------------------+-------------------------------+-------+-----------+

**Note: At least one of assignees, testers, assignees_number,
testers_number must be set.**


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "id": 7543745,
          "created_at": "2024-01-24T14:33:44+08:00",
          "updated_at": "2024-04-07T21:23:08+08:00"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/testyl001/test001/reviewer?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data '{
          "assignees": "username1,username2",
          "testers": "username1,username2",
          "assignees_number": 1,
          "testers_number": 1
      }'


13. Archive Repository
----------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/org/{org}/repo/{repo}/status``

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| org\*          | Repository Ownership Path       | path  | string    |
|                | (Company, Organization, or      |       |           |
|                | Personal Path)                  |       |           |
+----------------+---------------------------------+-------+-----------+
| repo\*         | Repository Path(path)           | path  | string    |
+----------------+---------------------------------+-------+-----------+
| status\*       | state, 0: open，2: archived     | body  | int       |
+----------------+---------------------------------+-------+-----------+
| password\*     | password                        | body  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "code": 1,
          "msg": "success"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/testyl001/test001/reviewer?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data '{
          "assignees": "username1,username2",
          "testers": "username1,username2",
          "assignees_number": 1,
          "testers_number": 1
      }'


14. Transfer Repository
-----------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/org/{org}/projects/{repo}/transfer``

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| org\*          | Repository Ownership Path       | path  | string    |
|                | (Company, Organization, or      |       |           |
|                | Personal Path)                  |       |           |
+----------------+---------------------------------+-------+-----------+
| repo\*         | Repository Path                 | path  | string    |
+----------------+---------------------------------+-------+-----------+
| transfer_to\*  | target namespace                | body  | string    |
+----------------+---------------------------------+-------+-----------+
| password\*     | password                        | body  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "code": 1,
          "msg": "success"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/org/xiaogang/projects/test/transfer?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data '{
          "transfer_to": "xiaogang_test",
          "password": "password"
      }'


15. Get Repository Permission Mode
----------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/transition``


Parameters
~~~~~~~~~~

+----------------+------------------------------+----------+-----------+
| Parameter      | Description                  | Type     | Data Type |
+================+==============================+==========+===========+
| access_token\* | personal access token        | formData | string    |
+----------------+------------------------------+----------+-----------+
| owner\*        | Repository Owner Path        | path     | string    |
|                | (Organization or User Path)  |          |           |
+----------------+------------------------------+----------+-----------+
| repo\*         | Repository Path(path)        | path     | string    |
+----------------+------------------------------+----------+-----------+


Response
~~~~~~~~

   Permission mode 1, 2, where 1 is inheritance mode and 2 is
   independent mode.

.. container:: highlight

   .. code:: text

      {
          "memberMgntMode": 1
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/repos/xiaogang/test/transition?access_token={your-token}'


16. Update Repository Permission Mode
-------------------------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/transition``


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
| mode\*         | Member permission management    | body  | int       |
|                | mode: 1 (Inheritance Mode), 2   |       |           |
|                | (Independent Mode); mixed mode  |       |           |
|                | settings are not accepted       |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "msg": "success",
          "code": 1
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/xiaogang/test/transition?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data '{
          "mode": 1
      }'


17. Set Repository Push Rules
-----------------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/push_config``


Parameters
~~~~~~~~~~

+--------------------------+-----------------------+----------+-----------+
| Parameter                | Description           | Type     | Data Type |
+==========================+=======================+==========+===========+
| access_token\*           | personal access token | formData | string    |
+--------------------------+-----------------------+----------+-----------+
| owner\*                  | Repository Owner Path | path     | string    |
|                          | (Organization or User |          |           |
|                          | Path)                 |          |           |
+--------------------------+-----------------------+----------+-----------+
| repo\*                   | Repository Path(path) | path     | string    |
+--------------------------+-----------------------+----------+-----------+
| reject_not_signed_by_gpg | Only commits with     | body     | boolean   |
|                          | verified signatures   |          |           |
|                          | are allowed           |          |           |
+--------------------------+-----------------------+----------+-----------+
| commit_message_regex     | Commit message        | body     | string    |
|                          | validation            |          |           |
+--------------------------+-----------------------+----------+-----------+
| max_file_size            | Commit file size      | body     | Integer   |
|                          | limit (in MB)         |          |           |
+--------------------------+-----------------------+----------+-----------+
| skip_rule_for_owner      | Commits by project    | body     | boolean   |
|                          | administrators are    |          |           |
|                          | not subject to the    |          |           |
|                          | above rules           |          |           |
+--------------------------+-----------------------+----------+-----------+
| deny_force_push          | Force push is         | body     | boolean   |
|                          | prohibited (including |          |           |
|                          | for administrators)   |          |           |
+--------------------------+-----------------------+----------+-----------+


Response
~~~~~~~~

返回参数含义参考 body

.. container:: highlight

   .. code:: text

      {
          "reject_not_signed_by_gpg": false,
          "deny_force_push": true,
          "max_file_size": 10,
          "skip_rule_for_owner": false
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/repos/gitcode-dev/euler-api-list/push_config' \
      --header 'PRIVATE-TOKEN: {your-token}' \
      --header 'Cookie: GitCodeUserName=bond007; HWWAFSESID=ac1f8735c7a0f5acb6; HWWAFSESTIME=1730276856784'


18. Get Repository Push Rules
-----------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/push_config``


Parameters
~~~~~~~~~~

+----------------+------------------------------+----------+-----------+
| Parameter      | Description                  | Type     | Data Type |
+================+==============================+==========+===========+
| access_token\* | personal access token        | formData | string    |
+----------------+------------------------------+----------+-----------+
| owner\*        | Repository Owner Path        | path     | string    |
|                | (Organization or User Path)  |          |           |
+----------------+------------------------------+----------+-----------+
| repo\*         | Repository Path(path)        | path     | string    |
+----------------+------------------------------+----------+-----------+


Response
~~~~~~~~

   Return parameter meanings: refer to the body of setting project push
   rules.

.. container:: highlight

   .. code:: text

      {
          "reject_not_signed_by_gpg": false,
          "deny_force_push": true,
          "max_file_size": 10,
          "skip_rule_for_owner": false
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/gitcode-dev/euler-api-list/push_config' \
      --header 'PRIVATE-TOKEN: {your-token}' \
      --form 'deny_force_push="true"'


19. Delete a Repository
-----------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}``


Parameters
~~~~~~~~~~

+----------------+------------------------------+----------+-----------+
| Parameter      | Description                  | Type     | Data Type |
+================+==============================+==========+===========+
| access_token\* | personal access token        | formData | string    |
+----------------+------------------------------+----------+-----------+
| owner\*        | Repository Owner Path        | path     | string    |
|                | (Organization or User Path)  |          |           |
+----------------+------------------------------+----------+-----------+
| repo\*         | Repository Path(path)        | path     | string    |
+----------------+------------------------------+----------+-----------+


Response
~~~~~~~~

无


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/repos/xiaogang/test?access_token={your-token}' \
      --header 'Content-Type: application/json'


20. Create Organization Repository
----------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/orgs/{org}/repos``


Parameters
~~~~~~~~~~

+------------------------+-------------------------------------+-------+-----------+
| Parameter              | Description                         | Type  | Data Type |
+========================+=====================================+=======+===========+
| access_token\*         | personal access token               | query | string    |
+------------------------+-------------------------------------+-------+-----------+
| name\*                 | Repository Name                     | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| description            | Repository Description              | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| homepage               | homepage                            | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| has_issues             | TRUE Allow Issues to Be Created     | body  | boolean   |
|                        | (Enabled/Disabled). Default: true   |       |           |
+------------------------+-------------------------------------+-------+-----------+
| has_wiki               | has wiki. Default: true             | body  | boolean   |
+------------------------+-------------------------------------+-------+-----------+
| auto_init              | When set to true, the repository    | body  | boolean   |
|                        | will be initialized with a README.  |       |           |
|                        | Default: Do not initialize (false). |       |           |
+------------------------+-------------------------------------+-------+-----------+
| gitignore_template     | gitignore template                  | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| license_template       | license template                    | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| path                   | Repository Path                     | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| private                | private: true/false                 | body  | boolean   |
+------------------------+-------------------------------------+-------+-----------+
| import_url             | Repository import URL, which must   | body  | string    |
|                        | end with .git, for example:         |       |           |
|                        | https://github.com/apache/kafka.git |       |           |
+------------------------+-------------------------------------+-------+-----------+


Response
~~~~~~~~

   Return parameter meanings: Refer to the body for setting project push
   rules.

.. container:: highlight

   .. code:: text

      {
          "id": 729293,
          "full_name": "xiaogang/4",
          "human_name": "xiaogang / 4",
          "url": "https://api.gitcode.com/api/v5/repos/xiaogang/4",
          "namespace": {
              "id": 137117,
              "name": "xiaogang",
              "path": "xiaogang",
              "develop_mode": "normal",
              "kind": "user",
              "full_path": "xiaogang",
              "full_name": "xiaogang",
              "visibility_level": 20,
              "enable_file_control": false,
              "owner_id": 496
          },
          "path": "4",
          "name": "4",
          "private": true,
          "public": false,
          "visibility": "private"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/orgs/xiaogang_test/repos?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data '{
          "name": "4",
          "has_issues": "true",
          "has_wiki": "true",
          "can_comment": "true",
          "private": "true"
      }'


21. Fork a Repository
---------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/forks``


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
| organization   | Full organization space         | body  | string    |
|                | address, if not provided, it    |       |           |
|                | will default to forking to the  |       |           |
|                | user’s personal space address   |       |           |
+----------------+---------------------------------+-------+-----------+
| name           | Forked repository name.         | body  | string    |
|                | Default: Source repository name |       |           |
+----------------+---------------------------------+-------+-----------+
| path           | Forked repository address.      | body  | string    |
|                | Default: Source repository      |       |           |
|                | address                         |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "id": 729292,
          "full_name": "xiaogang_test/fork2",
          "human_name": "测试组织 / fork2",
          "url": "https://api.gitcode.com/api/v5/repos/xiaogang_test/fork2",
          "namespace": {
              "id": 138108,
              "name": "测试组织",
              "path": "xiaogang_test",
              "develop_mode": "normal",
              "cell": "default",
              "kind": "group",
              "full_path": "xiaogang_test",
              "full_name": "测试组织",
              "visibility_level": 20,
              "enable_file_control": false
          }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/nevins/LessConsole/forks?access_token={your-token}' \
      --header 'Content-Type: application/json' \
      --data '{
          "name":"fork2",
          "path":"fork2",
          "organization":"xiaogang_test"
      }'


22. List Forks of a Repository
------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/forks``


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
| sort           | sort: fork(newest,              | query | string    |
|                | oldest)，star(stargazers)       |       |           |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number             | query | int       |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum 100     | query | int       |
+----------------+---------------------------------+-------+-----------+
| created_after  | created after                   | query | string    |
+----------------+---------------------------------+-------+-----------+
| created_before | created before                  | query | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "id": 567682,
              "full_name": "wangwt/RuoYi",
              "human_name": "wangwt / RuoYi",
              "url": "https://api.gitcode.com/api/v5/repos/wangwt/RuoYi",
              "namespace": {
                  "id": 153748,
                  "type": "personal",
                  "name": "wangwt",
                  "path": "wangwt",
                  "html_url": "https://test.gitcode.net/wangwt"
              },
              "description": "",
              "status": "",
              "created_at": "2024-07-29T15:42:45.149+08:00",
              "updated_at": "2024-07-29T15:42:45.149+08:00",
              "owner": {
                  "id": 970,
                  "login": "wangwt",
                  "name": "wangwt"
              },
              "pushed_at": "2024-11-08T16:24:10.576+08:00",
              "parent": {
                  "id": 517092,
                  "full_name": "xiaogang/RuoYi",
                  "human_name": "xiaogang / RuoYi",
                  "url": "https://api.gitcode.com/api/v5/repos/xiaogang/RuoYi",
                  "namespace": {
                      "id": 137117,
                      "type": "personal",
                      "name": "xiaogang",
                      "path": "xiaogang",
                      "html_url": "https://test.gitcode.net/xiaogang"
                  }
              },
              "private": false,
              "public": true
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/repos/nevins/LessConsole/forks?access_token={your-token}'


23. Upload Image
----------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/img/upload``


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
| body\*         | File content in base64 format   | body  | string    |
|                | (limit: 20MB).                  |       |           |
+----------------+---------------------------------+-------+-----------+
| file_name\*    | File Name                       | body  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "success": true,
          "path": "uploads/4c98ad75-729f-49ce-82ab-b41c1f7ffc90/test3.txt",
          "full_path": "https://gitcode.com/xiaogang/test/attachment/uploads/4c98ad75-729f-49ce-82ab-b41c1f7ffc90/test3.txt"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/tiandi/YanF4/img/upload?access_token=******' \
      --header 'Content-Type: application/json' \
      --data '{
      "body":"1",
      "file_name":"2.png"
      }'


24. Upload File
---------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/file/upload``


Parameters
~~~~~~~~~~

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
| file\*         | File content in base64       | formData | file      |
|                | format (limit: 20MB)         |          |           |
+----------------+------------------------------+----------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "success": true,
          "path": "uploads/4c98ad75-729f-49ce-82ab-b41c1f7ffc90/test3.txt",
          "full_path": "https://gitcode.com/xiaogang/test/attachment/uploads/4c98ad75-729f-49ce-82ab-b41c1f7ffc90/test3.txt"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/file/upload' \
      --header 'Content-Type: application/json;charset=UTF-8' \
      --header 'PRIVATE-TOKEN: token' \
      --form 'file=@"/Users/xiaogang/Downloads/test3.txt"'


25. List Users Watching a Repository
------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/subscribers``


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
| page           | Current Page Number             | query | int       |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum 100     | query | int       |
+----------------+---------------------------------+-------+-----------+
| watched_after  | watched after                   | query | String    |
+----------------+---------------------------------+-------+-----------+
| watched_before | watched before                  | query | String    |
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

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/subscribers' \
      --header 'PRIVATE-TOKEN: token'


26. List Users Starring a Repository
------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/stargazers``


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
| page           | Current Page Number             | query | int       |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum 100     | query | int       |
+----------------+---------------------------------+-------+-----------+
| starred_after  | starred after                   | query | string    |
+----------------+---------------------------------+-------+-----------+
| starred_before | starred before                  | query | string    |
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
              "starred_at": "2024-11-13T16:15:53.287+08:00"
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/stargazers' \
      --header 'PRIVATE-TOKEN: token'


27. Update Repository Settings
------------------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/repo_settings``


Parameters
~~~~~~~~~~

+--------------------------------------------+------------------------+-------+-----------+
| Parameter                                  | Description            | Type  | Data Type |
+============================================+========================+=======+===========+
| access_token\*                             | personal access token  | query | string    |
+--------------------------------------------+------------------------+-------+-----------+
| owner\*                                    | Repository Ownership   | path  | string    |
|                                            | Path (Company,         |       |           |
|                                            | Organization, or       |       |           |
|                                            | Personal Path)         |       |           |
+--------------------------------------------+------------------------+-------+-----------+
| repo\*                                     | Repository Path(path)  | path  | string    |
+--------------------------------------------+------------------------+-------+-----------+
| disable_fork                               | disable fork           | body  | Boolean   |
+--------------------------------------------+------------------------+-------+-----------+
| forbidden_developer_create_branch          | forbidden developer    | body  | Boolean   |
|                                            | create branch          |       |           |
+--------------------------------------------+------------------------+-------+-----------+
| forbidden_developer_create_tag             | forbidden developer    | body  | Boolean   |
|                                            | create tag             |       |           |
+--------------------------------------------+------------------------+-------+-----------+
| forbidden_committer_create_branch          | forbidden committer    | body  | Boolean   |
|                                            | create branch          |       |           |
+--------------------------------------------+------------------------+-------+-----------+
| forbidden_developer_create_branch_user_ids | forbidden developer    | body  | String    |
|                                            | create branch user ids |       |           |
+--------------------------------------------+------------------------+-------+-----------+
| branch_name_regex                          | branch name regex      | body  | String    |
+--------------------------------------------+------------------------+-------+-----------+
| tag_name_regex                             | tag name regex         | body  | String    |
+--------------------------------------------+------------------------+-------+-----------+
| generate_pre_merge_ref                     | generate pre-merge ref | body  | Boolean   |
+--------------------------------------------+------------------------+-------+-----------+
| rebase_disable_trigger_webhook             | rebase disable trigger | body  | Boolean   |
|                                            | webhook                |       |           |
+--------------------------------------------+------------------------+-------+-----------+
| open_gpg_verified                          | open gpg verified      | body  | Boolean   |
+--------------------------------------------+------------------------+-------+-----------+
| include_lfs_objects                        | ZIP downlaod include   | body  | Boolean   |
|                                            | lfs objects            |       |           |
+--------------------------------------------+------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "disable_fork": true,
          "forbidden_developer_create_branch": false,
          "forbidden_developer_create_tag": false,
          "forbidden_committer_create_branch": false,
          "generate_pre_merge_ref": false,
          "forbidden_gitlab_access": true,
          "rebase_disable_trigger_webhook": false,
          "include_lfs_objects": false
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/test-org/test-repo/repo_settings?access_token=token' \
      --header 'Content-Type: application/json' \
      --data '{"disable_fork": true}'


28. Get Repository Settings
---------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/repo_settings``


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


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "disable_fork": true,
          "forbidden_developer_create_branch": false,
          "forbidden_developer_create_tag": false,
          "forbidden_committer_create_branch": false,
          "generate_pre_merge_ref": false,
          "forbidden_gitlab_access": true,
          "rebase_disable_trigger_webhook": false,
          "include_lfs_objects": false
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/test-org/test-repo/repo_settings?access_token=token'


29. Get Pull Request Settings
-----------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pull_request_settings``


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


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "merge_request_setting": {
              "id": 1431,
              "project_id": 2745002,
              "disable_merge_by_self": false,
              "created_at": "2024-03-28T10:04:13.523+08:00",
              "updated_at": "2024-11-13T21:30:45.261+08:00",
              "can_force_merge": false,
              "disable_squash_merge": true,
              "approval_required_reviewers": 0,
              "approval_required_approvers": 0,
              "add_notes_after_merged": false,
              "merged_commit_author": "merged_by",
              "mark_auto_merged_mr_as_closed": false,
              "delete_source_branch_when_merged": false,
              "auto_squash_merge": false,
              "squash_merge_with_no_merge_commit": false,
              "close_issue_when_mr_merged": false,
              "can_reopen": true,
              "is_check_cla": false,
              "approval_approvers": [],
              "approval_testers": [],
              "approval_required_testers": 0,
              "is_allow_lite_merge_request": false
          },
          "only_allow_merge_if_all_discussions_are_resolved": false,
          "only_allow_merge_if_pipeline_succeeds": false,
          "merge_method": "merge"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/test-org/test-repo/pull_request_settings?access_token=token'


30. Update Pull Request Settings
--------------------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pull_request_settings``


Parameters
~~~~~~~~~~

+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| Parameter                                        | Description                                     | Type  | Data Type |
+==================================================+=================================================+=======+===========+
| access_token\*                                   | personal access token                           | query | string    |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| owner\*                                          | Repository Ownership Path (Company,             | path  | string    |
|                                                  | Organization, or Personal Path)                 |       |           |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| repo\*                                           | Repository Path(path)                           | path  | string    |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| approval_required_reviewers_enable               | 是否启用审批必需的评审者功能                    | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| approval_required_reviewers                      | 需要的审批者数量(最小评审人数【选择的数字：1~5, | body  | Integer   |
|                                                  | 如果取消评审人功能传入0】)                      |       |           |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| only_allow_merge_if_all_discussions_are_resolved | 评审问题全部解决才能合入                        | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| only_allow_merge_if_pipeline_succeeds            | 是否仅在流水线成功后才允许合并                  | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| disable_merge_by_self                            | 禁止合入自己创建的合并请求                      | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| can_force_merge                                  | 允许管理员强制合入                              | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| add_notes_after_merged                           | 允许合并请求合并后继续做代码检视和评论          | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| mark_auto_merged_mr_as_closed                    | 是否将自动合并的MR状态标记为关闭状态            | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| can_reopen                                       | 是否可以重新打开一个已经关闭的合并请求          | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| delete_source_branch_when_merged                 | 合并时是否删除源分支，默认删除原分支            | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| disable_squash_merge                             | 禁止 Squash 合并                                | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| auto_squash_merge                                | 新建合并请求，默认开启 Squash 合并              | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| merge_method                                     | 合并模式三选一(通过 merge commit                | body  | String    |
|                                                  | 合并：merge；通过 merge commit 合并             |       |           |
|                                                  | （记录半线性历史）：rebase_merge；fast -        |       |           |
|                                                  | forward 合并：ff)                               |       |           |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| squash_merge_with_no_merge_commit                | Squash 合并不产生 Merge 节点                    | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| merged_commit_author                             | 使用 MR (合入/创建) 者生成 Merge Commit（使用   | body  | String    |
|                                                  | PR 合入者生成 Merge Commit：传 merged_by; 使用  |       |           |
|                                                  | PR 创建者生成 Merge Commit：传 created_by）     |       |           |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| approval_required_approvers                      | 需要审批的批准者数量                            | body  | Integer   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| approval_approver_ids                            | 项目审查人, user_id 以逗号分隔                  | body  | String    |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| approval_tester_ids                              | 项目测试人，user_id以逗号分隔                   | body  | String    |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| approval_required_testers                        | 测试最小通过人数                                | body  | Integer   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| is_check_cla                                     | 是否校验CLA                                     | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| is_allow_lite_merge_request                      | 是否启用轻量级 Pull Request                     | body  | Boolean   |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| lite_merge_request_prefix_title                  | 轻量级 pr 的标题前缀                            | body  | String    |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+
| close_issue_when_mr_merged                       | 创建 Pull Request 时,默认选中                   | body  | Boolean   |
|                                                  | “合并后关闭已关联的 Issue”                      |       |           |
+--------------------------------------------------+-------------------------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "merge_request_setting": {
              "id": 1431,
              "project_id": 2745002,
              "disable_merge_by_self": false,
              "created_at": "2024-03-28T10:04:13.523+08:00",
              "updated_at": "2024-11-13T21:30:45.261+08:00",
              "can_force_merge": false,
              "disable_squash_merge": true,
              "approval_required_reviewers": 0,
              "approval_required_approvers": 0,
              "add_notes_after_merged": false,
              "merged_commit_author": "merged_by",
              "mark_auto_merged_mr_as_closed": false,
              "delete_source_branch_when_merged": false,
              "auto_squash_merge": false,
              "squash_merge_with_no_merge_commit": false,
              "close_issue_when_mr_merged": false,
              "can_reopen": true,
              "is_check_cla": false,
              "approval_approvers": [],
              "approval_testers": [],
              "approval_required_testers": 0,
              "is_allow_lite_merge_request": false
          },
          "only_allow_merge_if_all_discussions_are_resolved": false,
          "only_allow_merge_if_pipeline_succeeds": false,
          "merge_method": "merge"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/test-org/test-repo/pull_request_settings?access_token=token' \
      --header 'Content-Type: application/json' \
      --data '{"is_check_cla": false}'


31. Create Personal Repository
------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/user/repos``


Parameters
~~~~~~~~~~

+------------------------+-------------------------------------+-------+-----------+
| Parameter              | Description                         | Type  | Data Type |
+========================+=====================================+=======+===========+
| access_token\*         | personal access token               | query | string    |
+------------------------+-------------------------------------+-------+-----------+
| name\*                 | Repository Name                     | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| description            | Repository Description              | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| homepage               | homepage                            | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| has_issues             | TRUE Allow Issues to Be Created     | body  | boolean   |
|                        | (Enabled/Disabled)Default: true     |       |           |
+------------------------+-------------------------------------+-------+-----------+
| has_wiki               | has wiki, Default: true             | body  | boolean   |
+------------------------+-------------------------------------+-------+-----------+
| auto_init              | When set to true, the repository    | body  | boolean   |
|                        | will be initialized with a README.  |       |           |
|                        | Default: Do not initialize (false). |       |           |
+------------------------+-------------------------------------+-------+-----------+
| gitignore_template     | gitignore template                  | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| license_template       | license template                    | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| path                   | Repository Path                     | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| private                | true/false                          | body  | string    |
+------------------------+-------------------------------------+-------+-----------+
| import_url             | Repository import URL, which must   | body  | string    |
|                        | end with .git, for example:         |       |           |
|                        | https://github.com/apache/kafka.git |       |           |
+------------------------+-------------------------------------+-------+-----------+


Response
~~~~~~~~

   Return parameter meanings: refer to the body of setting project push
   rules.

.. container:: highlight

   .. code:: text

      {
          "id": 729293,
          "full_name": "xiaogang/4",
          "human_name": "xiaogang / 4",
          "url": "https://api.gitcode.com/api/v5/repos/xiaogang/4",
          "namespace": {
              "id": 137117,
              "name": "xiaogang",
              "path": "xiaogang",
              "develop_mode": "normal",
              "kind": "user",
              "full_path": "xiaogang",
              "full_name": "xiaogang",
              "visibility_level": 20,
              "enable_file_control": false,
              "owner_id": 496
          },
          "path": "4",
          "name": "4",
          "private": true,
          "public": false,
          "visibility": "private"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/user/repos?access_token=token' \
      --header 'Content-Type: application/json' \
      --data '{"name": "test2"}'


32. Update Repository Member Roles
----------------------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/members/{username}``


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
| username\*     | username                        | path  | string    |
+----------------+---------------------------------+-------+-----------+
| permission     | permission: pull, push, admin,  | body  | string    |
|                | customized role name. Default:  |       |           |
|                | push                            |       |           |
+----------------+---------------------------------+-------+-----------+
| role_id        | role ID, If the permission is   | body  | string    |
|                | set to “customized”, the role   |       |           |
|                | ID must be provided.            |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "followers_url": "https://api-test.gitcode.com/api/v5/users/xiaogang2/followers",
          "html_url": "https://test.gitcode.net/xiaogang2",
          "id": "65ffca965079ba0d1c00f6f2",
          "login": "xiaogang2",
          "name": "肖刚2",
          "type": "User",
          "url": "https://api-test.gitcode.com/api/v5/xiaogang2",
          "permissions": {
              "admin": false,
              "push": false,
              "customized": true,
              "pull": false
          }
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/xiaogang/test/members/xiaogang2?access_token=token' \
      --header 'Content-Type: application/json' \
      --data '{
          "permission": "admin"
      }'


33. Transfer Repository
-----------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/transfer``

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
| new_owner\*    | target namespace                | body  | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "new_owner": "tiandi",
          "new_name": "new_repo_name"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/RealMadrid/repo_yf99999/transfer?access_token=your_token' \
      --form 'new_owner="tiandi"' \
      --form 'new_name="new_repo_name"'


34. Get Custom Roles of a Repository
------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/customized_roles``


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


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "role_id": "e6cd76d6c82f46c78c71fd7f67eaf3bf",
              "access_level": 15,
              "role_name": "测试角色",
              "role_chinese_name": "测试角色",
              "role_description": "测试角色",
              "role_type": "project-customized",
              "member_count": 1,
              "created_at": "2024-04-17 08:00",
              "updated_at": "2024-04-17 08:00"
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/customized_roles?access_token=?'


35. Download Statistics
-----------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/download_statistics``


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
| start_date     | start date（eg:2024-01-06）     | query | string    |
+----------------+---------------------------------+-------+-----------+
| end_date       | end date (eg: 2024-12-06)       | query | string    |
+----------------+---------------------------------+-------+-----------+
| direction      | asc/desc, Default: desc         | query | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

+-----------------------------------+----------------------------+-----------+
| 字段名                            | Description                | Data Type |
+===================================+============================+===========+
| pdate                             | date                       | string    |
+-----------------------------------+----------------------------+-----------+
| repo_id                           | repo id                    | string    |
+-----------------------------------+----------------------------+-----------+
| total_dl_cnt                      | total downlaod count       | Long      |
+-----------------------------------+----------------------------+-----------+
| today_dl_cnt                      | today download count       | Long      |
+-----------------------------------+----------------------------+-----------+
| download_statistics_total         | Total downloads within the | Long      |
|                                   | specified time range       |           |
+-----------------------------------+----------------------------+-----------+
| download_statistics_history_total | Total downloads up to the  | Long      |
|                                   | cutoff date                |           |
+-----------------------------------+----------------------------+-----------+

.. container:: highlight

   .. code:: text

      {
          "download_statistics_detail": [
              {
                  "pdate": "2024-11-13",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 38
              },
              {
                  "pdate": "2024-11-14",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 38
              },
              {
                  "pdate": "2024-11-15",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 38
              },
              {
                  "pdate": "2024-11-16",
                  "repo_id": "625513",
                  "today_dl_cnt": 5,
                  "total_dl_cnt": 43
              },
              {
                  "pdate": "2024-11-17",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 43
              },
              {
                  "pdate": "2024-11-18",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 43
              },
              {
                  "pdate": "2024-11-19",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 43
              },
              {
                  "pdate": "2024-11-20",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 43
              },
              {
                  "pdate": "2024-11-21",
                  "repo_id": "625513",
                  "today_dl_cnt": 2,
                  "total_dl_cnt": 45
              },
              {
                  "pdate": "2024-11-22",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 45
              },
              {
                  "pdate": "2024-11-23",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 45
              },
              {
                  "pdate": "2024-11-24",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 45
              },
              {
                  "pdate": "2024-11-25",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 45
              },
              {
                  "pdate": "2024-11-26",
                  "repo_id": "625513",
                  "today_dl_cnt": 0,
                  "total_dl_cnt": 45
              }
          ],
          "download_statistics_total": 7,
          "download_statistics_history_total": 45
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/openharmony/applications_app_samples/download_statistics?direction=asc&access_token=your_token&start_date=2024-01-11&end_date=2024-12-11'


36. Get Raw File
----------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/raw/{path}``


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
| repo\*         | Repository path                 | path  | string    |
+----------------+---------------------------------+-------+-----------+
| path\*         | File path                       | path  | string    |
+----------------+---------------------------------+-------+-----------+
| ref            | Branch, tag, or commit          | query | string    |
|                | (default: repository’s default  |       |           |
|                | branch)                         |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      raw file content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/org-test/repo-test/raw/test/test.py?access_token=your_token'


37. Get Repository Contributor Statistics
-----------------------------------------

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/contributors/statistic?access_token=your_token``


Parameters
~~~~~~~~~~

+----------------+-----------------------------------+-------+---------+
| Parameter      | Description                       | IN    | Type    |
+================+===================================+=======+=========+
| access_token\* | personal access token             | query | string  |
+----------------+-----------------------------------+-------+---------+
| owner\*        | Repository Ownership Path         | path  | string  |
|                | (Company, Organization, or        |       |         |
|                | Personal Path)                    |       |         |
+----------------+-----------------------------------+-------+---------+
| repo\*         | Repository path                   | path  | string  |
+----------------+-----------------------------------+-------+---------+
| author         | Filter contributors by username.  | query | string  |
|                | Specify a username to retrieve    |       |         |
|                | contribution data for that user.  |       |         |
|                | By default, returns contribution  |       |         |
|                | data for all users.               |       |         |
+----------------+-----------------------------------+-------+---------+
| current_user   | Whether to return data only for   | query | boolean |
|                | the current user. ``true``        |       |         |
|                | returns contribution data only    |       |         |
|                | for the current user, ``false``   |       |         |
|                | or omission returns data for all  |       |         |
|                | users. When set to ``true``, it   |       |         |
|                | has higher priority than the      |       |         |
|                | ``author`` parameter.             |       |         |
+----------------+-----------------------------------+-------+---------+
| since          | Start date in the format          | query | string  |
|                | ``YYYY-MM-DD`` or                 |       |         |
|                | ``YYYY-MM-DD HH:mm:ss``. Used to  |       |         |
|                | limit the start time of the       |       |         |
|                | returned contribution data.       |       |         |
+----------------+-----------------------------------+-------+---------+
| until          | End date in the format            | query | string  |
|                | ``YYYY-MM-DD`` or                 |       |         |
|                | ``YYYY-MM-DD HH:mm:ss``. Used to  |       |         |
|                | limit the end time of the         |       |         |
|                | returned contribution data.       |       |         |
+----------------+-----------------------------------+-------+---------+
| ref_name       | Specifies the ref_name (branch    | query | string  |
|                | name, commit id, tag name) for    |       |         |
|                | which to retrieve contribution    |       |         |
|                | data. If not provided or empty,   |       |         |
|                | the ``default branch`` is used.   |       |         |
+----------------+-----------------------------------+-------+---------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "name": "test",
          "email": "aa@ss.com",
          "overview": {
            "additions": 762,
            "deletions": 0,
            "total_changes": 0,
            "commit_count": 8
          },
          "contributions": [
            {
              "date": "2024-12-05",
              "additions": 759,
              "deletions": 0,
              "total_changes": 759,
              "commit_count": 5
            },
            {
              "date": "2024-12-08",
              "additions": 2,
              "deletions": 0,
              "total_changes": 2,
              "commit_count": 2
            },
            {
              "date": "2024-12-09",
              "additions": 1,
              "deletions": 0,
              "total_changes": 1,
              "commit_count": 1
            }
          ]
        }
      ]

Response Fields Description
^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------------------------------+---------+-----------------------------+
| Field                           | Type    | Description                 |
+=================================+=========+=============================+
| ``name``                        | string  | The contributor’s name or   |
|                                 |         | username.                   |
+---------------------------------+---------+-----------------------------+
| ``email``                       | string  | The contributor’s email     |
|                                 |         | address.                    |
+---------------------------------+---------+-----------------------------+
| ``overview``                    | object  | Overall statistics for the  |
|                                 |         | contributor, including the  |
|                                 |         | following fields:           |
+---------------------------------+---------+-----------------------------+
| ``overview.additions``          | integer | Total number of lines       |
|                                 |         | added.                      |
+---------------------------------+---------+-----------------------------+
| ``overview.deletions``          | integer | Total number of lines       |
|                                 |         | deleted.                    |
+---------------------------------+---------+-----------------------------+
| ``overview.total_changes``      | integer | Total number of lines       |
|                                 |         | changed (``additions`` +    |
|                                 |         | ``deletions``).             |
+---------------------------------+---------+-----------------------------+
| ``overview.commit_count``       | integer | Total number of commits.    |
+---------------------------------+---------+-----------------------------+
| ``contributions``               | array   | Array of contribution       |
|                                 |         | records, containing         |
|                                 |         | contribution data for each  |
|                                 |         | date.                       |
+---------------------------------+---------+-----------------------------+
| ``contributions.date``          | string  | Contribution date in the    |
|                                 |         | format ``YYYY-MM-DD``.      |
+---------------------------------+---------+-----------------------------+
| ``contributions.additions``     | integer | Number of lines added on    |
|                                 |         | that date.                  |
+---------------------------------+---------+-----------------------------+
| ``contributions.deletions``     | integer | Number of lines deleted on  |
|                                 |         | that date.                  |
+---------------------------------+---------+-----------------------------+
| ``contributions.total_changes`` | integer | Number of lines changed on  |
|                                 |         | that date.                  |
+---------------------------------+---------+-----------------------------+
| ``contributions.commit_count``  | integer | Number of commits on that   |
|                                 |         | date.                       |
+---------------------------------+---------+-----------------------------+


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/org-test/myrepo/contributors/statistic?access_token=your_token'


38. Get Repository events
-------------------------

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/events?access_token=your_token``


Parameters
~~~~~~~~~~

+----------------+------------------------------------+-------+--------+
| Parameter      | Description                        | IN    | Type   |
+================+====================================+=======+========+
| access_token\* | personal access token.             | query | string |
+----------------+------------------------------------+-------+--------+
| owner\*        | Repository Ownership Path          | path  | string |
|                | (Company, Organization, or         |       |        |
|                | Personal Path).                    |       |        |
+----------------+------------------------------------+-------+--------+
| repo\*         | Repository path.                   | path  | string |
+----------------+------------------------------------+-------+--------+
| filter         | Filter criteria, pass in all       | query | string |
|                | (all), push (Push event), merged   |       |        |
|                | (Merged event), issue (issue       |       |        |
|                | event), comments (comment events), |       |        |
|                | team (Team events), project        |       |        |
|                | (Project Event).                   |       |        |
+----------------+------------------------------------+-------+--------+
| author         | Event trigger person, enter        | query | string |
|                | username.                          |       |        |
+----------------+------------------------------------+-------+--------+
| before         | The starting date is in the format | query | string |
|                | of ‘YYYY-MM-DD’. Used to limit the |       |        |
|                | starting time of the returned      |       |        |
|                | event.                             |       |        |
+----------------+------------------------------------+-------+--------+
| after          | End date, in the format of         | query | string |
|                | ‘YYYY-MM-DD’. Used to limit the    |       |        |
|                | end time of the returned event.    |       |        |
+----------------+------------------------------------+-------+--------+
| page           | Current Page Number.               | query | int    |
+----------------+------------------------------------+-------+--------+
| per_page       | Items Per Page, Maximum 100.       | query | int    |
+----------------+------------------------------------+-------+--------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
          "events": [
              {
                  "action": 22,
                  "action_name": "opened",
                  "author": {
                      "id": 607,
                      "iam_id": "f09ca8d721eb49e4add47b67c0dbef81",
                      "username": "xiaogang",
                      "state": "active",
                      "email": "",
                      "name": "xiaogang",
                      "name_cn": "",
                      "web_url": "https://gitcode.com/xiaogang"
                  },
                  "author_id": 607,
                  "author_username": "xiaogang2",
                  "created_at": "2024-11-19T07:01:02.714Z",
                  "project_id": 249609,
                  "title": "{\"userid\":[496],\"username\":[\"xiaogang\"]}",
                  "filter_sensitive": true
              }
          ],
          "has_next_page": false
      }


Response Fields Description
^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-----------------------------+---------+-----------------------------+
| Field                       | Type    | Description                 |
+=============================+=========+=============================+
| ``events``                  | array   | Event List.                 |
+-----------------------------+---------+-----------------------------+
| ``has_next_page``           | boolean | Is there still a next page. |
+-----------------------------+---------+-----------------------------+
| ``events.action``           | integer | Event type identification,  |
|                             |         | each event has a unique     |
|                             |         | identifier.                 |
+-----------------------------+---------+-----------------------------+
| ``events.action_name``      | string  | Event identifier name.      |
+-----------------------------+---------+-----------------------------+
| ``events.author``           | object  | Trigger person of the       |
|                             |         | event.                      |
+-----------------------------+---------+-----------------------------+
| ``events.author_id``        | integer | Trigger ID of the event.    |
+-----------------------------+---------+-----------------------------+
| ``events.author_username``  | string  | Event triggered person      |
|                             |         | account.                    |
+-----------------------------+---------+-----------------------------+
| ``events.created_at``       | string  | Event triggering time.      |
+-----------------------------+---------+-----------------------------+
| ``events.project_id``       | integer | Repository id.              |
+-----------------------------+---------+-----------------------------+
| ``events.title``            | string  | Event Title.                |
+-----------------------------+---------+-----------------------------+


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/events?access_token=your_token'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
