# Python Foundations

## Functions and single responsibility

A Python function should have one clear responsibility and a name that explains the action it performs. Keep inputs explicit, return a value rather than changing unrelated global state, and document surprising behavior. Small functions are easier to test because each one has fewer paths and dependencies.

## Choosing data structures

Use a list for ordered collections, a tuple for a fixed record, a set for membership checks, and a dictionary for key-value lookup. Choosing the structure that matches the question makes code easier to read and usually improves performance. Prefer comprehensions for simple transformations, but use a loop when the logic needs multiple steps.

## Errors and validation

Validate external input at the boundary of an application and raise a specific exception when a value cannot be accepted. Catch exceptions only where the application can recover or add useful context. A broad except block that hides the original error makes debugging and reliable testing much harder.
