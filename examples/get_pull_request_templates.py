"""List GitCode pull request templates and print one template body.

Configuration is read from ``examples/.env`` (see ``examples/.env.example``).
Templates are discovered on the **default branch**; resolution is described
under *Issue and pull request templates* in ``docs/sdk/client_api.rst``.
"""

from _shared import load_config

from gitcode_api import GitCode


def main() -> None:
    config = load_config()
    with GitCode(api_key=config.api_key, owner=config.username, repo=config.repo) as client:
        templates = client.pulls.list_templates()
        print(f"repository: {config.username}/{config.repo}")
        print(f"active pull request templates (after SDK resolution): {len(templates)}")
        print("")
        for row in templates:
            print(f"- {row.path} (sha={row.sha}) from {row.template_owner}/{row.template_repo}")
        if not templates:
            return
        first = templates[0]
        body = client.pulls.get_template(
            path=first.path,
            owner=first.template_owner,
            repo=first.template_repo,
        )
        print("")
        print("first template body:")
        print(body)


if __name__ == "__main__":
    main()
