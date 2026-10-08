# vabi-YouAreWhatYouEat

## Project structure

```
vabi-YouAreWhatYouEat/
├── data/
│   ├── raw/          # untouched downloads: FAO, GHO CSVs, Open Food Facts, urbanization
│   ├── reference/    # hand-built tables: who_guidelines.csv
│   └── cleaned/      # outputs of the notebooks
├── notebooks/
│   ├── 01_fao_cleaning.ipynb
│   ├── 02_who_gho_cleaning.ipynb
│   ├── 03_open_food_facts_cleaning.ipynb
│   ├── 04_urbanization_cleaning.ipynb
│   ├── 05_merge_all.ipynb
│   └── 06_feature_engineering.ipynb
├── tableau/          # exported .twbx workbook and screenshots
├── site/             # the static website (HTML/CSS/JS, embedded Tableau views)
├── report/           # report drafts and figures
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the notebooks in numeric order; each one reads from `data/raw` or `data/reference` and writes to `data/cleaned`.

# WHO guideline reference values

`who_guidelines.csv` is a hand-built table, not a downloaded dataset.

- **Source:** WHO, "Healthy diet" fact sheet, https://www.who.int/news-room/fact-sheets/detail/healthy-diet
- **Accessed:** 2026-10-08
- **Method:** the numeric recommendations for adults were copied from the fact sheet text and entered as one row per nutrient. Ranges have both `min` and `max`; one-sided limits leave the other blank.
- **Limitations:** WHO gives limits as % of energy, while FAO supply data is in kcal and grams per person per day, so values need converting before comparison. WHO "free sugars" does not match FAO "sugar and sweeteners" exactly.