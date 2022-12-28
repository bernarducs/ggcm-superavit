"""fp.plano_contas

Este módulo retorna dataframe relativo ao plano de contas onde
estão todas as flags das informações complementares.
"""

import pandas as pd


def tab_plano_contas(dir, analiticas=True) -> pd.DataFrame:
    df = pd.read_csv(
        f'{dir}/manual_plano_de_contas.txt', sep=';', encoding='latin-1'
    )
    df['CONTA'] = df['CONTA'].str.replace('.', '', regex=False).astype('int')
    if analiticas:
        df.query('ES == "S"', inplace=True)

    return df
