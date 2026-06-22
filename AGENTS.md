# Agent Rules

1. Do not create manual migrations. Use the project's migration tooling to generate migrations from model metadata instead.
2. Do not add compatibility layers for old code unless explicitly asked.
3. Do not run `poetry install`.
4. Do not run `poetry lock`.
5. Do only what the user explicitly requests. If there is a problem, report it to the user instead of making unrequested changes.
6. Do not add or run tests unless the user explicitly requests them.
