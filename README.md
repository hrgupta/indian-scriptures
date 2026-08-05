# Indian Scriptures

[![CodeQL Advanced](https://github.com/hrgupta/indian-scriptures/actions/workflows/codeql.yml/badge.svg)](https://github.com/hrgupta/indian-scriptures/actions/workflows/codeql.yml) · [![Super-Linter](https://github.com/hrgupta/indian-scriptures/actions/workflows/super-linter.yml/badge.svg)](https://github.com/hrgupta/indian-scriptures/actions/workflows/super-linter.yml)

This repository contains various **_Indian scriptures_** 📜 in a structured .csv format. The files contain the verses in their original Sanskrit language and their verse number.

The [data](https://github.com/hrgupta/indian-scriptures/tree/master/data) folder contains both raw and processed data. The _raw_ data is the direct output of the scrapy spiders and the _processed_ data contains data after additional processing.

The [notebooks](https://github.com/hrgupta/indian-scriptures/tree/master/notebooks) folder contain the notebooks used to create the processed dataset.

The [scriptures](https://github.com/hrgupta/indian-scriptures/tree/master/scriptures) folder is a scrapy project which contains the scrapy spiders to scrape data from the web.

The project aims to provide Indian scriptures in a format that is suitable for text mining and natural language processing. If you would like to propose any changes, kindly send a pull request.

All the files are scraped from <https://www.upanishads.iitk.ac.in> using scrapy 🕷️ framework.

> **2026 note:** the original IITK hosts are offline. The Gita spiders now scrape the [Gita Supersite mirror](https://old.gitasupersite.in), which preserves the original site structure — the spider logic is unchanged. The Upanishad spider still points at `upanishads.iitk.ac.in` (offline); its data is retained in `data/raw/upanishads/`.

## Set up

Requires [uv](https://docs.astral.sh/uv/) (or any Python 3.14 interpreter):

```bash
uv venv --python 3.14 venv
uv pip install -r requirements.txt
```

## Scrape the scriptures (spiders)

From the repository root:

```bash
cd scriptures/spiders
../../venv/bin/python bhagavadgita_spider.py   # Śrīmad Bhagavad Gītā → data/raw/gitas/bhagavadgita.csv
../../venv/bin/python gitas_spider.py          # Other Gitas → data/raw/gitas/gitas.csv
```

> The spiders are standalone scripts (each sets its own crawl settings, including a browser user-agent — the mirror drops connections from non-browser UAs). Note the site's `robots.txt` requests a 10-second crawl delay.

## Regenerate the processed datasets (notebooks)

The notebooks read `data/raw/…` and write `data/processed/…`:

```bash
venv/bin/jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=python3 --output /tmp/out.ipynb \
  notebooks/make_bhagavadgita_dataset.ipynb   # → data/processed/gitas/bhagavad_gita.csv
venv/bin/jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=python3 --output /tmp/out.ipynb \
  notebooks/make_gitas_dataset.ipynb          # → data/processed/gitas/<gita>.csv
venv/bin/jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.kernel_name=python3 --output /tmp/out.ipynb \
  notebooks/make_upanishad_dataset.ipynb      # → data/processed/upanishads/<upanishad>.csv
```

> The `--ExecutePreprocessor.kernel_name=python3` override is required: the notebooks were authored in 2020 and pin a Windows kernel name that no longer exists. Verified on Python 3.14: the notebooks regenerate `data/processed/` byte-identical to the committed CSVs.

## Docker

```bash
docker build -t indian-scriptures:latest .
docker run --rm -v "$PWD/data:/app/data" indian-scriptures:latest
→ runs the full pipeline: the spiders refresh data/raw, then the notebooks regenerate data/processed
```

> Mounting `data/` keeps the scraped and processed CSVs on your host; without the mount, the container's output is discarded on exit. The image is multi-platform — the same `Dockerfile` builds on linux/amd64 and linux/arm64.

## Directory structure

```text
indian-scriptures/
├── .github/
│   └── workflows/
│       ├── codeql.yml               - CodeQL Advanced analysis
│       └── super-linter.yml         - linting of changed files
├── .gitignore                       - files to ignore on git
├── LICENSE                          - license description
├── README.md                        - this README
├── data/
│   ├── processed/
│   │   ├── gitas/                   - 8 processed gita CSVs (title/mantra/number)
│   │   └── upanishads/              - 11 processed upanishad CSVs
│   └── raw/
│       ├── gitas/                   - raw spider output (bhagavadgita.csv, gitas.csv)
│       └── upanishads/              - raw spider output (upanishads.csv)
├── notebooks/
│   ├── make_bhagavadgita_dataset.ipynb   - raw → processed (Bhagavad Gita)
│   ├── make_gitas_dataset.ipynb          - raw → processed (Other Gitas)
│   └── make_upanishad_dataset.ipynb      - raw → processed (Upanishads)
├── requirements.txt                 - Python dependencies
├── scrapy.cfg                       - scrapy project configuration
└── scriptures/
    ├── __init__.py                  - package init
    ├── items.py                     - scrapy item definitions
    ├── middlewares.py               - scrapy middlewares
    ├── pipelines.py                 - scrapy pipelines
    ├── settings.py                  - scrapy settings
    └── spiders/
        ├── __init__.py              - package init
        ├── bhagavadgita_spider.py   - Śrīmad Bhagavad Gītā spider
        ├── gitas_spider.py          - Other Gitas spider
        └── upanishad_spider.py      - Upanishads spider
```
