"""fp.saldo_mensal

Este módulo retorna dataframe relativo aos saldos mensais que servirão
de base para contas do tipo f-pura e mista.

    FORMATO DO ARQUIVO
Dois arquivos por mês
AAAA_M_01.01_AcompSaldoMensal.txt a ser classificada como F-PURA
AAAA_M_AcompSaldoMensalFinPerm.txt a ser classificada como MISTA

"""

import os
import pandas as pd


MESES = {
    'Janeiro': 1,
    'Fevereiro': 2,
    'Março': 3,
    'Abril': 4,
    'Maio': 5,
    'Junho': 6,
    'Julho': 7,
    'Agosto': 8,
    'Setembro': 9,
    'Outubro': 10,
    'Novembro': 11,
    'Dezembro': 12,
}


def tab_saldo_txt_para_xlsx(dir) -> pd.DataFrame:
    cols_saldo_ini = [
        'UNIDADE ORÇAMENTÁRIA',
        'ANO',
        'MÊS',
        'CONTA',
        'INFORMAÇÃO COMPLEMENTAR',
        'SALDO INICIAL',
        # 'NATUREZA INICIAL',
        'MOV DÉBITO',
        'MOV CRÉDITO',
        'SALDO FINAL',
        'NATUREZA FINAL',
    ]

    saldo_txts = [f for f in os.listdir(dir) if f.endswith('.txt')]
    dfs = list()
    for saldo_txt in saldo_txts:

        df_saldo = pd.read_csv(
            f'{dir}/{saldo_txt}',
            sep=';',
            encoding='latin-1',
            usecols=cols_saldo_ini,
            decimal=',',
            thousands='.',
            dtype={'UNIDADE ORÇAMENTÁRIA': 'O'},
        )

        df_saldo[['ATRIBUTO1', 'ATRIBUTO2']] = 'F-PURA'
        if 'FinPerm' in saldo_txt:
            df_saldo['ATRIBUTO1'] = 'MISTA'
            df_saldo['ATRIBUTO2'] = (
                'MISTA - ' + df_saldo['INFORMAÇÃO COMPLEMENTAR'].str[-1]
            )

        dfs.append(df_saldo)

    df = pd.concat(dfs)
    df['MES_NUM'] = df['MÊS'].map(MESES)
    df['UG'] = df['UNIDADE ORÇAMENTÁRIA'].str.replace('.', '', regex=False)
    df.drop(['MÊS', 'UNIDADE ORÇAMENTÁRIA'], axis=1, inplace=True)

    return df
