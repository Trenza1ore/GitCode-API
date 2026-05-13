``IssuesResource.list_templates``, ``IssuesResource.get_template``,
``PullsResource.list_templates``, and ``PullsResource.get_template`` (and the
``Async*`` equivalents) help you read GitCode **active** templates from the
repository default branch via the Contents and Raw APIs.

``list_templates`` returns :class:`~gitcode_api._models.RepositoryGitCodeTemplate`
rows: each row includes ``path``, ``sha``, and the ``template_owner`` /
``template_repo`` of the repository where that file was found. ``get_template``
returns the decoded file body as ``str``; pass ``owner=`` and ``repo=`` from
the row when they differ from the client's default context (for example when
the template was resolved from another repository).

**Resolution (first source with any matching template wins).** The SDK builds
an ordered list of ``(owner, repo)`` pairs, then walks ``GET .../contents/.gitcode``
for each until it finds paths that match the template naming rules:

1. The client's default repository (``owner`` / ``repo`` from the call or client).
2. The owner's dedicated template repository: ``(owner, ".gitcode")``.
3. For **every** candidate in that list, ``GET /repos/{owner}/{repo}`` is used;
   when ``fork`` is true, the parent's ``full_name`` is split into
   ``(parent_owner, parent_repo)`` and both ``(parent_owner, parent_repo)`` and
   ``(parent_owner, ".gitcode")`` are appended if not already present. New pairs
   are processed the same way (so a forked ``owner/.gitcode`` repo can still pull
   in its upstream). The walk stops at a bounded number of candidates.

**Path filters.** Issue templates match repository-relative paths under
``.gitcode/`` whose names start with ``ISSUE_TEMPLATE`` (case-insensitive) and
end with ``.md``, ``.markdown``, ``.yml``, or ``.yaml``. Pull request templates
use the ``PULL_REQUEST_TEMPLATE`` prefix with the same extension set.

Runnable examples: ``examples/get_issue_templates.py`` and
``examples/get_pull_request_templates.py``.
