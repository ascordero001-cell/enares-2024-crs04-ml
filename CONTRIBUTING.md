# Contributing

## Workflow

1. Start from an approved issue.
2. Create or use a feature branch.
3. Make a small, focused change.
4. Run the relevant tests.
5. Review the Git diff for data, secrets and unintended outputs.
6. Commit with a descriptive message.
7. Push the branch and open a pull request.
8. Obtain review before merging.

## Safety

Never commit:

- ENARES microdata;
- `.sav`, `.csv`, `.parquet` or spreadsheet data;
- `.env` files;
- credentials, tokens or service-account keys;
- private Google Drive identifiers;
- outputs containing individual records.

Tests must use synthetic data or approved aggregated results.

## Methodological changes

Changes to indicators, universes, denominators, recodes, skip logic, weights or
survey design require methodological review.

A passing technical test does not by itself approve a methodological change.

## Local validation

Activate the project environment and run:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest -q
```

All tests must pass before opening a pull request.

## Commit examples

```text
chore(config): add environment-independent configuration
test(config): validate project configuration loader
feat(dataform): add CRS04 raw sources and assertions
docs(stage03): document migration evidence
```