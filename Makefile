# Makefile — commands for using dome2
#
# Mainly tool targets: what a user of the app runs. Development commands
# (sync, tests, ruff) run through `uv` directly (see CLAUDE.md); add targets
# for them only when something depends on them.

.PHONY: help

.DEFAULT_GOAL := help

help: ## List targets
	@awk 'BEGIN {FS = ":.*## "} \
		/^[a-zA-Z_-]+:.*## / {printf "  %-13s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Add user-facing targets here as features land, each with a `## description`:
#   validate: ## Check a card
#   	uv run <app> check

.PHONY: clone pull status-repos

clone: ## git clone every registered DOME package that is missing
	python3 -m dome2.stack_ops clone --registry stack/packages.yaml --src ..

pull: ## git pull every DOME package in the registry
	python3 -m dome2.stack_ops pull --registry stack/packages.yaml --src ..

status-repos: ## Fetch, then print CLEAN or DIRTY for each DOME repo
	@python3 -m dome2.stack_ops status --registry stack/packages.yaml --src ..
