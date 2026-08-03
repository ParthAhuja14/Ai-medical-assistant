# Contributing

Thanks for taking a look at this project! It started as a portfolio piece,
but contributions, bug reports, and suggestions are welcome.

## Getting set up

Follow the [Getting started (local development)](README.md#getting-started-local-development)
section of the README to get the backend and frontend running.

## Running tests

```bash
cd backend
pytest tests/ -v
```

Please add or update tests for any behavioral change to the diagnosis
pipeline, auth, or specialist search endpoints.

## Making changes

1. Fork the repo and create a branch off `main`.
2. Make your changes. Keep commits focused and messages descriptive.
3. Run the backend test suite and the frontend build (`npm run build`)
   locally before opening a PR — CI will run both automatically, but it's
   faster to catch issues locally.
4. Open a pull request describing what changed and why.

## Reporting issues

Please include:
- What you expected to happen vs. what actually happened
- Steps to reproduce
- Whether you're running locally or via Docker
- Any relevant error output from the backend logs

## A note on scope

This project deliberately keeps "medicine suggestions" to general categories
only, never specific drugs or dosages, and always frames predictions as
possibilities rather than diagnoses (see [Safety & Scope](README.md#safety--scope)
in the README). Please keep this framing intact in any contribution that
touches the diagnosis output or explanation layer.
