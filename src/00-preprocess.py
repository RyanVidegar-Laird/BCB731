#! /usr/bin/env python3

# Preprocess data
import sys
from pathlib import Path
import warnings
import re
import pandas as pd
import numpy as np

# basic positional args. 1: neoag file, 2: surv. file
path_neoag, path_surv = (arg for arg in sys.argv[1:3])

# Manually specify dtypes to avoid excel quirks
dtype_surv = {"Months": np.float32, "Status": bool}
dtype_neoag = {
    "MUTATION_ID": str,
    "WT.Peptide": str,
    "MT.Peptide": str,
    "MT.Allele": str,
    "WT.Score": np.int64,
    "MT.Score": np.int64,
    "HLA": str,
}

# ignore annoying openpyxl warning about file extension
with warnings.catch_warnings():
    warnings.simplefilter(action="ignore", category=UserWarning)

    df_neoag = pd.read_excel(
        path_neoag, sheet_name=None, usecols=range(1, 9), index_col=1, dtype=dtype_neoag
    )

    df_surv = pd.read_excel(path_surv, index_col=0, sheet_name=None, dtype=dtype_surv)

# regex patterns to clean up dataset names
neoag_ds_pattern = r"(.*?)(\s.+)"
surv_ds_pattern = r"(Survival\s)(.*?)(\s.*)"

# Concat and reindex neoantigen tables into one df
df_neoag = pd.concat(df_neoag, copy=False)
df_neoag.index = pd.MultiIndex.from_tuples(
    [(re.search(neoag_ds_pattern, i[0]).group(1), i[1]) for i in df_neoag.index],
    names=["Dataset", "Sample"],
)

# Same for survival data
df_surv = pd.concat(df_surv, verify_integrity=True, copy=False)
df_surv.index = pd.MultiIndex.from_tuples(
    [(re.search(surv_ds_pattern, i[0]).group(2), i[1]) for i in df_surv.index],
    names=["Dataset", "Sample"],
)

# Save to Arrow format
df_surv.to_feather(Path() / "data" / "survival.arrow")
df_neoag.to_feather(Path() / "data" / "neoantigens.arrow")
