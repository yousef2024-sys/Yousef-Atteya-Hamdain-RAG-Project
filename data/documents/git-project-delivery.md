# Shipping a Graduation Project

## README as a runbook

A strong README lets a stranger clone the repository and run the project without guessing. Include the architecture, setup commands, environment variables, data preparation, API examples, evaluation results, and screenshots. Separate safe example configuration from secrets and never commit a real environment file.

## Reproducible artifacts

Persist the processed chunks, embedding configuration, and vector index so the backend can start without rebuilding on every request. Pin important dependencies, keep generated artifacts small, and document how to regenerate them from the notebook. A clean separation between raw data, processed data, and runtime code makes handoff safer.

## Demo flow

A useful demo shows the complete flow: ask a real question, display the grounded answer, open the cited source, and explain one limitation or failure case. Demonstrate health checks and an invalid input response as well as the happy path. The presentation should make the retrieval and citation steps visible.
