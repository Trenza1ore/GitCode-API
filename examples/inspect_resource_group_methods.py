from typing import List
from _shared import load_config

from gitcode_api import GitCode


def main() -> None:
    config = load_config()
    lines: List[str] = []
    lines.append("Resource groups expose ``.methods`` — public callables per group")
    lines.append("(tuple order is stable SDK order, not plain A–Z on the full name)")
    lines.append("")
    lines.append("Quick check: client.pulls.methods is a tuple of method names, e.g.:")
    lines.append("")

    with GitCode(api_key=config.api_key, owner=config.owner, repo=config.repo) as client:
        sample = client.pulls.methods
        sample_signature = client.pulls.method_signature("list_issues")
        lines.append(f"  client.pulls.methods[:5] == {sample[:5]!r}")
        lines.append("")
        lines.append(f"  Example signature:\n  - client.pulls.{sample_signature}")
        lines.append("")
        lines.append("All groups on this client (name + inspect.signature):")
        lines.append("")

        for attr in sorted(GitCode.__annotations__):
            group = getattr(client, attr)
            names = group.methods
            lines.append(f"client.{attr}.methods  — {len(names)} name(s)")
            for name in names:
                lines.append(f"    {name}")
            lines.append("")

    report = "\n".join(lines).rstrip() + "\n"
    print(report)


if __name__ == "__main__":
    main()
