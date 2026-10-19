Keys:        iso3 (uppercase alpha-3), year (int)
Grain:       one row per iso3-year (no sex/age/urban splits left in)
Names:       snake_case, unit in the name where useful (sugar_g_day)
Missing:     NaN only. Never 0, -999 or "".
Country names: only in data/reference/countries.csv, never used as a join key
Lag:         <decide in the meeting: 5 or 10 years>
File names:  data/cleaned/<source>_clean.csv