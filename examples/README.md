# Examples

All example scripts read parameters from `examples/.env` via `python-dotenv`.

## Configure

Fill in:

- `GITCODE_ACCESS_TOKEN`
- `GITCODE_OWNER`
- `GITCODE_REPO`
- `GITCODE_USERNAME`

Optional:

- `GITCODE_PULL_STATE`
- `GITCODE_PER_PAGE`

## Run

```bash
uv run python examples/get_current_user.py
uv run python examples/get_repository_overview.py
uv run python examples/list_pull_requests.py
uv run python examples/async_list_branches.py
```
