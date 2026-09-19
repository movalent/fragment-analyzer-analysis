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

    file_name = '2026 03 25 Electropherogram.csv'

    return pd.read_csv(paths.input / file_name)

def save_adjusted_peaks(paths: Path, sample: str, peaks: pd.DataFrame) -> None:
    """
    Update the CSV containing manually adjusted peak boundaries.

    Args:
        paths (Path): Object containing project directory paths.
        sample (str): Name of the sample column to save.
        peaks (pd.DataFrame): DataFrame containing the adjusted peak boundaries.

    Returns:
        None    
    """

    output_file = paths.output / 'adjusted_peak_boundaries.csv'
    output_file.parent.mkdir(parents=True, exist_ok=True)

    adjusted = peaks.copy().reset_index(drop=True)

    adjusted.insert(0, 'sample', sample)  # Add header to csv file

    if output_file.exists():
        existing = pd.read_csv(output_file)
        existing = existing[existing['sample'] != sample]

        adjusted = pd.concat([existing, adjusted], ignore_index=True)

    adjusted.to_csv(output_file, index=False)