# Git Tools

This project now includes a small utility module for working with the
repository's history. The command:

```
zero-liftsim dev --analyze-docs
```

walks through every Markdown file in the ``docs`` directory and appends
a summary section to the end of each file. The section records the most
recent commit hash and the commit date converted to the ``US/Denver``
time zone. This helps track when documentation was last updated.
