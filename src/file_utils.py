import pandas as pd

def load_data(paths) -> pd.DataFrame:

    file_name = '2026 05 22 Electropherogram.csv'

    return pd.read_csv(paths.input / file_name)
