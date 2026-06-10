

def select_sample(input_df) -> list[str]:

    df = input_df.copy()

    sample_names = list(df.columns[1:])

    print('=================== Traces ===================\n')
    for index, sample in enumerate(sample_names, start=1):
        print(f'{index}: {sample}')

    print()
    print('Select the sample: ')

    sample_idx = int(input('> ')) - 1
    return sample_names[sample_idx]
