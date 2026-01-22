## 2024-07-16 - N+1 Query in `classement` Endpoint

**Learning:** The `classement` action in `concours.views.SerieViewSet` was fetching all `Note` objects into memory and performing calculations in Python, leading to a classic N+1 query problem. This is inefficient and scales poorly.

**Action:** Refactored the query to use Django ORM's `annotate`, `Sum`, and `F` expressions to perform the aggregation directly in the database. This significantly improves performance and reduces memory usage. Also discovered a `FieldError` when dividing a `DecimalField` by a `FloatField` with the SQLite backend, which was resolved by wrapping the division in an `ExpressionWrapper` and setting `output_field=FloatField()`.

## 2024-07-16 - Repository Hygiene

**Learning:** Committing auto-generated files like `__pycache__` directories and `.log` files pollutes the repository and can cause platform-specific issues. The `.gitignore` file was correctly configured, but these files had already been staged.

**Action:** Used `git rm -r --cached` to remove the unwanted files from the Git index. In the future, I will always check the staging area for auto-generated files before committing.
