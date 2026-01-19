# BOLT'S JOURNAL - CRITICAL LEARNINGS ONLY

This journal is for CRITICAL learnings that will help Bolt avoid mistakes or make better decisions.

- A performance bottleneck specific to this codebase's architecture
- An optimization that surprisingly DIDN'T work (and why)
- A rejected change with a valuable lesson
- A codebase-specific performance pattern or anti-pattern
- A surprising edge case in how this app handles performance

## 2024-07-25 - Clean Commits and Correct Imports

**Learning:** Committing auto-generated files like `.pyc` and `django.log` is a serious repository hygiene issue. It bloats the repository and can mask real changes. Additionally, a `NameError` was introduced by incorrectly referencing an imported object.

**Action:** Always check the git status before committing to ensure no auto-generated files are staged. Double-check imports and references to avoid `NameError` bugs.
