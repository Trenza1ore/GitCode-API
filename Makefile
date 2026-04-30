.PHONY: docs docs-clean format

SPHINX_BUILD ?= uv run --group docs sphinx-build
DOCS_SOURCE_DIR := docs
DOCS_BUILD_DIR := $(DOCS_SOURCE_DIR)/_build/html

docs: docs-clean
	$(SPHINX_BUILD) -b html $(DOCS_SOURCE_DIR) $(DOCS_BUILD_DIR)

docs-clean:
	rm -rf $(DOCS_SOURCE_DIR)/_build
	rm -rf $(DOCS_SOURCE_DIR)/sdk/generated

format:
	uv run ruff check --fix || true
	uv run ruff check --select I --fix || true
	uv run ruff format || true

test:
	uv pip install .
	uv run pytest

release:
	@$(if $(strip $(VERSION)),:,$(error VERSION is required, e.g. make release VERSION=1.2.3))
	printf '%s\n' "$(VERSION)" > gitcode_api/version.txt
	sed -i '' 's/^version = ".*"/version = "$(VERSION)"/' pyproject.toml
	uv lock
	git add pyproject.toml uv.lock gitcode_api/version.txt
	git commit -m "chore: bump version to $(VERSION)"
	git tag -a "$(VERSION)" -m "$(VERSION)"
	git push --tags
	git push
