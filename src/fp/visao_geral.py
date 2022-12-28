"""fp.visao_geral

Este módulo retorna dataframe relativo a visão geral que servirá
de base para contas do tipo p-pura.
"""

import os
import re
import pandas as pd


USE_COLS = [
    'Ano',
    'Orgao',
    'Unidade',
    'Conta',
    'Natureza',
    # 'Título',
    # 'Sistema',
    # 'Saldo Ano Anterior',
    'Saldo Mês Anterior',
    'Movimento Débito no mês',
    'Movimento Crédito no mês',
    'Saldo Atual',
]
ORDER_COLS = [
    'Ano',
    'CONTA',
    'INFORMAÇÃO COMPLEMENTAR',
    'Saldo Mês Anterior',
    'Movimento Débito no mês',
    'Movimento Crédito no mês',
    'Saldo Atual',
    'Natureza',
    'ATRIBUTO1',
    'ATRIBUTO2',
    'MES_NUM',
    'UG',
]
RENAME_COLS = [
    'ANO',
    'CONTA',
    'INFORMAÇÃO COMPLEMENTAR',
    'SALDO INICIAL',
    'MOV DÉBITO',
    'MOV CRÉDITO',
    'SALDO FINAL',
    'NATUREZA FINAL',
    'ATRIBUTO1',
    'ATRIBUTO2',
    'MES_NUM',
    'UG',
]
PATTERN = r'(\d{6})'


def tab_vgeral_txt_xlsx(dir) -> pd.DataFrame:

    saldo_txts = [f for f in os.listdir(dir) if f.endswith('.txt')]
    dfs = list()
    for saldo_txt in saldo_txts:
        mes_ano_str = re.findall(PATTERN, saldo_txt)[0]
        df = pd.read_csv(
            f'{dir}/{saldo_txt}',
            sep=';',
            usecols=USE_COLS,
            decimal=',',
            thousands='.',
            dtype={'Conta': 'O', 'Orgao': 'O', 'Unidade': 'O'},
        )
        df['INFORMAÇÃO COMPLEMENTAR'] = ''
        df['CONTA'] = df.Conta.str.replace('.', '', regex=False).astype('int')
        df['MES_NUM'] = int(mes_ano_str[:-4])
        df['UG'] = df['Orgao'] + df['Unidade'].str.zfill(2)
        df.drop(['Conta', 'Orgao', 'Unidade'], axis=1, inplace=True)
        df[['ATRIBUTO1', 'ATRIBUTO2']] = 'P-PURA'
        dfs.append(df)

    df = pd.concat(dfs)
    df = df[ORDER_COLS]
    df.columns = RENAME_COLS
    return df
