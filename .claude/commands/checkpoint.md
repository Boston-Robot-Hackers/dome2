Run a full checkpoint in this order:

- Run all tests
- Run `ruff check . && ruff format --check .`. Before fixing any violation, ask
  the user for confirmation, and state whether the fix is consistent with or at
  odds with @.claude/style_guide.md.
- Update current.md's `## Open` section with your latest context; move any
  newly-completed items out to `02-doc/history.md` instead of appending to
  current.md
- Review changed code against judgment rules in @.claude/style_guide.md (design, error handling, naming semantics)
- Update any changed literate md files
- Create a commit (no need for a pull request)
- Push to github