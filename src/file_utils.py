from pathlib import Path
import pandas as pd

def load_data(paths: Path) -> pd.DataFrame:
    """
    Load fragment analyzer trace data from a ProSize-exported CSV file.

    Args:
        paths (Path): Object containing project directory paths.

    Returns:
        pd.DataFrame: DataFrame containing raw fragment analyzer trace data.
    """

    file_name = '2026 05 22 Electropherogram.csv'

    return pd.read_csv(paths.input / file_name)
