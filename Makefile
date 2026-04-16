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
