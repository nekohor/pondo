import pondo
import pandas as pd

record_type = "ledger"

factor_names = ["asym_flt", "sym_flt"]

filename = "D:/NutCloudSync/work/topics/999others/20191226冷轧追溯浪形异议/coils.xlsx"


df = pd.read_excel(filename)
pondo.specific_export(factor_names, record_type, df["coil_id"])
