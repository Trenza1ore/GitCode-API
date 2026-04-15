Pull Request API Documentation
==============================


1. Get the List of Pull Requests
--------------------------------

Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls``

Parameters
~~~~~~~~~~

+------------------+------------------------------------------------+-------+-----------+
| Parameter        | Description                                    | Type  | Data Type |
+==================+================================================+=======+===========+
| access_token\*   | personal access token                          | query | string    |
+------------------+------------------------------------------------+-------+-----------+
| owner\*          | Repository Owner Path (Organization or User    | path  | string    |
|                  | Path)                                          |       |           |
+------------------+------------------------------------------------+-------+-----------+
| repo\*           | Repository Path(path)                          | path  | string    |
+------------------+------------------------------------------------+-------+-----------+
| state            | Pull Request state:                            | query | string    |
|                  | all、open、closed、locked、merged，default:all |       |           |
+------------------+------------------------------------------------+-------+-----------+
| base             | base branch                                    | query | string    |
+------------------+------------------------------------------------+-------+-----------+
| since            | Since update time in ISO 8601 format, e.g.,    | quey  | string    |
|                  | ``2024-11-20T13:00:21+08:00``                  |       |           |
+------------------+------------------------------------------------+-------+-----------+
| direction        | Ascending/Descending order, default:desc 【asc | query | string    |
|                  | or desc】                                      |       |           |
+------------------+------------------------------------------------+-------+-----------+
| sort             | Sorting Fields: created、updated,              | query | string    |
|                  | default:created                                |       |           |
+------------------+------------------------------------------------+-------+-----------+
| milestone_number | milestone number                               | quey  | int       |
+------------------+------------------------------------------------+-------+-----------+
| labels           | Comma-separated list of label names.           | quey  | string    |
+------------------+------------------------------------------------+-------+-----------+
| page             | Current Page Number，default:1, default:1      | query | int       |
+------------------+------------------------------------------------+-------+-----------+
| per_page         | Items Per Page, Maximum                        | query | int       |
|                  | 100,default:20,default:20                      |       |           |
+------------------+------------------------------------------------+-------+-----------+
| author           | Optional. Username of the PR creator           | query | string    |
+------------------+------------------------------------------------+-------+-----------+
| assignee         | Optional. Username of the PR assignee          | query | string    |
+------------------+------------------------------------------------+-------+-----------+
| reviewer         | Optional. Username of the PR reviewer          | query | string    |
+------------------+------------------------------------------------+-------+-----------+
| merged_after     | Return merge requests merged after the         | query | string    |
|                  | specified time in ISO 8601 format, e.g.,       |       |           |
|                  | ``2024-11-20T13:00:21+08:00``                  |       |           |
+------------------+------------------------------------------------+-------+-----------+
| merged_before    | Return merge requests merged before the        | query | string    |
|                  | specified time in ISO 8601 format, e.g.,       |       |           |
|                  | ``2024-11-20T13:00:21+08:00``                  |       |           |
+------------------+------------------------------------------------+-------+-----------+
| only_count       | If true, only return the count of merge        | query | boolean   |
|                  | requests. Default: false                       |       |           |
+------------------+------------------------------------------------+-------+-----------+
| created_after    | Return merge requests created after the        | query | string    |
|                  | specified time in ISO 8601 format, e.g.,       |       |           |
|                  | ``2024-11-20T13:00:21+08:00``                  |       |           |
+------------------+------------------------------------------------+-------+-----------+
| created_before   | Return merge requests created before the       | query | string    |
|                  | specified time in ISO 8601 format, e.g.,       |       |           |
|                  | ``2024-11-20T13:00:21+08:00``                  |       |           |
+------------------+------------------------------------------------+-------+-----------+
| updated_before   | Return merge requests updated before the       | query | string    |
|                  | specified time in ISO 8601 format, e.g.,       |       |           |
|                  | ``2024-11-20T13:00:21+08:00``                  |       |           |
+------------------+------------------------------------------------+-------+-----------+
| updated_after    | Return merge requests updated after the        | query | string    |
|                  | specified time in ISO 8601 format, e.g.,       |       |           |
|                  | ``2024-11-20T13:00:21+08:00``                  |       |           |
+------------------+------------------------------------------------+-------+-----------+

..

   Note: The ISO 8601 time in the query parameter needs to be
   URL-encoded. For example, 2024-11-20T13:00:21+08:00 should be
   URL-encoded as 2024-11-20T13%3A00%3A21%2B08%3A00.

Response
~~~~~~~~

**only_count model（only_count: True）**

.. container:: highlight

   .. code:: text

      {
        "all": 1,
        "opened": 1,
        "closed": 0,
        "merged": 0,
        "locked": 0
      }

..

   Note: The state parameter is not effective in only_count mode.

**None only_count model (only_count: None or False)**

.. container:: highlight

   .. code:: text

      [
        {
          "number": 63,
          "html_url": "https://test.gitcode.net/One/One/merge_requests/63",
          "close_related_issue": null,
          "prune_branch": false,
          "draft": false,
          "url": "https://api.gitcode.net/api/v5/repos/One/One/pulls/63",
          "labels": [
            {
              "id": 381445,
              "color": "#008672",
              "name": "help wanted",
              "title": "help wanted",
              "repository_id": 243377,
              "type": null,
              "text_color": null
            },
            {
              "id": 381446,
              "color": "#CFD240",
              "name": "invalid",
              "title": "invalid",
              "repository_id": 243377,
              "type": null,
              "text_color": null
            },
            {
              "id": 381447,
              "color": "#D876E3",
              "name": "question",
              "title": "question",
              "repository_id": 243377,
              "type": null,
              "text_color": null
            }
          ],
          "user": {
            "id": "65f94ab6f21fa3084fc04823",
            "login": "csdntest13",
            "name": "csdntest13_gitcode",
            "state": "active",
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
            "avatar_path": null,
            "email": "",
            "name_cn": "csdntest13",
            "html_url": "https://test.gitcode.net/csdntest13",
            "tenant_name": null,
            "is_member": null
          },
          "assignees": [
            {
              "id": "64c71c3d64037b4af1c7a93f",
              "login": "green",
              "name": "百里",
              "state": "optional",
              "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/be/fb/7b9e393fbd80ca315dec249f2be6e6a7378f591609b6525798bc6d95abedc992.png?time=1712128581171",
              "avatar_path": null,
              "email": null,
              "name_cn": "green",
              "html_url": "https://test.gitcode.net/green",
              "assignee": true,
              "code_owner": false,
              "accept": false
            }
          ],
          "head": {
            "label": "test_b12",
            "ref": "test_b12",
            "sha": "fb6495834d1bf7a39dfdb44ad25e6f83c7136310",
            "user": {
              "id": "65f94ab6f21fa3084fc04823",
              "login": "csdntest13",
              "name": "csdntest13_gitcode",
              "state": "active",
              "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
              "avatar_path": null,
              "email": "",
              "name_cn": "csdntest13",
              "html_url": "https://test.gitcode.net/csdntest13",
              "tenant_name": null,
              "is_member": null
            },
            "repo": {
              "id": 243377,
              "full_path": "One/One",
              "human_name": "One / One",
              "name": "One",
              "path": "One",
              "description": "csdntest13的第一个项目(公开)",
              "namespace": {
                "id": 136909,
                "name": "One",
                "path": "One",
                "develop_mode": "normal",
                "region": null,
                "cell": "default",
                "kind": "group",
                "full_path": "One",
                "full_name": "One ",
                "parent_id": null,
                "visibility_level": 20,
                "enable_file_control": null,
                "owner_id": null
              },
              "owner": {
                "id": "65f94ab6f21fa3084fc04823",
                "login": "csdntest13",
                "name": "csdntest13_gitcode",
                "state": "active",
                "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
                "avatar_path": null,
                "email": "",
                "name_cn": "csdntest13",
                "html_url": "https://test.gitcode.net/csdntest13",
                "tenant_name": null,
                "is_member": null
              },
              "assigner": {
                "id": "64c71c3d64037b4af1c7a93f",
                "login": "green",
                "name": "百里",
                "state": null,
                "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/be/fb/7b9e393fbd80ca315dec249f2be6e6a7378f591609b6525798bc6d95abedc992.png?time=1712128581171",
                "avatar_path": null,
                "email": null,
                "name_cn": null,
                "html_url": "https://test.gitcode.net/green",
                "tenant_name": null,
                "is_member": null
              },
              "private": null,
              "public": null,
              "internal": false
            }
          },
          "base": {
            "label": "dev",
            "ref": "dev",
            "sha": "0c02dd57f8945791460a141f155dd2f4bd5dea86",
            "user": {
              "id": "65f94ab6f21fa3084fc04823",
              "login": "csdntest13",
              "name": "csdntest13_gitcode",
              "state": "active",
              "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
              "avatar_path": null,
              "email": "",
              "name_cn": "csdntest13",
              "html_url": "https://test.gitcode.net/csdntest13",
              "tenant_name": null,
              "is_member": null
            },
            "repo": {
              "id": 243377,
              "full_path": "One/One",
              "human_name": "One / One",
              "name": "One",
              "path": "One",
              "description": "csdntest13的第一个项目(公开)",
              "namespace": {
                "id": 136909,
                "name": "One",
                "path": "One",
                "develop_mode": "normal",
                "region": null,
                "cell": "default",
                "kind": "group",
                "full_path": "One",
                "full_name": "One ",
                "parent_id": null,
                "visibility_level": 20,
                "enable_file_control": null,
                "owner_id": null
              },
              "owner": {
                "id": "65f94ab6f21fa3084fc04823",
                "login": "csdntest13",
                "name": "csdntest13_gitcode",
                "state": "active",
                "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
                "avatar_path": null,
                "email": "",
                "name_cn": "csdntest13",
                "html_url": "https://test.gitcode.net/csdntest13",
                "tenant_name": null,
                "is_member": null
              },
              "assigner": {
                "id": "64c71c3d64037b4af1c7a93f",
                "login": "green",
                "name": "百里",
                "state": null,
                "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/be/fb/7b9e393fbd80ca315dec249f2be6e6a7378f591609b6525798bc6d95abedc992.png?time=1712128581171",
                "avatar_path": null,
                "email": null,
                "name_cn": null,
                "html_url": "https://test.gitcode.net/green",
                "tenant_name": null,
                "is_member": null
              },
              "private": null,
              "public": null,
              "internal": false
            }
          },
          "id": 70067,
          "iid": 63,
          "project_id": 243377,
          "title": "测试创建PR",
          "body": null,
          "state": "merged",
          "created_at": "2024-04-21T17:35:16.655+08:00",
          "updated_at": "2024-04-24T22:27:49.197+08:00",
          "merged_at": "2024-04-24T22:27:48.631+08:00",
          "closed_by": null,
          "closed_at": null,
          "title_html": null,
          "description_html": null,
          "target_branch": "dev",
          "source_branch": "test_b12",
          "squash_commit_message": null,
          "user_notes_count": 1,
          "upvotes": 0,
          "downvotes": 0,
          "source_project_id": 243377,
          "target_project_id": 243377,
          "work_in_progress": false,
          "milestone": null,
          "merge_when_pipeline_succeeds": false,
          "merge_status": "can_be_merged",
          "sha": "fb6495834d1bf7a39dfdb44ad25e6f83c7136310",
          "merge_commit_sha": "6c93b6e6fcf1ce1f0ce918d1a481f0500531ab72",
          "discussion_locked": null,
          "should_remove_source_branch": false,
          "force_remove_source_branch": false,
          "allow_collaboration": null,
          "allow_maintainer_to_push": null,
          "web_url": "https://test.gitcode.net/One/One/merge_requests/63",
          "time_stats": {
            "time_estimate": null,
            "total_time_spent": 0,
            "human_time_estimate": null,
            "human_total_time_spent": null
          },
          "squash": false,
          "merge_request_type": "MergeRequest",
          "has_pre_merge_ref": false,
          "review_mode": "approval",
          "is_source_branch_exist": true,
          "approval_merge_request_approvers": [
            {
              "id": 233,
              "username": "wunian2011",
              "name": "wunian2011",
              "nick_name": "测试吴",
              "name_cn": "wunian2011",
              "email": null,
              "state": "approve",
              "is_codeowner": false,
              "updated_at": "2024-04-24T21:40:11.095+08:00",
              "avatar_url": null
            },
            {
              "id": 277,
              "username": "renww",
              "name": "renww",
              "nick_name": "介简介简介简介简介简介简介简介简介",
              "name_cn": "renww",
              "email": null,
              "state": "optional",
              "is_codeowner": false,
              "updated_at": "2024-04-21T17:35:18.509+08:00",
              "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ee/dc/7602704ee7dcf13f4383a72d492b1813823afba729ae6e9115877a4a0128d990.jpg?time=1711447395118"
            }
          ],
          "approval_merge_request_testers": [],
          "added_lines": 1,
          "removed_lines": 0,
          "subscribed": true,
          "changes_count": "1",
          "latest_build_started_at": null,
          "latest_build_finished_at": null,
          "first_deployed_to_production_at": null,
          "pipeline": null,
          "diff_refs": {
            "base_sha": "0c02dd57f8945791460a141f155dd2f4bd5dea86",
            "head_sha": "fb6495834d1bf7a39dfdb44ad25e6f83c7136310",
            "start_sha": "b6d44deb0ca73d7a50916d0fea02c72edd6c924e"
          },
          "merge_error": null,
          "json_merge_error": null,
          "rebase_in_progress": null,
          "diverged_commits_count": null,
          "merge_request_reviewer_list": [],
          "merge_request_review_count": 0,
          "merge_request_reviewers_count": 0,
          "notes": 1,
          "unresolved_discussions_count": 0,
          "gate_check": true,
          "head_pipeline_id": null,
          "pipeline_status": "",
          "codequality_status": "success",
          "pipeline_status_with_code_quality": "",
          "from_forked_project": false,
          "forked_project_name": null,
          "can_delete_source_branch": true,
          "required_reviewers": [],
          "omega_mode": false,
          "root_mr_locked_detail": null,
          "source_git_url": "ssh://git@test.gitcode.net:2222/One/One.git",
          "auto_merge": false,
          "milestone": {
            "created_at": "2024-04-15T18:33:01+08:00",
            "description": "1",
            "due_on": "2024-04-29",
            "number": 73008,
            "repository_id": 249609,
            "state": "active",
            "title": "第二个里程碑",
            "updated_at": "2024-04-15T18:33:01+08:00",
            "url": "https://test.gitcode.net/xiaogang_test/test222/milestones/2"
          }
        }
      ]

Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls?access_token=xxxx' \


2. Merge a Pull Request
-----------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/merge``


Parameters
~~~~~~~~~~

+----------------+----------------------------------------------------------------------------------------------------------+-------+-----------+
| Parameter      | Description                                                                                              | Type  | Data Type |
+================+==========================================================================================================+=======+===========+
| access_token\* | personal access token                                                                                    | query | string    |
+----------------+----------------------------------------------------------------------------------------------------------+-------+-----------+
| owner\*        | Repository Owner Path (Organization or User Path)                                                        | path  | string    |
+----------------+----------------------------------------------------------------------------------------------------------+-------+-----------+
| repo\*         | Repository Path(path)                                                                                    | path  | string    |
+----------------+----------------------------------------------------------------------------------------------------------+-------+-----------+
| number\*       | PR number, i.e., the sequence number of the pull request in the repository.                              | path  | int       |
+----------------+----------------------------------------------------------------------------------------------------------+-------+-----------+
| merge_method   | 可选。合并PR的方法，merge（合并所有提交）、squash（扁平化分支合并）和rebase（变基并合并）。默认为merge。 | body  | string    |
+----------------+----------------------------------------------------------------------------------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "sha": "c20ac9624d2811a9313af29769dcf581b60c3044",
        "merged": true,
        "message": "Pull Request 已成功合并"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request PUT 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/merge?access_token=xxxx' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "merge_method": "merge"
      }'


3. Get Issues Associated with a Pull Request
--------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/issues``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
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
          "number": "1",
          "title": "[bug] test",
          "state": "open",
          "title": "进行稳定性测试",
          "url": "https://api.gitcode.com/api/v5/repos/sytest/paopao/issues/1",
          "body": "发生什么问题了？",
          "user": {
            "id": "681",
            "login": "test",
            "name": "test"
          },
          "labels": [
            {
              "color": "#008672",
              "name": "help wanted",
              "id": 381445,
              "title": "help wanted",
              "type": null,
              "textColor": "#FFFFFF"
            }
          ]
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/issues?access_token=xxxx' \


4. Submit a Pull Request Comment
--------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/comments``


Parameters
~~~~~~~~~~

+-----------------+--------------------------------+-------+-----------+
| Parameter       | Description                    | Type  | Data Type |
+=================+================================+=======+===========+
| access_token\*  | personal access token          | query | string    |
+-----------------+--------------------------------+-------+-----------+
| owner\*         | Repository Owner Path          | path  | string    |
|                 | (Organization or User Path)    |       |           |
+-----------------+--------------------------------+-------+-----------+
| repo\*          | Repository Path(path)          | path  | string    |
+-----------------+--------------------------------+-------+-----------+
| number\*        | PR number, i.e., the sequence  | path  | int       |
|                 | number of the pull request in  |       |           |
|                 | the repository.                |       |           |
+-----------------+--------------------------------+-------+-----------+
| body\*          | Comment Content                | body  | string    |
+-----------------+--------------------------------+-------+-----------+
| path            | Relative Path of the File      | body  | string    |
+-----------------+--------------------------------+-------+-----------+
| position        | Relative Line Number in the    | body  | int       |
|                 | Diff                           |       |           |
+-----------------+--------------------------------+-------+-----------+
| need_to_resolve | Whether it needs to be         | body  | boolean   |
|                 | resolved (true: review         |       |           |
|                 | comments need to be resolved,  |       |           |
|                 | false: review comments do not  |       |           |
|                 | need to be resolved, default   |       |           |
|                 | is false)                      |       |           |
+-----------------+--------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": "97219c08d421e55cfa841deca16a30f5d7269e10",
        "body": "22222"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request PUT 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/comments?access_token=xxxx' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "body": "body"
      }'


5. List Files in a Pull Request Commit
--------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/files``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "sha": "45e1211262a0ed24eeb85ac37f7776259ef0e7e1",
          "filename": "README.md",
          "status": null,
          "additions": "3",
          "deletions": "1",
          "blob_url": "https://ra w.gitcode.com/zzero/demo/blob/45e1211262a0ed24eeb85ac37f7776259ef0e7e1/README.md",
          "raw_url": "https://ra w.gitcode.com/zzero/demo/raw/45e1211262a0ed24eeb85ac37f7776259ef0e7e1/README.md",
          "patch": {
            "diff": "@@ -13,4 +13,6 @@ demo\n \r\n > covid_19 一个模拟感染人群爆发的小动画\r\n \r\n-> leetcode 算法解答\n\\ No newline at end of file\n+> leetcode 算法解答\r\n+\r\n+> juc包测试\n\\ No newline at end of file\n",
            "new_path": "README.md",
            "old_path": "README.md",
            "a_mode": "100644",
            "b_mode": "100644",
            "new_file": false,
            "renamed_file": false,
            "deleted_file": false,
            "too_large": false
          }
        },
        {
          "sha": "45e1211262a0ed24eeb85ac37f7776259ef0e7e1",
          "filename": "src/main/java/com/zhzh/sc/demo/juc/lock/VolatileDemo.java",
          "status": null,
          "additions": "3",
          "deletions": "0",
          "blob_url": "https://ra w.gitcode.com/zzero/demo/blob/45e1211262a0ed24eeb85ac37f7776259ef0e7e1/src/main/java/com/zhzh/sc/demo/juc/lock/VolatileDemo.java",
          "raw_url": "https://ra w.gitcode.com/zzero/demo/raw/45e1211262a0ed24eeb85ac37f7776259ef0e7e1/src/main/java/com/zhzh/sc/demo/juc/lock/VolatileDemo.java",
          "patch": {
            "diff": "@@ -15,6 +15,9 @@ public class VolatileDemo {\n         System.out.println(\"service end\");\n     }\n \n+    /**\n+     * 测试方法入口\n+     */\n     public static void main(String[] args) throws InterruptedException {\n         VolatileDemo v = new VolatileDemo();\n         new Thread(v::service, \"thread-1\").start();\n",
            "new_path": "src/main/java/com/zhzh/sc/demo/juc/lock/VolatileDemo.java",
            "old_path": "src/main/java/com/zhzh/sc/demo/juc/lock/VolatileDemo.java",
            "a_mode": "100644",
            "b_mode": "100644",
            "new_file": false,
            "renamed_file": false,
            "deleted_file": false,
            "too_large": false
          }
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/files?access_token=xxxx' \


6. Get All Comments for a Specific Pull Request
-----------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/comments``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number，default:1  | query | int       |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum         | query | int       |
|                | 100,default:20                  |       |           |
+----------------+---------------------------------+-------+-----------+
| direction      | asc/desc                        | query | int       |
+----------------+---------------------------------+-------+-----------+
| comment_type   | diff_comment/pr_comment         | query | string    |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": "de772738e6dab92174c0e86c052ccf9bed24f747",
          "body": "111",
          "created_at": "2024-04-19T07:48:59.755+00:00",
          "updated_at": "2024-04-19T07:48:59.755+00:00",
          "user": {
            "id": 708,
            "login": "Lzm_0916",
            "name": "Lzm_0916",
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/cb/da/6cb18d9ae9f1a94b4f640d3b848351c352c7869f33d0cb68e7acad4f224c4e23.png",
            "html_url": "https://test.gitcode.net/Lzm_0916"
          }
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/comments?access_token=xxxx' \


7. Create a Pull Request
------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls``


Parameters
~~~~~~~~~~

+------------------------+------------------------+-------+-----------+
| Parameter              | Description            | Type  | Data Type |
+========================+========================+=======+===========+
| access_token\*         | personal access token  | query | string    |
+------------------------+------------------------+-------+-----------+
| owner\*                | Repository Owner Path  | path  | string    |
|                        | (Organization or User  |       |           |
|                        | Path)                  |       |           |
+------------------------+------------------------+-------+-----------+
| repo\*                 | Repository Path(path)  | path  | string    |
+------------------------+------------------------+-------+-----------+
| title\*                | title                  | body  | string    |
+------------------------+------------------------+-------+-----------+
| head\*                 | head, eg：branch，fork | body  | string    |
|                        | pr:username:branch     |       |           |
+------------------------+------------------------+-------+-----------+
| base\*                 | base                   | body  | string    |
+------------------------+------------------------+-------+-----------+
| body                   | pr description         | body  | string    |
+------------------------+------------------------+-------+-----------+
| milestone_number       | milestone number       | body  | int       |
+------------------------+------------------------+-------+-----------+
| labels                 | Comma-separated list   | body  | string    |
|                        | of label names.        |       |           |
+------------------------+------------------------+-------+-----------+
| issue                  | The title and content  | body  | string    |
|                        | of the Pull Request    |       |           |
|                        | can be automatically   |       |           |
|                        | filled based on the    |       |           |
|                        | specified Issue ID.    |       |           |
+------------------------+------------------------+-------+-----------+
| assignees              | Optional. Approvals’   | body  | string    |
|                        | usernames, multiple    |       |           |
|                        | can be specified,      |       |           |
|                        | separated by commas    |       |           |
|                        | (e.g.,                 |       |           |
|                        | username1,username2).  |       |           |
|                        | Note: This option is   |       |           |
|                        | invalid if the         |       |           |
|                        | repository’s code      |       |           |
|                        | review settings        |       |           |
|                        | already have           |       |           |
|                        | designated approvals.  |       |           |
+------------------------+------------------------+-------+-----------+
| testers                | Optional. Testers’     | body  | string    |
|                        | usernames, multiple    |       |           |
|                        | can be specified,      |       |           |
|                        | separated by commas    |       |           |
|                        | (e.g.,                 |       |           |
|                        | username1,username2).  |       |           |
|                        | Note: This option is   |       |           |
|                        | invalid if the         |       |           |
|                        | repository’s code      |       |           |
|                        | review settings        |       |           |
|                        | already have           |       |           |
|                        | designated testers.    |       |           |
+------------------------+------------------------+-------+-----------+
| prune_source_branch    | Whether to delete the  | body  | boolean   |
|                        | source branch after    |       |           |
|                        | merging the PR.        |       |           |
|                        | Default: false (do not |       |           |
|                        | delete)                |       |           |
+------------------------+------------------------+-------+-----------+
| draft                  | wip pr,default: false  | body  | boolean   |
+------------------------+------------------------+-------+-----------+
| squash                 | squash, default: false | body  | boolean   |
+------------------------+------------------------+-------+-----------+
| squash_commit_message  | squash message         | body  | string    |
+------------------------+------------------------+-------+-----------+
| fork_path              | fork repo path         | body  | string    |
|                        | (owner/repo)           |       |           |
+------------------------+------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 11264998,
        "url": "https://gitcode.com/api/v5/repos/zzero/demo/pulls/6",
        "html_url": "https://gitcode.com/zzero/demo/pulls/6",
        "diff_url": "https://gitcode.com/zzero/demo/pulls/6.diff",
        "patch_url": "https://gitcode.com/zzero/demo/pulls/6.patch",
        "issue_url": "https://gitcode.com/api/v5/repos/zzero/demo/pulls/6/issues",
        "commits_url": "https://gitcode.com/api/v5/repos/zzero/demo/pulls/6/commits",
        "review_comments_url": "https://gitcode.com/api/v5/repos/zzero/demo/pulls/comments/{/number}",
        "review_comment_url": "https://gitcode.com/api/v5/repos/zzero/demo/pulls/comments",
        "comments_url": "https://gitcode.com/api/v5/repos/zzero/demo/pulls/6/comments",
        "number": 6,
        "title": "测试创建PR",
        "description": "update: 更新文件 dev_001.txt \nupdate: 更新文件 dev_001.txt ",
        "state": "opened",
        "created_at": "2024-04-14T20:53:13.185+08:00",
        "updated_at": "2024-04-14T20:53:22.634+08:00",
        "merged_by": null,
        "merged_at": null,
        "closed_by": null,
        "closed_at": null,
        "title_html": null,
        "description_html": null,
        "target_branch": "test_b5",
        "source_branch": "dev",
        "squash_commit_message": null,
        "user_notes_count": 0,
        "upvotes": 0,
        "downvotes": 0,
        "author": {
          "id": 494,
          "name": "csdntest13",
          "username": "csdntest13",
          "iam_id": "d8b3e018b2364546b946886a669d50fc",
          "nick_name": "csdntest13_gitcode",
          "state": "active",
          "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
          "avatar_path": null,
          "email": "csdntest13@noreply.gitcode.com",
          "name_cn": "csdntest13",
          "web_url": "https://gitcode.com/csdntest13",
          "tenant_name": null,
          "is_member": null
        },
        "assignee": null,
        "source_project_id": 243377,
        "target_project_id": 243377,
        "labels": [
          {
            "color": "#008672",
            "name": "help wanted",
            "id": 381445,
            "title": "help wanted",
            "type": null,
            "textColor": "#FFFFFF"
          },
          {
            "color": "#CFD240",
            "name": "invalid",
            "id": 381446,
            "title": "invalid",
            "type": null,
            "textColor": "#FFFFFF"
          },
          {
            "color": "#D876E3",
            "name": "question",
            "id": 381447,
            "title": "question",
            "type": null,
            "textColor": "#333333"
          }
        ],
        "work_in_progress": false,
        "milestone": null,
        "merge_when_pipeline_succeeds": false,
        "merge_status": "unchecked",
        "sha": "8da7a5c35e71deeb0bf1d9ecae70449c574749f2",
        "merge_commit_sha": null,
        "discussion_locked": null,
        "should_remove_source_branch": false,
        "force_remove_source_branch": false,
        "allow_collaboration": null,
        "allow_maintainer_to_push": null,
        "web_url": "https://gitcode.com/One/One/merge_requests/53",
        "time_stats": {
          "time_estimate": null,
          "total_time_spent": 0,
          "human_time_estimate": null,
          "human_total_time_spent": null
        },
        "squash": false,
        "merge_request_type": "MergeRequest",
        "has_pre_merge_ref": false,
        "review_mode": "approval",
        "is_source_branch_exist": true,
        "approval_merge_request_reviewers": [
          {
            "id": 43,
            "username": "green",
            "name": "green",
            "nick_name": null,
            "name_cn": "green",
            "email": null,
            "state": "optional",
            "is_codeowner": false,
            "updated_at": "2024-04-14T20:53:23.021+08:00",
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/be/fb/7b9e393fbd80ca315dec249f2be6e6a7378f591609b6525798bc6d95abedc992.png?time=1712128581171"
          }
        ],
        "approval_merge_request_approvers": [
          {
            "id": 277,
            "username": "renww",
            "name": "renww",
            "nick_name": null,
            "name_cn": "renww",
            "email": null,
            "state": "optional",
            "is_codeowner": false,
            "updated_at": "2024-04-14T20:53:23.751+08:00",
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ee/dc/7602704ee7dcf13f4383a72d492b1813823afba729ae6e9115877a4a0128d990.jpg?time=1711447395118"
          }
        ],
        "approval_merge_request_testers": [
          {
            "id": 43,
            "username": "green",
            "name": "green",
            "nick_name": null,
            "name_cn": "green",
            "email": null,
            "state": "optional",
            "is_codeowner": false,
            "updated_at": "2024-04-14T20:53:23.755+08:00",
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/be/fb/7b9e393fbd80ca315dec249f2be6e6a7378f591609b6525798bc6d95abedc992.png?time=1712128581171"
          },
          {
            "id": 277,
            "username": "renww",
            "name": "renww",
            "nick_name": null,
            "name_cn": "renww",
            "email": null,
            "state": "optional",
            "is_codeowner": false,
            "updated_at": "2024-04-14T20:53:23.755+08:00",
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ee/dc/7602704ee7dcf13f4383a72d492b1813823afba729ae6e9115877a4a0128d990.jpg?time=1711447395118"
          }
        ],
        "source_project": {
          "id": 243377,
          "description": "csdntest13的第一个项目(公开)",
          "name": "One",
          "name_with_namespace": "One / One",
          "path": "One",
          "path_with_namespace": "One/One",
          "develop_mode": "normal",
          "created_at": "2024-03-19T16:24:01.197+08:00",
          "updated_at": "2024-03-19T16:42:34.834+08:00",
          "archived": false,
          "is_kia": false,
          "ssh_url_to_repo": "ssh://git@gitcode.com:2222/One/One.git",
          "http_url_to_repo": "https://gitcode.com/One/One.git",
          "web_url": "https://gitcode.com/One/One",
          "readme_url": "https://gitcode.com/One/One/blob/main/README.md",
          "product_id": "28f96caf52004e81ab0bc38d60d11940",
          "product_name": null,
          "member_mgnt_mode": 3,
          "default_branch": "main",
          "tag_list": [],
          "license_url": null,
          "license": {
            "key": "Apache_License_v2.0",
            "name": null,
            "nickname": null,
            "html_url": null,
            "source_url": null
          },
          "avatar_url": null,
          "star_count": 1,
          "forks_count": 0,
          "open_issues_count": 108,
          "open_merge_requests_count": 32,
          "open_change_requests_count": null,
          "watch_count": 1,
          "last_activity_at": "2024-04-14T20:43:58.602+08:00",
          "namespace": {
            "id": 136909,
            "name": "One",
            "path": "One",
            "develop_mode": "normal",
            "region": null,
            "cell": "default",
            "kind": "group",
            "full_path": "One",
            "full_name": "One ",
            "parent_id": null,
            "visibility_level": 20,
            "enable_file_control": null,
            "owner_id": null
          },
          "empty_repo": false,
          "starred": false,
          "visibility": "public",
          "security": "internal",
          "has_updated_kia": false,
          "network_type": "green",
          "owner": null,
          "creator": {
            "id": 494,
            "name": "csdntest13",
            "username": "csdntest13",
            "iam_id": "d8b3e018b2364546b946886a669d50fc",
            "nick_name": "csdntest13_gitcode",
            "state": "active",
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
            "avatar_path": null,
            "email": "csdntest13@noreply.gitcode.com",
            "name_cn": "csdntest13",
            "web_url": "https://gitcode.com/csdntest13",
            "tenant_name": null,
            "is_member": null
          },
          "creator_id": 494,
          "forked_from_project": null,
          "item_type": "Project",
          "main_repository_language": ["Text", "#cccccc"],
          "mirror_project_data": null,
          "statistics": null,
          "branch_count": null,
          "tag_count": null,
          "member_count": null,
          "repo_replica_urls": null,
          "open_external_wiki": true,
          "release_count": null
        },
        "target_project": {
          "id": 243377,
          "description": "csdntest13的第一个项目(公开)",
          "name": "One",
          "name_with_namespace": "One / One",
          "path": "One",
          "path_with_namespace": "One/One",
          "develop_mode": "normal",
          "created_at": "2024-03-19T16:24:01.197+08:00",
          "updated_at": "2024-03-19T16:42:34.834+08:00",
          "archived": false,
          "is_kia": false,
          "ssh_url_to_repo": "ssh://git@gitcode.com:2222/One/One.git",
          "http_url_to_repo": "https://gitcode.com/One/One.git",
          "web_url": "https://gitcode.com/One/One",
          "readme_url": "https://gitcode.com/One/One/blob/main/README.md",
          "product_id": "28f96caf52004e81ab0bc38d60d11940",
          "product_name": null,
          "member_mgnt_mode": 3,
          "default_branch": "main",
          "tag_list": [],
          "license_url": null,
          "license": {
            "key": "Apache_License_v2.0",
            "name": null,
            "nickname": null,
            "html_url": null,
            "source_url": null
          },
          "avatar_url": null,
          "star_count": 1,
          "forks_count": 0,
          "open_issues_count": 108,
          "open_merge_requests_count": 32,
          "open_change_requests_count": null,
          "watch_count": 1,
          "last_activity_at": "2024-04-14T20:43:58.602+08:00",
          "namespace": {
            "id": 136909,
            "name": "One",
            "path": "One",
            "develop_mode": "normal",
            "region": null,
            "cell": "default",
            "kind": "group",
            "full_path": "One",
            "full_name": "One ",
            "parent_id": null,
            "visibility_level": 20,
            "enable_file_control": null,
            "owner_id": null
          },
          "empty_repo": false,
          "starred": false,
          "visibility": "public",
          "security": "internal",
          "has_updated_kia": false,
          "network_type": "green",
          "owner": null,
          "creator": {
            "id": 494,
            "name": "csdntest13",
            "username": "csdntest13",
            "iam_id": "d8b3e018b2364546b946886a669d50fc",
            "nick_name": "csdntest13_gitcode",
            "state": "active",
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
            "avatar_path": null,
            "email": "csdntest13@noreply.gitcode.com",
            "name_cn": "csdntest13",
            "web_url": "https://gitcode.com/csdntest13",
            "tenant_name": null,
            "is_member": null
          },
          "creator_id": 494,
          "forked_from_project": null,
          "item_type": "Project",
          "main_repository_language": ["Text", "#cccccc"],
          "mirror_project_data": null,
          "statistics": null,
          "branch_count": null,
          "tag_count": null,
          "member_count": null,
          "repo_replica_urls": null,
          "open_external_wiki": true,
          "release_count": null
        },
        "added_lines": 19860,
        "removed_lines": 1,
        "subscribed": true,
        "changes_count": "6",
        "latest_build_started_at": null,
        "latest_build_finished_at": null,
        "first_deployed_to_production_at": null,
        "pipeline": null,
        "diff_refs": {
          "base_sha": "0c02dd57f8945791460a141f155dd2f4bd5dea86",
          "head_sha": "8da7a5c35e71deeb0bf1d9ecae70449c574749f2",
          "start_sha": "fb6495834d1bf7a39dfdb44ad25e6f83c7136310"
        },
        "merge_error": null,
        "json_merge_error": null,
        "rebase_in_progress": null,
        "diverged_commits_count": null,
        "merge_request_assignee_list": [],
        "merge_request_reviewer_list": [],
        "user": {
          "can_merge": true
        },
        "merge_request_review_count": 0,
        "merge_request_reviewers_count": 0,
        "notes": 0,
        "unresolved_discussions_count": 0,
        "e2e_issues": [
          {
            "id": 13588,
            "issue_type": 7,
            "linked_issue_type": null,
            "issue_num": "issue100",
            "commit_id": null,
            "merge_request_id": 68253,
            "check_fail_reason": "",
            "check_result": true,
            "issue_link": "https://gitcode.com/One/One/issues/100",
            "created_at": "2024-04-14T20:53:23.772+08:00",
            "mks_id": null,
            "pbi_id": null,
            "pbi_name": null,
            "source": null,
            "issue_project_id": 243377,
            "title": "第boudoirripinings-45个issue",
            "issue_project": null,
            "auto_c_when_mr_merged": false
          }
        ],
        "gate_check": true,
        "head_pipeline_id": null,
        "pipeline_status": "",
        "codequality_status": "success",
        "pipeline_status_with_code_quality": "",
        "from_forked_project": false,
        "forked_project_name": null,
        "can_delete_source_branch": true,
        "required_reviewers": [],
        "omega_mode": false,
        "root_mr_locked_detail": null,
        "source_git_url": "ssh://git@gitcode.com:2222/One/One.git",
        "auto_merge": null
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls?access_token=xxxx' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "title": "title",
          "head": "dev",
          "base": "main"
      }'


8. Update a Pull Request
------------------------


Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}``


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
| number\*         | PR number, i.e., the sequence | path  | int       |
|                  | number of the pull request in |       |           |
|                  | the repository.               |       |           |
+------------------+-------------------------------+-------+-----------+
| title            | title                         | body  | string    |
+------------------+-------------------------------+-------+-----------+
| body             | body                          | body  | string    |
+------------------+-------------------------------+-------+-----------+
| state            | state                         | body  | string    |
+------------------+-------------------------------+-------+-----------+
| milestone_number | milestone number              | body  | int       |
+------------------+-------------------------------+-------+-----------+
| labels           | Comma-separated list of label | body  | string    |
|                  | names.                        |       |           |
+------------------+-------------------------------+-------+-----------+
| draft            | wip pr                        | body  | boolean   |
+------------------+-------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "title": "test_b3->dev",
        "body": "new: 新增文件 test_b3 \n2223333444444",
        "state": "opened",
        "created_at": "2024-03-28T22:23:29.999+08:00",
        "updated_at": "2024-04-14T21:06:52.499+08:00"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PATCH 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15?access_token=xxxx' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "body": "body"
      }'


9. Get a Pull Request
---------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "id": 111,
        "html_url": "http://gitcode.com/sytest/paopao/pull/1",
        "number": 1,
        "url": "https://api.gitcode.com/api/v5/repos/sytest/paopao/pulls/1",
        "issue_url": "https://api.gitcode.com/api/v5/repos/sytest/paopao/pulls/1/issues",
        "state": "open",
        "assignees_number": 1,
        "assignees": [
          {
            "id": 2,
            "login": "test",
            "name": "test_web",
            "avatar_url": "http://gitcode.com/sytest/paopao/pull/1.png",
            "html_url": "http://gitcode.com/sytest/paopao/pull/1",
            "assigness": true,
            "code_owner": false,
            "accept": true
          }
        ],
        "testers": [
          {
            "id": 2,
            "login": "test",
            "name": "test_web",
            "avatar_url": "http://gitcode.com/sytest/paopao/pull/1.png",
            "html_url": "http://gitcode.com/sytest/paopao/pull/1"
          }
        ],
        "labels": [
          {
            "id": 222,
            "name": "label1",
            "repository_id": 1,
            "created_at": "",
            "updated_at": ""
          }
        ],
        "created_at": "",
        "updated_at": "",
        "closed__at": "",
        "draft": false,
        "merged_at": "",
        "can_merge_check": false,
        "mergeable": true,
        "body": "Description",
        "user": {
          "id": "userId",
          "login": "test"
        },
        "head": {
          "label": "test",
          "ref": "test",
          "sha": "91861a9668041fc1c0ff51d1db66b6297179f5e6",
          "repo": {
            "path": "paopao",
            "name": "paopao"
          }
        },
        "base": {
          "label": "main",
          "ref": "main",
          "sha": "91861a9668041fc1c0ff51d1db66b6297179f5e6",
          "repo": {
            "path": "paopao",
            "name": "paopao"
          }
        },
        "prune_branch": false,
        "mergeable_state": {
              "merge_request_id": 111,
              "state": false,
              "status_without_user_auth": false,
              "conflict_passed": false,
              "branch_missing_passed": true,
              "non_ff_passed": true,
              "mr_state_passed": true,
              "merged_by_user_passed": true,
              "work_in_progress_passed": true,
              "resolve_discussion_passed": true,
              "ci_state_passed": true,
              "merge_by_self_passed": true,
              "can_force_merge": false,
              "approval_reviewers_required_passed": true,
              "approval_approvers_required_passed": true,
              "approval_testers_required_passed": true,
              "merge_request_switch": {
                  "review_mode": "approval",
                  "merge_method": "merge",
                  "only_allow_merge_if_all_discussions_are_resolved": false,
                  "disable_merge_by_self": false,
                  "only_allow_merge_if_pipeline_succeeds": false,
                  "disable_squash_merge": false,
                  "squash_merge_with_no_merge_commit": false,
                  "approval_required_reviewers_count": 0,
                  "approval_required_reviewers_branch": "*",
                  "add_notes_after_merged": false,
                  "mark_auto_merged_mr_as_closed": false,
                  "can_force_merge": false,
                  "can_reopen": true
              },
              "reason": {},
              "check_tasks_num": 0
          },
        "ref_pull_requests": [
              {
                  "id": 191973,
                  "number": 3,
                  "state": "merged",
                  "title": "dddd"
              }
        ]
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15?access_token=xxxx'


10. Get Commits for a Specific Pull Request
-------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/commits``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "sha": "91861a9668041fc1c0ff51d1db66b6297179f5e6",
          "html_url": "https://gitcode.com/sytest/paopao/blob/91861a9668041fc1c0ff51d1db66b6297179f5e6",
          "commit": {
            "author": {
              "login": "test",
              "name": "test",
              "email": "test@test.com",
              "date": "2024-03-28T11:19:33+08:00"
            },
            "committer": {
              "login": "test",
              "name": "test",
              "email": "test@test.com"
            },
            "message": "!5 333 * add 1/2/3/4. * add 1/2/3. "
          },
          "author": {
            "id": "id123",
            "login": "test",
            "name": "test",
            "avatar_url": "https://gitcode/pic.png",
            "html_url": "https://gitcode.com/test"
          },
          "committer": {
            "id": "id123",
            "login": "test",
            "name": "test",
            "avatar_url": "https://gitcode/pic.png",
            "html_url": "https://gitcode.com/test"
          },
          "parents": {
            "sha": "2e208a1e38f6a5a7b0cc3787688067ba082a8bb7",
            "shas": ["2e208a1e38f6a5a7b0cc3787688067ba082a8bb7"]
          }
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/commits?access_token=xxxx'


11. Create a Pull Request Label
-------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/labels``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
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

Response Code
~~~~~~~~~~~~~

.. container:: highlight

   .. code:: text

      HTTP status 201 No Content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/labels?access_token=xxxx' \
      --header 'Content-Type: application/json' \
      --data-raw '["feat"]'


12. Delete a Pull Request Label
-------------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/labels/{name}``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+
| name\*         | Comma-separated list of label   | path  | string    |
|                | names.                          |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      HTTP status 204 No Content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request DELETE 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/labels/bug?access_token=xxxx'


13. Process Pull Request Test
-----------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/test``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+
| force          | Whether to force the test to    | body  | boolean   |
|                | pass (default is false), only   |       |           |
|                | effective for administrators    |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      HTTP status 204 No Content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/test?access_token=xxxx'


14. Process Pull Request Approval
---------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/review``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+
| force          | Whether to force the test to    | body  | boolean   |
|                | pass (default is false), only   |       |           |
|                | effective for administrators    |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      HTTP status 204 No Content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request POST 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/review?access_token=xxxx'


15. Get the events Log of a Pull Request
----------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/operate_logs``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+
| sort           | desc(default), asc              | query | String    |
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
          "content": "Create mr issue link: **第boudoirripinings-24个issue** #79",
          "id": 274531,
          "action": "add_mr_issue_link",
          "merge_request_id": 70067,
          "created_at": "2024-04-23T11:32:08.522+08:00",
          "updated_at": "2024-04-23T11:32:08.522+08:00",
          "discussion_id": "18a5ab21f57cda175b8eabc2ec829a9e04d4d458",
          "project": "One/One",
          "assignee": null,
          "proposer": null,
          "user": {
            "id": "65f94ab6f21fa3084fc04823",
            "name": "csdntest13",
            "login": "csdntest13",
            "iam_id": "d8b3e018b2364546b946886a669d50fc",
            "nick_name": "csdntest13_gitcode",
            "state": "active",
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
            "avatar_path": null,
            "email": "csdntest13@noreply.gitcode.com",
            "name_cn": "csdntest13",
            "web_url": "https://test.gitcode.net/csdntest13",
            "tenant_name": null,
            "is_member": null
          }
        },
        {
          "content": "Create mr issue link: **第boudoirripinings-25个issue** #80",
          "id": 274529,
          "action": "add_mr_issue_link",
          "merge_request_id": 70067,
          "created_at": "2024-04-23T11:32:07.588+08:00",
          "updated_at": "2024-04-23T11:32:07.588+08:00",
          "discussion_id": "9b4b01dbe059dbdc120afd8bdf9fd865d4ea42b1",
          "project": "One/One",
          "assignee": null,
          "proposer": null,
          "user": {
            "id": "65f94ab6f21fa3084fc04823",
            "name": "csdntest13",
            "login": "csdntest13",
            "iam_id": "d8b3e018b2364546b946886a669d50fc",
            "nick_name": "csdntest13_gitcode",
            "state": "active",
            "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/ec/ba/4e7c4661b6154a7dd088d9fe64b4893383a2e318bf362350ce18d44df6ac7e37.png?time=1711533165876",
            "avatar_path": null,
            "email": "csdntest13@noreply.gitcode.com",
            "name_cn": "csdntest13",
            "web_url": "https://test.gitcode.net/csdntest13",
            "tenant_name": null,
            "is_member": null
          }
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/operate_logs?access_token=xxxx'


16. Get All Labels of a Pull Request
------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/labels``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 18517,
          "color": "#ED4014",
          "name": "bug",
          "repository_id": 198606,
          "url": "",
          "created_at": "2024-02-23",
          "updated_at": "2024-02-23",
          "text_color": "#FFFFFF"
        },
        {
          "id": 383740,
          "color": "#428BCA",
          "name": "performance",
          "repository_id": 198606,
          "url": "",
          "created_at": "2024-04-20",
          "updated_at": "2024-04-20",
          "text_color": "#FFFFFF"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/labels?access_token=xxxx'


17. Reset the Pull Request Test Status
--------------------------------------


Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/testers``


Parameters
~~~~~~~~~~

+----------------+-------------------------------------------------+-------+-----------+
| Parameter      | Description                                     | Type  | Data Type |
+================+=================================================+=======+===========+
| access_token\* | personal access token                           | query | string    |
+----------------+-------------------------------------------------+-------+-----------+
| owner\*        | Repository Owner Path (Organization or User     | path  | string    |
|                | Path)                                           |       |           |
+----------------+-------------------------------------------------+-------+-----------+
| repo\*         | Repository Path(path)                           | path  | string    |
+----------------+-------------------------------------------------+-------+-----------+
| number\*       | PR number, i.e., the sequence number of the     | path  | int       |
|                | pull request in the repository.                 |       |           |
+----------------+-------------------------------------------------+-------+-----------+
| reset_all      | 是否重置所有测试人，默认：false，只对管理员生效 | body  | boolean   |
+----------------+-------------------------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      HTTP status 204 No Content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PATCH 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/testers?access_token=xxxx' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "reset_all": "true"
      }'


18. Reset the Pull Request Approval Status
------------------------------------------


Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/assignees``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+
| reset_all      | reset all，default: false，only | body  | boolean   |
|                | worked for admin                |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      HTTP status 204 No Content


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PATCH 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/assignees?access_token=xxxx' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "reset_all": "true"
      }'


19. Get File Changes in a Pull Request
--------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/files.json``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "code": 0,
        "added_lines": 7,
        "remove_lines": 7,
        "count": 2,
        "diff_refs": {
          "base_sha": "db015522f67b15e868c5f929ff1af4cba9ddd112",
          "start_sha": "db015522f67b15e868c5f929ff1af4cba9ddd112",
          "head_sha": "93cd8303ac07886610d738baf7ddd620f04ee778"
        },
        "diffs": [
          {
            "new_blob_id": "b575bd06b44029dc12771503388d61ea383169cb",
            "statistic": {
              "type": "text_type",
              "path": "1",
              "old_path": "1",
              "new_path": "1",
              "view": false
            },
            "head": {
              "url": "https://pre-raw.gitcode.com/xiaogang/test/raw/93cd8303ac07886610d738baf7ddd620f04ee778/1",
              "commit_id": "93cd8303ac07886610d738baf7ddd620f04ee778"
            },
            "added_lines": 3,
            "remove_lines": 3,
            "content": {
              "text": [
                {
                  "line_content": "111",
                  "old_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_1_1",
                    "line_num": "1"
                  },
                  "new_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_1_1",
                    "line_num": ""
                  },
                  "type": "old"
                },
                {
                  "line_content": "111222",
                  "old_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_2_1",
                    "line_num": ""
                  },
                  "new_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_2_1",
                    "line_num": "1"
                  },
                  "type": "new"
                },
                {
                  "line_content": " ",
                  "old_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_2_2",
                    "line_num": "2"
                  },
                  "new_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_2_2",
                    "line_num": "2"
                  }
                },
                {
                  "line_content": "1113",
                  "old_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_3_3",
                    "line_num": "3"
                  },
                  "new_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_3_3",
                    "line_num": ""
                  },
                  "type": "old"
                },
                {
                  "line_content": "1113333",
                  "old_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_4_3",
                    "line_num": ""
                  },
                  "new_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_4_3",
                    "line_num": "3"
                  },
                  "type": "new"
                },
                {
                  "line_content": " ",
                  "old_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_4_4",
                    "line_num": "4"
                  },
                  "new_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_4_4",
                    "line_num": "4"
                  }
                },
                {
                  "line_content": "444",
                  "old_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_5_5",
                    "line_num": "5"
                  },
                  "new_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_5_5",
                    "line_num": ""
                  },
                  "type": "old"
                },
                {
                  "line_content": "4442423",
                  "old_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_6_5",
                    "line_num": ""
                  },
                  "new_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_6_5",
                    "line_num": "5"
                  },
                  "type": "new"
                },
                {
                  "line_content": " 5555",
                  "old_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_6_6",
                    "line_num": "6"
                  },
                  "new_line": {
                    "line_code": "356a192b7913b04c54574d18c28d46e6395428ab_6_6",
                    "line_num": "6"
                  }
                }
              ]
            }
          },
          {
            "new_blob_id": "1d3e5f08788ce215053e01fd54a76c6c6fbc1ddc",
            "statistic": {
              "type": "text_type",
              "path": "2",
              "old_path": "2",
              "new_path": "2",
              "view": false
            },
            "head": {
              "url": "https://pre-raw.gitcode.com/xiaogang/test/raw/93cd8303ac07886610d738baf7ddd620f04ee778/2",
              "commit_id": "93cd8303ac07886610d738baf7ddd620f04ee778"
            },
            "added_lines": 4,
            "remove_lines": 4,
            "content": {
              "text": [
                {
                  "line_content": " 11111",
                  "old_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_1_1",
                    "line_num": "1"
                  },
                  "new_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_1_1",
                    "line_num": "1"
                  }
                },
                {
                  "line_content": "22222",
                  "old_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_2_2",
                    "line_num": "2"
                  },
                  "new_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_2_2",
                    "line_num": ""
                  },
                  "type": "old"
                },
                {
                  "line_content": "22222adfsasf",
                  "old_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_3_2",
                    "line_num": ""
                  },
                  "new_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_3_2",
                    "line_num": "2"
                  },
                  "type": "new"
                },
                {
                  "line_content": " 3333",
                  "old_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_3_3",
                    "line_num": "3"
                  },
                  "new_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_3_3",
                    "line_num": "3"
                  }
                },
                {
                  "line_content": "",
                  "old_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_4_4",
                    "line_num": "4"
                  },
                  "new_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_4_4",
                    "line_num": ""
                  },
                  "type": "old"
                },
                {
                  "line_content": "",
                  "old_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_5_4",
                    "line_num": "5"
                  },
                  "new_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_5_4",
                    "line_num": ""
                  },
                  "type": "old"
                },
                {
                  "line_content": "4444",
                  "old_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_6_4",
                    "line_num": "6"
                  },
                  "new_line": {
                    "line_code": "da4b9237bacccdf19c0760cab7aec4a8359010b0_6_4",
                    "line_num": ""
                  },
                  "type": "old"
                }
              ]
            }
          }
        ]
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/15/files.json?access_token=xxxx'


20. Get File Content
--------------------


Request
~~~~~~~

``GET https://raw.gitcode.com/{owner}/{repo}/raw/{head_sha}/{name}``

   To obtain the file changes in a specific pull request (PR), you can
   use the following endpoint: 《19. Get File Changes in a Pull
   Request》\ ``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/files.json``
   Once you have retrieved the response, you can directly access the URL
   provided in the diffs.head.url field by copying it into your web
   browser.


21. Get the List of Enterprise Pull Requests
--------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/enterprises/{enterprise}/pull_requests``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| enterprise\*   | Enterprise Path(path/login)     | path  | string    |
+----------------+---------------------------------+-------+-----------+
| repo           | 可选。Repository Path(path)     | query | string    |
+----------------+---------------------------------+-------+-----------+
| state          | 可选。Pull Request 状态         | query | string    |
+----------------+---------------------------------+-------+-----------+
| issue_number   | issue全局id                     | query | int       |
+----------------+---------------------------------+-------+-----------+
| sort           | 可选。Sorting Fields，Default:  | query | string    |
|                | Sorted by Creation Time         |       |           |
+----------------+---------------------------------+-------+-----------+
| direction      | asc/desc                        | query | string    |
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
          "id": 71020,
          "url": "https://test.gitcode.net/api/v5/repos/test/test/1",
          "html_url": "https://test.gitcode.net/test/test/1",
          "number": 1,
          "state": "merged",
          "assignees_number": 0,
          "testers_number": 0,
          "assignees": [],
          "testers": [],
          "mergeable": null,
          "can_merge_check": true,
          "head": {
            "ref": "main",
            "sha": "d874402d259744a00121c2cff0febc8554339aef",
            "repo": {
              "path": "test",
              "name_space": {
                "path": "repo-dev"
              },
              "assigner": {
                "id": "uuid",
                "login": "Lzm_0916",
                "name": "Lzm_0916"
              }
            }
          },
          "base": {
            "ref": null,
            "sha": null,
            "repo": {
              "path": "test",
              "name_space": {
                "path": "repo-dev"
              }
            }
          },
          "milestone": {
            "created_at": "2024-04-15T18:33:01+08:00",
            "description": "1",
            "due_on": "2024-04-29",
            "number": 73008,
            "repository_id": 249609,
            "state": "active",
            "title": "第二个里程碑",
            "updated_at": "2024-04-15T18:33:01+08:00",
            "url": "https://test.gitcode.net/xiaogang_test/test222/milestones/2"
          }
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/enterprises/xiaogang_test/pull_requests?access_token=xxxx'


22. Get a Comment of Pull Request
---------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/comments/{id}``


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
        "id": 1486664,
        "body": "1111112222222",
        "comment_type": "DiscussionNote",
        "user": {
          "id": "303745",
          "login": "yinlin",
          "name": "yinlin-昵称",
          "type": "User"
        },
        "target": {
          "issue": {
            "id": 478892,
            "title": "1111",
            "number": "478892"
          }
        },
        "created_at": "2024-09-27T14:58:51+08:00",
        "updated_at": "2024-09-27T14:58:51+08:00"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/repos/Hello_worldsss/IK_001_01/pulls/comments/1486664?access_token=xxxx'


23. Check if a Pull Request is Merged
-------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/merge``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "message": "Pull Request已经合并"
      }

or

.. container:: highlight

   .. code:: text

      {
        "error": "Pull Request不存在或未合并"
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request GET 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/pulls/1/merge?access_token=xxx'


24. Assign a User to Approve a Pull Request
-------------------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/assignees``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+
| assignees\*    | User’s personal space address,  | body  | string    |
|                | separated by commas.            |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {
        "assignees_number": 1
      }


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request POST 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/pulls/2/assignees?access_token=xxx' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "assignees": "xiaogang"
      }'


25. Cancel a User’s Approval on a Pull Request
----------------------------------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/assignees``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+
| assignees\*    | User’s personal space address,  | body  | string    |
|                | separated by commas.            |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

无


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request DELETE 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/pulls/2/assignees?access_token=xxxx' \
      --form 'assignees="xiaogang"'


26. Edit a Comment
------------------


Request
~~~~~~~

``PATCH https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/comments/{id}``


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
| id\*           | the ID of a cmment           | path     | int       |
+----------------+------------------------------+----------+-----------+
| body\*         | Comment Content              | formData | string    |
+----------------+------------------------------+----------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {}


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request PATCH 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/pulls/comments/1495107?access_token=xxxx' \
      --header 'Content-Type: application/json' \
      --data-raw '{
          "body": "Duis enim esse"
      }'


27. Delete a Comment
--------------------


Request
~~~~~~~

``DELETE https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/comments/{id}``


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
| id\*           | the ID of a comment             | path  | int       |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      {}


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location -g --request DELETE 'https://api.gitcode.com/api/v5/repos/dengmengmian/oneapi/pulls/comments/1495107?access_token=xxxx'


28. Replace All Labels on a Pull Request
----------------------------------------


Request
~~~~~~~

``PUT https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/labels``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+
| labels\*       | new labels, eg: [“feat”, “bug”] | body  | array     |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

无


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com/api/v5/repos/xiaogang_test/test222/pulls/1/labels?access_token=xxxx' \
      --header 'Content-Type: application/json' \
      --data '[
          "bug"
      ]'


29. Assign a User to Test a Pull Request
----------------------------------------


Request
~~~~~~~

``POST https://api.gitcode.com/api/v5/repos/{owner}/{repo}/pulls/{number}/testers``


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
| number\*       | PR number, i.e., the sequence   | path  | int       |
|                | number of the pull request in   |       |           |
|                | the repository.                 |       |           |
+----------------+---------------------------------+-------+-----------+
| testers\*      | User’s personal space address,  | body  | string    |
|                | separated by commas.            |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 43,
          "login": "green",
          "name": "green",
          "avatar_url": "https://gitcode-img.obs.cn-south-1.myhuaweicloud.com:443/be/fb/7b9e393fbd80ca315dec249f2be6e6a7378f591609b6525798bc6d95abedc992.png?time=1712128581171"
        },
        {
          "id": 452,
          "login": "zhanghq2",
          "name": "zhanghq2"
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request PUT 'https://api.gitcode.com//api/v5/repos/xiaogang_test/test222/pulls/15/testers?access_token=xxxx' \
      --header 'Content-Type: application/json;charset=UTF-8' \
      --data '{
          "testers":"green,zhanghq2"
      }'


30. Get the List of Organization Pull Requests
----------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/org/{org}/pull_requests``


Parameters
~~~~~~~~~~

+----------------+---------------------------------+-------+-----------+
| Parameter      | Description                     | Type  | Data Type |
+================+=================================+=======+===========+
| access_token\* | personal access token           | query | string    |
+----------------+---------------------------------+-------+-----------+
| org\*          | org(path/login)                 | path  | string    |
+----------------+---------------------------------+-------+-----------+
| state          | state                           | query | string    |
+----------------+---------------------------------+-------+-----------+
| issue_number   | Global Issue ID (not iid)       | int   | string    |
+----------------+---------------------------------+-------+-----------+
| sort           | Sorting Fields，Default: Sorted | query | string    |
|                | by Creation Time                |       |           |
+----------------+---------------------------------+-------+-----------+
| direction      | asc/desc                        | query | string    |
+----------------+---------------------------------+-------+-----------+
| page           | Current Page Number，default:1  | query | int       |
+----------------+---------------------------------+-------+-----------+
| per_page       | Items Per Page, Maximum         | int   | string    |
|                | 100,default:20                  |       |           |
+----------------+---------------------------------+-------+-----------+


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
        {
          "id": 71020,
          "url": "https://test.gitcode.net/api/v5/repos/test/test/1",
          "html_url": "https://test.gitcode.net/test/test/1",
          "number": 1,
          "state": "merged",
          "assignees_number": 0,
          "testers_number": 0,
          "assignees": [],
          "testers": [],
          "mergeable": null,
          "can_merge_check": true,
          "head": {
            "ref": "main",
            "sha": "d874402d259744a00121c2cff0febc8554339aef",
            "repo": {
              "path": "test",
              "name_space": {
                "path": "repo-dev"
              },
              "assigner": {
                "id": "uuid",
                "login": "Lzm_0916",
                "name": "Lzm_0916"
              }
            }
          },
          "base": {
            "ref": null,
            "sha": null,
            "repo": {
              "path": "test",
              "name_space": {
                "path": "repo-dev"
              }
            }
          }
        }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location 'https://api.gitcode.com/api/v5/org/xiaogang_test/pull_requests?access_token=xxxx'


31. Get Pull Requests Associated with an Enterprise Issue
---------------------------------------------------------


Request
~~~~~~~

``GET https://api.gitcode.com/api/v5/enterprises/{enterprise}/issues/{number}/pull_requests``


Parameters
~~~~~~~~~~

============== ========================= ===== =========
Parameter      Description               Type  Data Type
============== ========================= ===== =========
access_token\* personal access token     query string
enterprise\*   org(path/login)           path  string
number\*       Global Issue ID (not iid) path  Integer
============== ========================= ===== =========


Response
~~~~~~~~

.. container:: highlight

   .. code:: text

      [
          {
              "number": 1,
              "html_url": "https://test.gitcode.net/owner-test/wonderful1/merge_requests/1",
              "url": "https://test.gitcode.net/api/v5/repos/owner-test/wonderful1/pulls/1",
              "close_related_issue": 0,
              "prune_branch": false,
              "draft": false,
              "labels": [],
              "user": {
                  "id": "654c61e5560ed95fd216cf31",
                  "login": "csdn_fenglh",
                  "name": "fenglh",
                  "state": "active",
                  "email": "",
                  "name_cn": "",
                  "html_url": "https://test.gitcode.net/csdn_fenglh"
              },
              "assignees": [],
              "testers": [],
              "head": {
                  "label": "wonderful1-patch-1",
                  "ref": "wonderful1-patch-1",
                  "sha": "9931ba43e2c485741192d8e9a0b698fed79100f9",
                  "user": {
                      "id": "6638af02bbeee41d0fe74c35",
                      "login": "malongge5",
                      "name": "malongge5",
                      "state": "active",
                      "email": "malongge5@noreply.gitcode.com",
                      "name_cn": "",
                      "html_url": "https://test.gitcode.net/malongge5"
                  },
                  "repo": {
                      "id": 686738,
                      "full_path": "owner-test/wonderful1",
                      "full_name": "owner-test/wonderful1",
                      "human_name": "测试 / wonderful1",
                      "name": "wonderful1",
                      "path": "wonderful1",
                      "description": "我的测试代码仓库",
                      "owner": {
                          "id": "6638af02bbeee41d0fe74c35",
                          "login": "malongge5",
                          "name": "malongge5",
                          "state": "active",
                          "email": "malongge5@noreply.gitcode.com",
                          "name_cn": "",
                          "html_url": "https://test.gitcode.net/malongge5"
                      },
                      "assigner": {
                          "id": "6638af02bbeee41d0fe74c35",
                          "login": "malongge5",
                          "name": "malongge5",
                          "state": "active",
                          "email": "malongge5@noreply.gitcode.com",
                          "name_cn": "",
                          "html_url": "https://test.gitcode.net/malongge5"
                      },
                      "internal": false,
                      "html_url": "https://test.gitcode.net/owner-test/wonderful1.git"
                  }
              },
              "base": {
                  "label": "abc",
                  "ref": "abc",
                  "sha": "44a8d3e1142468ab2db0fa8c3402a71ccf891572",
                  "user": {
                      "id": "6638af02bbeee41d0fe74c35",
                      "login": "malongge5",
                      "name": "malongge5",
                      "state": "active",
                      "email": "malongge5@noreply.gitcode.com",
                      "name_cn": "",
                      "html_url": "https://test.gitcode.net/malongge5"
                  },
                  "repo": {
                      "id": 686738,
                      "full_path": "owner-test/wonderful1",
                      "full_name": "owner-test/wonderful1",
                      "human_name": "测试 / wonderful1",
                      "name": "wonderful1",
                      "path": "wonderful1",
                      "description": "我的测试代码仓库",
                      "owner": {
                          "id": "6638af02bbeee41d0fe74c35",
                          "login": "malongge5",
                          "name": "malongge5",
                          "state": "active",
                          "email": "malongge5@noreply.gitcode.com",
                          "name_cn": "",
                          "html_url": "https://test.gitcode.net/malongge5"
                      },
                      "assigner": {
                          "id": "6638af02bbeee41d0fe74c35",
                          "login": "malongge5",
                          "name": "malongge5",
                          "state": "active",
                          "email": "malongge5@noreply.gitcode.com",
                          "name_cn": "",
                          "html_url": "https://test.gitcode.net/malongge5"
                      },
                      "internal": false,
                      "html_url": "https://test.gitcode.net/owner-test/wonderful1.git"
                  }
              },
              "id": 191980,
              "iid": 1,
              "project_id": 686738,
              "title": "hhhh",
              "body": "update: 更新文件 README.md ",
              "state": "merged",
              "assignees_number": 0,
              "testers_number": 0,
              "created_at": "2024-11-23T20:51:32+08:00",
              "updated_at": "2024-12-13T16:16:54+08:00",
              "merged_at": "2024-11-25T20:40:19+08:00",
              "closed_at": "",
              "target_branch": "abc",
              "source_branch": "wonderful1-patch-1",
              "source_project_id": 686738,
              "force_remove_source_branch": false,
              "web_url": "https://test.gitcode.net/owner-test/wonderful1/merge_requests/1",
              "merge_request_type": "MergeRequest",
              "review_mode": "approval",
              "added_lines": 2,
              "removed_lines": 2,
              "diff_refs": {
                  "base_sha": "91a8edc0db6889fc7309d3306da7b12113e4a73f",
                  "head_sha": "9931ba43e2c485741192d8e9a0b698fed79100f9",
                  "start_sha": "91a8edc0db6889fc7309d3306da7b12113e4a73f"
              },
              "notes": 0,
              "pipeline_status": "",
              "pipeline_status_with_code_quality": "",
              "source_git_url": "ssh://git@test.gitcode.net:2222/owner-test/wonderful1.git",
              "can_merge_check": true,
              "mergeable": true,
              "locked": false,
              "diff_url": "https://test.gitcode.net/owner-test/wonderful1/merge_requests/1.diff",
              "patch_url": "https://test.gitcode.net/owner-test/wonderful1/merge_requests/1.patch",
              "commits_url": "https://test.gitcode.net/api/v5/repos/owner-test/wonderful1/pulls/1/commits",
              "comments_url": "https://test.gitcode.net/api/v5/repos/owner-test/wonderful1/pulls/1/comments",
              "issue_url": "https://test.gitcode.net/api/v5/repos/owner-test/wonderful1/pulls/1/issues"
          }
      ]


Demo
~~~~

.. container:: highlight

   .. code:: text

      curl --location --request GET 'https://api.gitcode.com/api/v5/enterprises/owner-test/issues/471521/pull_requests?access_token=***'

.. This page was generated from upstream GitCode Help documentation.
.. Source URL: https://docs.gitcode.com/en/docs/repos/pulls/
.. Do not edit by hand; re-run scripts/build_gitcode_sphinx_docs.py
