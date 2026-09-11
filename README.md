# ENARES 2024 CRS04 — Reproducible Pipeline and Population Surveillance

### Reproducible survey engineering and privacy-safe population surveillance for adolescents in Peru

[![CI](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/workflows/ci.yml/badge.svg)](https://github.com/ascordero001-cell/enares-2024-crs04-ml/actions/workflows/ci.yml)
![Stage 03](https://img.shields.io/badge/Stage%2003-PASS%20in%20shadow-success)
![Stage 04](https://img.shields.io/badge/Stage%2004-LOCAL%20SHADOW-yellow)
![Privacy](https://img.shields.io/badge/data-no%20microdata-blue)

A reproducible, traceable and auditable pipeline that processes ENARES 2024
Questionnaire 4 — adolescents aged 12–17 — and develops a population-level
surveillance application for violence against children and adolescents in Peru.

Built by **Ana Silvia Cordero Ricaldi**, BSc Computer Science and Artificial
Intelligence student at the University of Sussex, as an **Independent
Undergraduate Research Apprenticeship** in data engineering applied to official
institutional microdata.

> **Publication status:** V0 remains the official version. Release
> `stage03-v0.5-cloud-full` passed its technical, reproducibility and
> methodological-supervision gates and completed handoff to Stage 04, but
> remains `SHADOW — NOT PUBLISHED`. Stage 04 is authorised only as
> `LOCAL SHADOW ONLY`; cloud, publication and cutover remain unauthorised.

![Synthetic Stage 04 demonstration showing candidate, reference and suppressed states](docs/stage04/evidence/sprint042_corte2_states.png)

*Synthetic demonstration — SHADOW, NOT PUBLISHED. It contains no respondent-level data.*

## What this project delivers

- Reproducible ingestion and preservation of official institutional survey sources, with
  manifests and hashes frozen at every stage.
- Survey-weighted indicators for analytical modules 3.1–3.6 — **516 indicators**
  across **3,014 statistical rows**, validated against SPSS with **3,013/3,014
  exact parity (99.97%)**.
- Automated tests, CI (`pytest` and Dataform compilation), Architecture Decision
  Records, and independent methodological review before promotion.
- A privacy-safe Streamlit population-surveillance application, currently in
  controlled local shadow development for Stage 04.
- No microdata or individual respondent records in the public repository —
  code, contracts, synthetic fixtures and aggregated evidence only.

## Current status

| Stage | Scope | Status |
|---|---|---|
| Stage 01 | Ingestion and preservation of official sources | ✅ Approved |
| Stage 02 | Storage and initial validation in BigQuery | ✅ Approved |
| Stage 03 | Cleaning, indicators 3.1–3.6, sampling design and cloud migration | ✅ `PASS` in shadow |
| Stage 04 | Privacy-safe population-surveillance application | 🟡 `LOCAL SHADOW ONLY` — Corte 2 under review |
| Stage 05 | Evaluation, monitoring and post-publication decisions | ⏳ Pending |

**Version meaning:** `V0` is the historical implementation and official version.
`V0.5` is the component-validated cloud migration and remains
`SHADOW — NOT PUBLISHED`. `V1` is a future promoted version, pending a separate
cutover decision. A technical or methodological `PASS` does not itself authorise
institutional publication.

## Explore the project

| I want to… | Go to |
|---|---|
| Understand the Stage 04 architecture | [Architecture blueprint](CRS04_STAGE04_HOJA_ARQUITECTONICA_APP_VIGILANCIA.md) |
| Review full Stage 03 closure evidence | [Closure report](docs/stage03/stage3_closure_report.md) · [Stage 03 PASS](docs/stage03/stage3_pass.md) · [Data contract](docs/stage03/stage03_data_contract.md) |
| Follow Stage 04 development | [Governing document](CRS04_STAGE04_CORREGIDO_VER6_NUEVA_METODOLOGIA.md) · [Issue map](docs/stage04/issue_map.md) · [Umbrella issue #43](https://github.com/ascordero001-cell/enares-2024-crs04-ml/issues/43) |
| Inspect Corte 2 evidence | [Coverage record](docs/stage04/sprint042_corte2_module_coverage.md) · [Module matrix](docs/stage04/module_coverage_matrix.md) · [HCI evidence](docs/stage04/hci_accessibility_corte2.md) |
| Understand an engineering decision | [Architecture Decision Records](docs/adr/) |
| Contribute | [Contribution guide](CONTRIBUTING.md) |

## Architecture at a glance

```text
Official institutional / SPSS sources
  -> Stage 01: ingestion, manifests and hashes
  -> Stage 02: raw layer
  -> Stage 03: cleaned layer
  -> Stage 03: analytical modules 3.1–3.6
  -> reporting_crs04_survey_input_v0_5
  -> Dataform validations + SPSS-R regression
  -> human decision and shadow release
  -> Stage 04: validated aggregates
  -> local contracts and repository boundary
  -> row validation and privacy controls
  -> local Streamlit application
```

The application consumes only authorised aggregated results. It never queries
respondent-level microdata or supports searches for individual children or
adolescents. The future BigQuery published view and Cloud Run deployment remain
behind a separate cloud gate; no cloud resource is authorised in the current phase.

## Analytical modules

| Module | Population surveillance content |
|---|---|
| 3.1 | Characteristics, perceptions and social norms |
| 3.2 | Psychological and physical violence in the household |
| 3.3 | Psychological and physical violence at school |
| 3.4 | Sexual violence |
| 3.5 | Polyvictimisation and accumulation of violence |
| 3.6 | Help-seeking and receipt of support |

The official block **3.6 corresponds to help-seeking**. Historical `3.7` naming
is preserved only in traceability documentation and is never presented as current.

## Reproducibility and collaboration

Two guarantees are kept separate: **reproducible** means that the same inputs
produce the same outputs; **collaborative** means another contributor can extend
the work without silently breaking its contracts.

**Reproducible — same inputs, same outputs**

- **Source integrity.** Every raw survey file is hashed on ingestion in Stage 01,
  and the V0 baseline is frozen under the `stage03-v0-baseline` tag.
- **Validated parity.** Release `stage03-v0.5-cloud-full` matched SPSS on 3,013 of
  3,014 statistical rows. The documented `VS_12M` exception uses the full
  18,807-adolescent denominator required by the canonical rule.
- **Versioned contracts.** The reporting contract is pinned at 18,807 rows and
  737 explicit columns; an indicator change requires a contract change rather
  than an unrecorded query edit.

**Collaborative — someone else can pick this up**

- **Traceable decisions.** [Architecture Decision Records](docs/adr/) capture why
  universes, denominators, recodes and sampling-design choices were made.
- **Gated changes.** Work follows issue → branch → small commits → pull request →
  CI → independent review → merge.
- **Tested before merge.** `.github/workflows/ci.yml` runs blocking `pytest` and
  Dataform compilation on a clean runner, plus informative notebook lint.

## Privacy and responsible use

This public repository contains code, contracts, synthetic fixtures and
aggregated evidence only. It does not contain `.sav` files, `.zip`/`.xlsx`
exports with microdata, respondent-level rows, personal identifiers,
credentials, tokens, `.env` files, service-account keys or unsanitised Drive
identifiers. Original data and restricted outputs remain in authorised private
locations. The surveillance application must never support searches for
individual children or adolescents.

## Repository map

```text
enares-2024-crs04-ml/
├── .github/workflows/       # Continuous integration
├── app/                     # Local Streamlit application
├── configs/                 # Configuration, indicators and skip logic
├── dataform/
│   └── definitions/
│       ├── sources/         # Raw sources and V0 references
│       ├── cleaned/         # Structural integration
│       ├── analytical/      # Modules 3.1–3.6 and the full table
│       ├── assertions/      # Quality, domain and parity checks
│       ├── reporting/       # Delivery contract to Stage 04
│       └── ops/             # Lineage and validation results
├── docs/
│   ├── adr/                 # Architecture Decision Records
│   ├── stage03/             # Contracts, evidence and closure
│   └── stage04/             # Local-shadow contracts and evidence
├── notebooks/               # Reproducible Stage 01–03 notebooks
├── scripts/                 # Reproducible generators and utilities
├── src/enares/              # Modular Python source
├── tests/                   # Synthetic, contract and application tests
├── .env.example
├── CONTRIBUTING.md
├── Dockerfile
├── requirements.txt
└── requirements-dev.txt
```

## Quick start

```powershell
git clone https://github.com/ascordero001-cell/enares-2024-crs04-ml.git
cd enares-2024-crs04-ml
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Cloud authentication and deployment commands are intentionally omitted. They
require a separate gate with authorised billing and IAM owners, budget and
rollback conditions; they are never run automatically in the current phase.

## Extended documentation

- [Stage 03 PASS](docs/stage03/stage3_pass.md) · [Closure report](docs/stage03/stage3_closure_report.md) · [Data contract](docs/stage03/stage03_data_contract.md)
- [Supervisor acceptance](docs/stage03/stage03_supervisor_acceptance.md) · [Handoff to Stage 04](docs/stage03/stage04_handoff.md)
- [Known Stage 03 discrepancies](docs/stage03/known_discrepancies.md) · [Migration decisions](docs/stage03/migration_decisions.md)
- [PRE-STAGE04 gate](PRE_STAGE04.md) · [Naming conventions](NAMING_CONVENTIONS.md) · [V0 registry](CRS04_STAGE04_VERSION_0_REGISTRO.md)
- [Corte 2 reconciliation](docs/stage04/reconciliation_modules_31_36.md) · [Known Stage 04 discrepancies](docs/stage04/known_discrepancies.md)
- [Contribution guide](CONTRIBUTING.md)

## Author, supervision and disclaimer

Built and maintained by **Ana Silvia Cordero Ricaldi**, BSc Computer Science and
Artificial Intelligence, University of Sussex, as an independent undergraduate
research apprenticeship. Independent methodological supervision is registered
in the Stage 03 closure and Stage 04 gate evidence.

This repository is a technical and formative project. Neither the V0.5 release
nor the Stage 04 application constitute, by themselves, an official publication
of any institution. Institutional use requires additional review, authorisation
and governance.
