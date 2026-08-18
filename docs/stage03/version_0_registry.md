# Version 0 Registry

## Baseline

- Git tag: `stage03-v0-baseline`
- Commit: `2a381dec941fefe3159fa4aad02c8fd4f4b6a228`
- Local artifacts: 16 notebooks
- Execution environment: Google Colab
- Execution status: all notebooks executed successfully
- Automated validation: PASS
- Supervisor approval: pending confirmation

## Evidence

| Artifact | Location | Status | Notes |
|---|---|---|---|
| V0 notebooks | Git repository | Executed | All 16 ran successfully in Google Colab |
| Notebook hash inventory | `docs/stage03/v0_hash_inventory.csv` | Created | SHA-256 recorded |
| PASS Markdown report | Restricted Google Drive | Available externally | Generated after successful validation |
| Canonical SPSS syntax | External location | Location to confirm | Not stored in the local repository |
| BigQuery tables | Google Cloud | Existing | Inventory required during Stage 03 migration |

## PASS report limitation

The PASS Markdown report currently exists only in Google Drive. Its exact
filename, Drive folder, generation date and source notebook should be recorded.
It has not yet been copied into the repository or Cloud Storage.

Before copying it, confirm that it contains no microdata, credentials, personal
paths or confidential identifiers.