#!/bin/sh
# Refresh pipeline: scrape the scriptures, then regenerate the processed datasets.
set -e

cd /app/scriptures/spiders
echo "== Scraping Srimad Bhagavad Gita =="
python bhagavadgita_spider.py
echo "== Scraping Other Gitas =="
python gitas_spider.py
# The Upanishad spider still targets upanishads.iitk.ac.in, which is
# offline; it is parked until a reachable source is found.

cd /app
echo "== Regenerating processed datasets =="
for nb in make_bhagavadgita_dataset make_gitas_dataset make_upanishad_dataset; do
  echo "-- $nb"
  jupyter nbconvert --to notebook --execute \
    --ExecutePreprocessor.kernel_name=python3 \
    --output "/tmp/$nb.out.ipynb" \
    "notebooks/$nb.ipynb"
done

echo "== Done. Raw data: /app/data/raw  Processed: /app/data/processed =="
