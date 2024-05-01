import pandas as pd
import random as ran
import numpy as np

# read MKSs into memory for rapid use below. Split and organise into dictionary with MKS code as key.
mkc = {}
mkc_df = pd.read_csv("exports/NEW_MKC.CSV")
mkc_codes = pd.Series(mkc_df["Mark Scheme code"]).unique()

for mkc_code in mkc_codes:
    mkc[mkc_code] = mkc_df.loc[mkc_df["Mark Scheme code"] == mkc_code]
    # print(mkc[mkc_code].head())

# read SAS_MKS.csv into mega-df, filtering out any records that do not have a new MKS.
sas_df_all = pd.read_csv("exports/SAS_MKS.CSV", low_memory=False)
sas_df = sas_df_all[sas_df_all["NEWMKS"].isin(mkc_codes)]

sas_df = sas_df.copy()

sas_df["SAS_ACTG"] = sas_df["SAS_ACTG"].astype(str)

# generate marks - where mark/grade scheme - and appropriate random grade
cnt = 0
for index, row in sas_df.iterrows():
    
    if cnt == 5000:
        print(index)
        cnt = 0

    mkc_code = row["NEWMKS"]
    this_mkc = mkc[mkc_code]

    # generate for mark/grade schemes: uses char 3 = "M" to id mark/grade schemes
    """ relies on standardised scheme naming """
    if row["NEWMKS"][3] == "M":

        num = ran.randrange(0, 100, 1)
        sas_df.loc[index, "SAS_ACTM"] = num

        this_mkc = this_mkc.loc[(this_mkc["Max Mark display"] >= num) & (this_mkc["Min Mark display"] <= num)]

    samp = this_mkc.sample(n=1)
    grade = samp["Grade"].iloc[0]

    sas_df.loc[index, "SAS_ACTG"] = grade

    cnt += 1
        
# select columns and format for export

sas_df["SAS_ACTM"] = sas_df["SAS_ACTM"].apply(lambda x: x * 100 if not pd.isna(x) else np.nan)
sas_df["SAS_ACTM"] = sas_df["SAS_ACTM"].astype(pd.Int64Dtype())
sas_df["MAB_SEQ"] = sas_df["MAB_SEQ"].astype(str).str.zfill(3)

sas_df.to_csv("output/SAS_SUMMARY.CSV", index=False)

fields = ["SPR_CODE", "MOD_CODE", "MAV_OCCUR", "AYR_CODE", "PSL_CODE", "MAP_CODE", "MAB_SEQ", "SAS_ACTM", "SAS_ACTG"]
sas_df = sas_df[fields]

sas_df.to_csv("output/SAS_TO_IMPORT.CSV", index=False)

print("See output folder for your CSVs!")