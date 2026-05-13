# Copyright (c) Hugo Huang. 2026.
.PHONY: docs docs-dev docs-clean format rst-table test release lint docstring amend binary mcpb

SPHINX_BUILD ?= uv run --group docs sphinx-build
DOCS_SOURCE_DIR := docs
DOCS_BUILD_ROOT := $(DOCS_SOURCE_DIR)/_build
DOCS_HTML_DIR := $(DOCS_BUILD_ROOT)/html
DOCS_EPUB_DIR := $(DOCS_BUILD_ROOT)/epub
DOCS_SINGLEHTML_DIR := $(DOCS_BUILD_ROOT)/singlehtml

# Shared doctree cache outside each builder output to avoid EPUB packager unknown-mimetype warnings.
DOCS_DOCTREES_DIR := $(DOCS_BUILD_ROOT)/doctrees

docs-dev: docs-clean rst-table
	$(SPHINX_BUILD) -d $(DOCS_DOCTREES_DIR) -b html $(DOCS_SOURCE_DIR) $(DOCS_HTML_DIR)
	@uv run python scripts/docs_rename_resource_methods.py

docs: docs-dev
	@uv run python -c 'from webbrowser import open; from pathlib import Path; open(f"file://{Path.cwd().resolve()}/docs/_build/html/index.html")' || true
	$(SPHINX_BUILD) -d $(DOCS_DOCTREES_DIR) -b epub $(DOCS_SOURCE_DIR) $(DOCS_EPUB_DIR)
	$(SPHINX_BUILD) -d $(DOCS_DOCTREES_DIR) -b singlehtml $(DOCS_SOURCE_DIR) $(DOCS_SINGLEHTML_DIR)
	@uv run python scripts/docs_rename_resource_methods.py

docs-clean:
	rm -rf $(DOCS_SOURCE_DIR)/_build
	rm -rf $(DOCS_SOURCE_DIR)/sdk/generated

format:
	uv run ruff check --fix || true
	uv run ruff check --select I --fix || true
	uv run ruff format || true

rst-table:
	uv run python scripts/fix_rst_table.py docs/**/*.rst

lint:
	uv run mypy -p gitcode_api

test:
	uv pip install .
	uv run pytest

release: badge
	@$(if $(strip $(VERSION)),:,$(error VERSION is required, e.g. make release VERSION=1.2.3))
	printf '%s\n' "$(VERSION)" > gitcode_api/version.txt
	sed -i '' 's/^version = ".*"/version = "$(VERSION)"/' pyproject.toml
	uv lock
	git add pyproject.toml uv.lock gitcode_api/version.txt README*.md
	git commit -m "chore: bump version to $(VERSION)"
	git tag -a "$(VERSION)" -m "$(VERSION)"
	git push --tags
	git push

docstring:
	@uv run pydocstyle gitcode_api/

amend:
	git commit --amend --no-edit

# One-file executable: dist/gitcode-api (macOS/Linux) or dist/gitcode-api.exe (Windows).
binary:
	uv run --group binary pyinstaller --clean --noconfirm scripts/gitcode-api.spec

# MCP Bundles (.mcpb) are zip archives containing a local MCP server (basically a MCP wheel for Claude)
mcpb:
	uv run python scripts/build_manifest.py
	mcpb pack . gitcode.mcpb
	@rm manifest.json .mcpbignore

# Mutate badge with uuid to force refresh GitCode cache
badge:
	uv run python scripts/mutate_badge.py
