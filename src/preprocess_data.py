import pandas as pd


def select_sample(input_df: pd.DataFrame) -> str:
    """
    Prompt the user to select a sample trace from a DataFrame.

    The function displays all sample names (taken from DataFrame columns)
    as a numbered list and requests user input via the command line.

    Args:
        input_df (pd.DataFrame): DataFrame containing raw trace data

    Returns:
        str: Name of the selected sample column.
    """

    df = input_df.copy()

    sample_names = list(df.columns[1:])

    print('=================== Traces ===================\n')
    for index, sample in enumerate(sample_names, start=1):
        print(f'{index}: {sample}')

    print()
    print('Select the sample: ')

    sample_idx = int(input('> ')) - 1
    return sample_names[sample_idx]
