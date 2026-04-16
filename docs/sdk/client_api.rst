Client API Reference
====================

This reference is organized by the chained SDK entrypoints users call at
runtime, such as ``GitCode.branches.list()`` and
``AsyncGitCode.pulls.list()``.

``GitCode`` and ``AsyncGitCode`` are context managers: use ``with GitCode(...)``
and ``async with AsyncGitCode(...)`` so the default httpx client is closed when
the block ends. The same applies to ``SyncAPIClient`` and ``AsyncAPIClient``;
see :doc:`quickstart` for examples. If you pass ``http_client=``, only that
outer client performs transport teardown when you close it.

Synchronous client
------------------

.. currentmodule:: gitcode_api._client

.. autoclass:: GitCode
   :members: close
   :inherited-members:
   :no-index:

Repository resources
~~~~~~~~~~~~~~~~~~~~

``GitCode.repos``
^^^^^^^^^^^^^^^^^

.. autoattribute:: GitCode.repos
   :no-index:

.. currentmodule:: gitcode_api.resources.repositories

.. automethod:: ReposResource.get
   :no-index:
.. automethod:: ReposResource.list_user
   :no-index:
.. automethod:: ReposResource.list_for_owner
   :no-index:
.. automethod:: ReposResource.create_personal
   :no-index:
.. automethod:: ReposResource.create_for_org
   :no-index:
.. automethod:: ReposResource.update
   :no-index:
.. automethod:: ReposResource.delete
   :no-index:
.. automethod:: ReposResource.fork
   :no-index:
.. automethod:: ReposResource.list_forks
   :no-index:
.. automethod:: ReposResource.list_contributors
   :no-index:
.. automethod:: ReposResource.list_languages
   :no-index:
.. automethod:: ReposResource.list_stargazers
   :no-index:
.. automethod:: ReposResource.list_subscribers
   :no-index:
.. automethod:: ReposResource.update_module_settings
   :no-index:
.. automethod:: ReposResource.update_reviewer_settings
   :no-index:
.. automethod:: ReposResource.set_org_repo_status
   :no-index:
.. automethod:: ReposResource.transfer_to_org
   :no-index:
.. automethod:: ReposResource.get_transition
   :no-index:
.. automethod:: ReposResource.update_transition
   :no-index:
.. automethod:: ReposResource.update_push_config
   :no-index:
.. automethod:: ReposResource.get_push_config
   :no-index:
.. automethod:: ReposResource.upload_image
   :no-index:
.. automethod:: ReposResource.upload_file
   :no-index:
.. automethod:: ReposResource.update_repo_settings
   :no-index:
.. automethod:: ReposResource.get_repo_settings
   :no-index:
.. automethod:: ReposResource.get_pull_request_settings
   :no-index:
.. automethod:: ReposResource.update_pull_request_settings
   :no-index:
.. automethod:: ReposResource.set_member_role
   :no-index:
.. automethod:: ReposResource.transfer
   :no-index:
.. automethod:: ReposResource.list_customized_roles
   :no-index:
.. automethod:: ReposResource.get_download_statistics
   :no-index:
.. automethod:: ReposResource.get_contributor_statistics
   :no-index:
.. automethod:: ReposResource.list_events
   :no-index:

``GitCode.contents``
^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.contents
   :no-index:

.. currentmodule:: gitcode_api.resources.repositories

.. automethod:: RepoContentsResource.get
   :no-index:
.. automethod:: RepoContentsResource.create
   :no-index:
.. automethod:: RepoContentsResource.update
   :no-index:
.. automethod:: RepoContentsResource.delete
   :no-index:
.. automethod:: RepoContentsResource.list_paths
   :no-index:
.. automethod:: RepoContentsResource.get_tree
   :no-index:
.. automethod:: RepoContentsResource.get_blob
   :no-index:
.. automethod:: RepoContentsResource.get_raw
   :no-index:

``GitCode.branches``
^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.branches
   :no-index:

.. currentmodule:: gitcode_api.resources.repositories

.. automethod:: BranchesResource.list
   :no-index:
.. automethod:: BranchesResource.get
   :no-index:
.. automethod:: BranchesResource.create
   :no-index:
.. automethod:: BranchesResource.list_protected
   :no-index:

``GitCode.commits``
^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.commits
   :no-index:

.. currentmodule:: gitcode_api.resources.repositories

.. automethod:: CommitsResource.list
   :no-index:
.. automethod:: CommitsResource.get
   :no-index:
.. automethod:: CommitsResource.compare
   :no-index:
.. automethod:: CommitsResource.list_comments
   :no-index:
.. automethod:: CommitsResource.get_comment
   :no-index:
.. automethod:: CommitsResource.create_comment
   :no-index:
.. automethod:: CommitsResource.update_comment
   :no-index:
.. automethod:: CommitsResource.delete_comment
   :no-index:

Collaboration resources
~~~~~~~~~~~~~~~~~~~~~~~

``GitCode.issues``
^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.issues
   :no-index:

.. currentmodule:: gitcode_api.resources.collaboration

.. automethod:: IssuesResource.list
   :no-index:
.. automethod:: IssuesResource.get
   :no-index:
.. automethod:: IssuesResource.create
   :no-index:
.. automethod:: IssuesResource.update
   :no-index:
.. automethod:: IssuesResource.list_comments
   :no-index:
.. automethod:: IssuesResource.create_comment
   :no-index:
.. automethod:: IssuesResource.get_comment
   :no-index:
.. automethod:: IssuesResource.update_comment
   :no-index:
.. automethod:: IssuesResource.delete_comment
   :no-index:
.. automethod:: IssuesResource.list_pull_requests
   :no-index:
.. automethod:: IssuesResource.add_labels
   :no-index:
.. automethod:: IssuesResource.remove_label
   :no-index:
.. automethod:: IssuesResource.list_enterprise
   :no-index:
.. automethod:: IssuesResource.list_user
   :no-index:
.. automethod:: IssuesResource.list_org
   :no-index:
.. automethod:: IssuesResource.get_enterprise_issue
   :no-index:
.. automethod:: IssuesResource.list_enterprise_comments
   :no-index:
.. automethod:: IssuesResource.list_enterprise_labels
   :no-index:
.. automethod:: IssuesResource.list_operation_logs
   :no-index:

``GitCode.pulls``
^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.pulls
   :no-index:

.. currentmodule:: gitcode_api.resources.collaboration

.. automethod:: PullsResource.list
   :no-index:
.. automethod:: PullsResource.get
   :no-index:
.. automethod:: PullsResource.create
   :no-index:
.. automethod:: PullsResource.update
   :no-index:
.. automethod:: PullsResource.merge
   :no-index:
.. automethod:: PullsResource.get_merge_status
   :no-index:
.. automethod:: PullsResource.list_commits
   :no-index:
.. automethod:: PullsResource.list_files
   :no-index:
.. automethod:: PullsResource.list_comments
   :no-index:
.. automethod:: PullsResource.create_comment
   :no-index:
.. automethod:: PullsResource.get_comment
   :no-index:
.. automethod:: PullsResource.update_comment
   :no-index:
.. automethod:: PullsResource.delete_comment
   :no-index:
.. automethod:: PullsResource.list_labels
   :no-index:
.. automethod:: PullsResource.add_labels
   :no-index:
.. automethod:: PullsResource.replace_labels
   :no-index:
.. automethod:: PullsResource.remove_label
   :no-index:
.. automethod:: PullsResource.request_review
   :no-index:
.. automethod:: PullsResource.list_operation_logs
   :no-index:
.. automethod:: PullsResource.request_test
   :no-index:
.. automethod:: PullsResource.update_testers
   :no-index:
.. automethod:: PullsResource.add_testers
   :no-index:
.. automethod:: PullsResource.update_assignees
   :no-index:
.. automethod:: PullsResource.add_assignees
   :no-index:
.. automethod:: PullsResource.remove_assignees
   :no-index:
.. automethod:: PullsResource.list_issues
   :no-index:
.. automethod:: PullsResource.list_enterprise
   :no-index:
.. automethod:: PullsResource.list_org
   :no-index:
.. automethod:: PullsResource.list_issue_pull_requests
   :no-index:

``GitCode.labels``
^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.labels
   :no-index:

.. currentmodule:: gitcode_api.resources.collaboration

.. automethod:: LabelsResource.list
   :no-index:
.. automethod:: LabelsResource.create
   :no-index:
.. automethod:: LabelsResource.update
   :no-index:
.. automethod:: LabelsResource.delete
   :no-index:
.. automethod:: LabelsResource.clear_issue_labels
   :no-index:
.. automethod:: LabelsResource.replace_issue_labels
   :no-index:
.. automethod:: LabelsResource.list_enterprise
   :no-index:

``GitCode.milestones``
^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.milestones
   :no-index:

.. currentmodule:: gitcode_api.resources.collaboration

.. automethod:: MilestonesResource.list
   :no-index:
.. automethod:: MilestonesResource.get
   :no-index:
.. automethod:: MilestonesResource.create
   :no-index:
.. automethod:: MilestonesResource.update
   :no-index:
.. automethod:: MilestonesResource.delete
   :no-index:

``GitCode.members``
^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.members
   :no-index:

.. currentmodule:: gitcode_api.resources.collaboration

.. automethod:: MembersResource.add_or_update
   :no-index:
.. automethod:: MembersResource.remove
   :no-index:
.. automethod:: MembersResource.list
   :no-index:
.. automethod:: MembersResource.get
   :no-index:
.. automethod:: MembersResource.get_permission
   :no-index:

Account and discovery resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``GitCode.users``
^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.users
   :no-index:

.. currentmodule:: gitcode_api.resources.account

.. automethod:: UsersResource.get
   :no-index:
.. automethod:: UsersResource.me
   :no-index:
.. automethod:: UsersResource.list_emails
   :no-index:
.. automethod:: UsersResource.list_events
   :no-index:
.. automethod:: UsersResource.list_repos
   :no-index:
.. automethod:: UsersResource.create_key
   :no-index:
.. automethod:: UsersResource.list_keys
   :no-index:
.. automethod:: UsersResource.delete_key
   :no-index:
.. automethod:: UsersResource.get_key
   :no-index:
.. automethod:: UsersResource.get_namespace
   :no-index:
.. automethod:: UsersResource.list_starred
   :no-index:

``GitCode.orgs``
^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.orgs
   :no-index:

.. currentmodule:: gitcode_api.resources.account

.. automethod:: OrgsResource.list_for_user
   :no-index:
.. automethod:: OrgsResource.list_authenticated
   :no-index:
.. automethod:: OrgsResource.get_member
   :no-index:
.. automethod:: OrgsResource.get
   :no-index:
.. automethod:: OrgsResource.list_repos
   :no-index:
.. automethod:: OrgsResource.create_repo
   :no-index:
.. automethod:: OrgsResource.get_enterprise_member
   :no-index:
.. automethod:: OrgsResource.get_membership
   :no-index:
.. automethod:: OrgsResource.list_members
   :no-index:
.. automethod:: OrgsResource.list_enterprise_members
   :no-index:
.. automethod:: OrgsResource.remove_member
   :no-index:
.. automethod:: OrgsResource.list_followers
   :no-index:
.. automethod:: OrgsResource.get_issue_extend_settings
   :no-index:
.. automethod:: OrgsResource.invite_member
   :no-index:
.. automethod:: OrgsResource.update_enterprise_member
   :no-index:
.. automethod:: OrgsResource.update
   :no-index:
.. automethod:: OrgsResource.leave
   :no-index:

``GitCode.search``
^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.search
   :no-index:

.. currentmodule:: gitcode_api.resources.account

.. automethod:: SearchResource.users
   :no-index:
.. automethod:: SearchResource.issues
   :no-index:
.. automethod:: SearchResource.repositories
   :no-index:

``GitCode.oauth``
^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.oauth
   :no-index:

.. currentmodule:: gitcode_api.resources.account

.. automethod:: OAuthResource.build_authorize_url
   :no-index:
.. automethod:: OAuthResource.exchange_token
   :no-index:
.. automethod:: OAuthResource.refresh_token
   :no-index:

Miscellaneous repository resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``GitCode.releases``
^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.releases
   :no-index:

.. currentmodule:: gitcode_api.resources.misc

.. automethod:: ReleasesResource.update
   :no-index:
.. automethod:: ReleasesResource.get_by_tag
   :no-index:
.. automethod:: ReleasesResource.list
   :no-index:

``GitCode.tags``
^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.tags
   :no-index:

.. currentmodule:: gitcode_api.resources.misc

.. automethod:: TagsResource.list
   :no-index:
.. automethod:: TagsResource.create
   :no-index:
.. automethod:: TagsResource.list_protected
   :no-index:
.. automethod:: TagsResource.delete_protected
   :no-index:
.. automethod:: TagsResource.get_protected
   :no-index:
.. automethod:: TagsResource.create_protected
   :no-index:
.. automethod:: TagsResource.update_protected
   :no-index:

``GitCode.webhooks``
^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: GitCode.webhooks
   :no-index:

.. currentmodule:: gitcode_api.resources.misc

.. automethod:: WebhooksResource.list
   :no-index:
.. automethod:: WebhooksResource.create
   :no-index:
.. automethod:: WebhooksResource.get
   :no-index:
.. automethod:: WebhooksResource.update
   :no-index:
.. automethod:: WebhooksResource.delete
   :no-index:
.. automethod:: WebhooksResource.test
   :no-index:

Asynchronous client
-------------------

.. currentmodule:: gitcode_api._client

.. autoclass:: AsyncGitCode
   :members: close
   :inherited-members:
   :no-index:

Repository resources
~~~~~~~~~~~~~~~~~~~~

``AsyncGitCode.repos``
^^^^^^^^^^^^^^^^^^^^^^

.. autoattribute:: AsyncGitCode.repos
   :no-index:

.. currentmodule:: gitcode_api.resources.repositories

.. automethod:: AsyncReposResource.get
   :no-index:
.. automethod:: AsyncReposResource.list_user
   :no-index:
.. automethod:: AsyncReposResource.list_for_owner
   :no-index:
.. automethod:: AsyncReposResource.create_personal
   :no-index:
.. automethod:: AsyncReposResource.create_for_org
   :no-index:
.. automethod:: AsyncReposResource.update
   :no-index:
.. automethod:: AsyncReposResource.delete
   :no-index:
.. automethod:: AsyncReposResource.fork
   :no-index:
.. automethod:: AsyncReposResource.list_forks
   :no-index:
.. automethod:: AsyncReposResource.list_contributors
   :no-index:
.. automethod:: AsyncReposResource.list_languages
   :no-index:
.. automethod:: AsyncReposResource.list_stargazers
   :no-index:
.. automethod:: AsyncReposResource.list_subscribers
   :no-index:
.. automethod:: AsyncReposResource.update_module_settings
   :no-index:
.. automethod:: AsyncReposResource.update_reviewer_settings
   :no-index:
.. automethod:: AsyncReposResource.set_org_repo_status
   :no-index:
.. automethod:: AsyncReposResource.transfer_to_org
   :no-index:
.. automethod:: AsyncReposResource.get_transition
   :no-index:
.. automethod:: AsyncReposResource.update_transition
   :no-index:
.. automethod:: AsyncReposResource.update_push_config
   :no-index:
.. automethod:: AsyncReposResource.get_push_config
   :no-index:
.. automethod:: AsyncReposResource.upload_image
   :no-index:
.. automethod:: AsyncReposResource.upload_file
   :no-index:
.. automethod:: AsyncReposResource.update_repo_settings
   :no-index:
.. automethod:: AsyncReposResource.get_repo_settings
   :no-index:
.. automethod:: AsyncReposResource.get_pull_request_settings
   :no-index:
.. automethod:: AsyncReposResource.update_pull_request_settings
   :no-index:
.. automethod:: AsyncReposResource.set_member_role
   :no-index:
.. automethod:: AsyncReposResource.transfer
   :no-index:
.. automethod:: AsyncReposResource.list_customized_roles
   :no-index:
.. automethod:: AsyncReposResource.get_download_statistics
   :no-index:
.. automethod:: AsyncReposResource.get_contributor_statistics
   :no-index:
.. automethod:: AsyncReposResource.list_events
   :no-index:

``AsyncGitCode.contents``
^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.contents
   :no-index:

.. currentmodule:: gitcode_api.resources.repositories

.. automethod:: AsyncRepoContentsResource.get
   :no-index:
.. automethod:: AsyncRepoContentsResource.create
   :no-index:
.. automethod:: AsyncRepoContentsResource.update
   :no-index:
.. automethod:: AsyncRepoContentsResource.delete
   :no-index:
.. automethod:: AsyncRepoContentsResource.list_paths
   :no-index:
.. automethod:: AsyncRepoContentsResource.get_tree
   :no-index:
.. automethod:: AsyncRepoContentsResource.get_blob
   :no-index:
.. automethod:: AsyncRepoContentsResource.get_raw
   :no-index:

``AsyncGitCode.branches``
^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.branches
   :no-index:

.. currentmodule:: gitcode_api.resources.repositories

.. automethod:: AsyncBranchesResource.list
   :no-index:
.. automethod:: AsyncBranchesResource.get
   :no-index:
.. automethod:: AsyncBranchesResource.create
   :no-index:
.. automethod:: AsyncBranchesResource.list_protected
   :no-index:

``AsyncGitCode.commits``
^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.commits
   :no-index:

.. currentmodule:: gitcode_api.resources.repositories

.. automethod:: AsyncCommitsResource.list
   :no-index:
.. automethod:: AsyncCommitsResource.get
   :no-index:
.. automethod:: AsyncCommitsResource.compare
   :no-index:
.. automethod:: AsyncCommitsResource.list_comments
   :no-index:
.. automethod:: AsyncCommitsResource.get_comment
   :no-index:
.. automethod:: AsyncCommitsResource.create_comment
   :no-index:
.. automethod:: AsyncCommitsResource.update_comment
   :no-index:
.. automethod:: AsyncCommitsResource.delete_comment
   :no-index:

Collaboration resources
~~~~~~~~~~~~~~~~~~~~~~~

``AsyncGitCode.issues``
^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.issues
   :no-index:

.. currentmodule:: gitcode_api.resources.collaboration

.. automethod:: AsyncIssuesResource.list
   :no-index:
.. automethod:: AsyncIssuesResource.get
   :no-index:
.. automethod:: AsyncIssuesResource.create
   :no-index:
.. automethod:: AsyncIssuesResource.update
   :no-index:
.. automethod:: AsyncIssuesResource.list_comments
   :no-index:
.. automethod:: AsyncIssuesResource.create_comment
   :no-index:
.. automethod:: AsyncIssuesResource.get_comment
   :no-index:
.. automethod:: AsyncIssuesResource.update_comment
   :no-index:
.. automethod:: AsyncIssuesResource.delete_comment
   :no-index:
.. automethod:: AsyncIssuesResource.list_pull_requests
   :no-index:
.. automethod:: AsyncIssuesResource.add_labels
   :no-index:
.. automethod:: AsyncIssuesResource.remove_label
   :no-index:
.. automethod:: AsyncIssuesResource.list_enterprise
   :no-index:
.. automethod:: AsyncIssuesResource.list_user
   :no-index:
.. automethod:: AsyncIssuesResource.list_org
   :no-index:
.. automethod:: AsyncIssuesResource.get_enterprise_issue
   :no-index:
.. automethod:: AsyncIssuesResource.list_enterprise_comments
   :no-index:
.. automethod:: AsyncIssuesResource.list_enterprise_labels
   :no-index:
.. automethod:: AsyncIssuesResource.list_operation_logs
   :no-index:

``AsyncGitCode.pulls``
^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.pulls
   :no-index:

.. currentmodule:: gitcode_api.resources.collaboration

.. automethod:: AsyncPullsResource.list
   :no-index:
.. automethod:: AsyncPullsResource.get
   :no-index:
.. automethod:: AsyncPullsResource.create
   :no-index:
.. automethod:: AsyncPullsResource.update
   :no-index:
.. automethod:: AsyncPullsResource.merge
   :no-index:
.. automethod:: AsyncPullsResource.get_merge_status
   :no-index:
.. automethod:: AsyncPullsResource.list_commits
   :no-index:
.. automethod:: AsyncPullsResource.list_files
   :no-index:
.. automethod:: AsyncPullsResource.list_comments
   :no-index:
.. automethod:: AsyncPullsResource.create_comment
   :no-index:
.. automethod:: AsyncPullsResource.get_comment
   :no-index:
.. automethod:: AsyncPullsResource.update_comment
   :no-index:
.. automethod:: AsyncPullsResource.delete_comment
   :no-index:
.. automethod:: AsyncPullsResource.list_labels
   :no-index:
.. automethod:: AsyncPullsResource.add_labels
   :no-index:
.. automethod:: AsyncPullsResource.replace_labels
   :no-index:
.. automethod:: AsyncPullsResource.remove_label
   :no-index:
.. automethod:: AsyncPullsResource.request_review
   :no-index:
.. automethod:: AsyncPullsResource.list_operation_logs
   :no-index:
.. automethod:: AsyncPullsResource.request_test
   :no-index:
.. automethod:: AsyncPullsResource.update_testers
   :no-index:
.. automethod:: AsyncPullsResource.add_testers
   :no-index:
.. automethod:: AsyncPullsResource.update_assignees
   :no-index:
.. automethod:: AsyncPullsResource.add_assignees
   :no-index:
.. automethod:: AsyncPullsResource.remove_assignees
   :no-index:
.. automethod:: AsyncPullsResource.list_issues
   :no-index:
.. automethod:: AsyncPullsResource.list_enterprise
   :no-index:
.. automethod:: AsyncPullsResource.list_org
   :no-index:
.. automethod:: AsyncPullsResource.list_issue_pull_requests
   :no-index:

``AsyncGitCode.labels``
^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.labels
   :no-index:

.. currentmodule:: gitcode_api.resources.collaboration

.. automethod:: AsyncLabelsResource.list
   :no-index:
.. automethod:: AsyncLabelsResource.create
   :no-index:
.. automethod:: AsyncLabelsResource.update
   :no-index:
.. automethod:: AsyncLabelsResource.delete
   :no-index:
.. automethod:: AsyncLabelsResource.clear_issue_labels
   :no-index:
.. automethod:: AsyncLabelsResource.replace_issue_labels
   :no-index:
.. automethod:: AsyncLabelsResource.list_enterprise
   :no-index:

``AsyncGitCode.milestones``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.milestones
   :no-index:

.. currentmodule:: gitcode_api.resources.collaboration

.. automethod:: AsyncMilestonesResource.list
   :no-index:
.. automethod:: AsyncMilestonesResource.get
   :no-index:
.. automethod:: AsyncMilestonesResource.create
   :no-index:
.. automethod:: AsyncMilestonesResource.update
   :no-index:
.. automethod:: AsyncMilestonesResource.delete
   :no-index:

``AsyncGitCode.members``
^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.members
   :no-index:

.. currentmodule:: gitcode_api.resources.collaboration

.. automethod:: AsyncMembersResource.add_or_update
   :no-index:
.. automethod:: AsyncMembersResource.remove
   :no-index:
.. automethod:: AsyncMembersResource.list
   :no-index:
.. automethod:: AsyncMembersResource.get
   :no-index:
.. automethod:: AsyncMembersResource.get_permission
   :no-index:

Account and discovery resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``AsyncGitCode.users``
^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.users
   :no-index:

.. currentmodule:: gitcode_api.resources.account

.. automethod:: AsyncUsersResource.get
   :no-index:
.. automethod:: AsyncUsersResource.me
   :no-index:
.. automethod:: AsyncUsersResource.list_emails
   :no-index:
.. automethod:: AsyncUsersResource.list_events
   :no-index:
.. automethod:: AsyncUsersResource.list_repos
   :no-index:
.. automethod:: AsyncUsersResource.create_key
   :no-index:
.. automethod:: AsyncUsersResource.list_keys
   :no-index:
.. automethod:: AsyncUsersResource.delete_key
   :no-index:
.. automethod:: AsyncUsersResource.get_key
   :no-index:
.. automethod:: AsyncUsersResource.get_namespace
   :no-index:
.. automethod:: AsyncUsersResource.list_starred
   :no-index:

``AsyncGitCode.orgs``
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.orgs
   :no-index:

.. currentmodule:: gitcode_api.resources.account

.. automethod:: AsyncOrgsResource.list_for_user
   :no-index:
.. automethod:: AsyncOrgsResource.list_authenticated
   :no-index:
.. automethod:: AsyncOrgsResource.get_member
   :no-index:
.. automethod:: AsyncOrgsResource.get
   :no-index:
.. automethod:: AsyncOrgsResource.list_repos
   :no-index:
.. automethod:: AsyncOrgsResource.create_repo
   :no-index:
.. automethod:: AsyncOrgsResource.get_enterprise_member
   :no-index:
.. automethod:: AsyncOrgsResource.get_membership
   :no-index:
.. automethod:: AsyncOrgsResource.list_members
   :no-index:
.. automethod:: AsyncOrgsResource.list_enterprise_members
   :no-index:
.. automethod:: AsyncOrgsResource.remove_member
   :no-index:
.. automethod:: AsyncOrgsResource.list_followers
   :no-index:
.. automethod:: AsyncOrgsResource.get_issue_extend_settings
   :no-index:
.. automethod:: AsyncOrgsResource.invite_member
   :no-index:
.. automethod:: AsyncOrgsResource.update_enterprise_member
   :no-index:
.. automethod:: AsyncOrgsResource.update
   :no-index:
.. automethod:: AsyncOrgsResource.leave
   :no-index:

``AsyncGitCode.search``
^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.search
   :no-index:

.. currentmodule:: gitcode_api.resources.account

.. automethod:: AsyncSearchResource.users
   :no-index:
.. automethod:: AsyncSearchResource.issues
   :no-index:
.. automethod:: AsyncSearchResource.repositories
   :no-index:

``AsyncGitCode.oauth``
^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.oauth
   :no-index:

.. currentmodule:: gitcode_api.resources.account

.. automethod:: AsyncOAuthResource.build_authorize_url
   :no-index:
.. automethod:: AsyncOAuthResource.exchange_token
   :no-index:
.. automethod:: AsyncOAuthResource.refresh_token
   :no-index:

Miscellaneous repository resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``AsyncGitCode.releases``
^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.releases
   :no-index:

.. currentmodule:: gitcode_api.resources.misc

.. automethod:: AsyncReleasesResource.update
   :no-index:
.. automethod:: AsyncReleasesResource.get_by_tag
   :no-index:
.. automethod:: AsyncReleasesResource.list
   :no-index:

``AsyncGitCode.tags``
^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.tags
   :no-index:

.. currentmodule:: gitcode_api.resources.misc

.. automethod:: AsyncTagsResource.list
   :no-index:
.. automethod:: AsyncTagsResource.create
   :no-index:
.. automethod:: AsyncTagsResource.list_protected
   :no-index:
.. automethod:: AsyncTagsResource.delete_protected
   :no-index:
.. automethod:: AsyncTagsResource.get_protected
   :no-index:
.. automethod:: AsyncTagsResource.create_protected
   :no-index:
.. automethod:: AsyncTagsResource.update_protected
   :no-index:

``AsyncGitCode.webhooks``
^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: gitcode_api._client

.. autoattribute:: AsyncGitCode.webhooks
   :no-index:

.. currentmodule:: gitcode_api.resources.misc

.. automethod:: AsyncWebhooksResource.list
   :no-index:
.. automethod:: AsyncWebhooksResource.create
   :no-index:
.. automethod:: AsyncWebhooksResource.get
   :no-index:
.. automethod:: AsyncWebhooksResource.update
   :no-index:
.. automethod:: AsyncWebhooksResource.delete
   :no-index:
.. automethod:: AsyncWebhooksResource.test
   :no-index:
