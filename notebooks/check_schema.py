import pandas as pd

def check_schema(df, name, grain=("iso3", "year")):
    """
    Check a cleaned dataframe against the team schema.
    - grain: key columns that must uniquely identify a row.
             Default is ("iso3", "year"). For country-level files with no year
             (e.g. Open Food Facts), use grain=("iso3",).
    Returns True if no problems were found, False otherwise.
    """
    problems = []
    grain = list(grain)

    # 1. Key columns exist
    missing_keys = [k for k in grain if k not in df.columns]
    if missing_keys:
        problems.append(f"missing key column(s): {missing_keys}")

    if not missing_keys:
        # 2. No missing values in keys
        null_keys = df[grain].isna().sum()
        null_keys = null_keys[null_keys > 0]
        if len(null_keys):
            problems.append(f"missing values in key columns: {null_keys.to_dict()}")

        # 3. One row per key combination
        n_dup = df.duplicated(grain).sum()
        if n_dup:
            problems.append(f"{n_dup} duplicate rows on {grain} "
                            "(a split such as sex or age is probably still in the data)")

        # 4. iso3 format: uppercase 3-letter codes
        if "iso3" in grain:
            bad = df.loc[~df["iso3"].astype(str).str.fullmatch(r"[A-Z]{3}"), "iso3"].unique()
            if len(bad):
                problems.append(f"iso3 values not uppercase 3-letter codes: {list(bad)[:10]}")

        # 5. year is an integer
        if "year" in grain and df["year"].dtype.kind != "i":
            problems.append(f"year dtype is {df['year'].dtype}, expected int")

    # 6. snake_case column names
    bad_names = [c for c in df.columns if c != c.lower() or " " in c or "-" in c]
    if bad_names:
        problems.append(f"column names not snake_case: {bad_names}")

    # 7. Sentinel values that should be NaN
    num = df.select_dtypes("number")
    sentinels = [c for c in num.columns if num[c].isin([-999, -99, -9999]).any()]
    if sentinels:
        problems.append(f"sentinel values (-999 / -99 / -9999) in: {sentinels}")

    # 8. Empty-string or "NA"-style text that should be NaN
    txt = df.select_dtypes("object")
    text_missing = [c for c in txt.columns
                    if txt[c].astype(str).str.strip().str.lower()
                       .isin(["", "na", "n/a", "nan", "null", "none", "-"]).any()
                    and c not in grain]
    if text_missing:
        problems.append(f"text placeholders for missing values in: {text_missing}")

    # Summary line (paste this in the group chat)
    years = (f"{df['year'].min()}-{df['year'].max()}"
             if "year" in df.columns and df["year"].notna().any() else "n/a")
    n_iso = df["iso3"].nunique() if "iso3" in df.columns else "n/a"
    print(f"{name}: {df.shape[0]} rows x {df.shape[1]} cols | iso3: {n_iso} | years: {years}")

    if problems:
        print("  PROBLEMS:")
        for p in problems:
            print(f"   - {p}")
        return False
    print("  OK")
    return True