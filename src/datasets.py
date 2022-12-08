import os
import re
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


def vgeral_txt_xlsx(dir):
    cols_visao_geral = [
        'Ano',
        'Conta',
        'Natureza',
        'Título',
        # 'Sistema',
        'Saldo Ano Anterior',
        'Saldo Mês Anterior',
        'Movimento Débito no mês',
        'Movimento Crédito no mês',
        'Saldo Atual',
    ]
    pattern = r'(\d{6})'

    saldo_txts = [f for f in os.listdir(dir) if f.endswith('txt')]
    dfs = list()
    for saldo_txt in saldo_txts:
        mes_ano_str = re.findall(pattern, saldo_txt)[0]

        df = pd.read_csv(
            f'{dir}/{saldo_txt}',
            sep=';',
            usecols=cols_visao_geral,
            decimal=',',
            thousands='.',
            dtype={'Conta': 'O'},
        )
        df['CONTA'] = df.Conta.str.replace('.', '', regex=False)
        df['MES_NUM'] = mes_ano_str[:-4]
        df.drop('Conta', axis=1, inplace=True)
        df.to_excel(f'src/datasets/outputs/visao_geral.xlsx', index=False)
        dfs.append(df)

    df = pd.concat(dfs)
    df.to_excel(
        f'src/datasets/outputs/visao_geral_{mes_ano_str}.xlsx', index=False
    )
    return df


def saldo_txt_para_xlsx(dir):
    cols_saldo_ini = [
        'UNIDADE ORÇAMENTÁRIA',
        'ANO',
        'MÊS',
        'CONTA',
        'INFORMAÇÃO COMPLEMENTAR',
        'SALDO INICIAL',
        'NATUREZA INICIAL',
        'MOV DÉBITO',
        'MOV CRÉDITO',
        'SALDO FINAL',
        'NATUREZA FINAL',
    ]
    cols_categ = [
        'UNIDADE ORÇAMENTÁRIA',
        'MÊS',
        'INFORMAÇÃO COMPLEMENTAR',
        'NATUREZA INICIAL',
        'NATUREZA FINAL',
        'arquivo',
    ]

    saldo_txts = [f for f in os.listdir(dir) if f.endswith('txt')]
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

        df_saldo = df_saldo.assign(arquivo='F-PURA')
        if 'FinPerm' in saldo_txt:
            df_saldo = df_saldo.assign(arquivo='MISTA')

        dfs.append(df_saldo)

    df = pd.concat(dfs)
    df['MES_NUM'] = df['MÊS'].map(MESES)
    df[cols_categ] = df[cols_categ].astype('category')
    # df.to_parquet('src/datasets/outputs/saldo_inicial.parquet.gzip', index=False)
    # df.to_excel(f'src/datasets/outputs/saldo_mensal.xlsx', index=False)

    return df


if __name__ == '__main__':
    visao_geral_dir = 'src/datasets/visao_geral'
    saldo_dir = 'src/datasets/saldo_mensal'

    df_vgeral = vgeral_txt_xlsx(visao_geral_dir)
    df_saldos = saldo_txt_para_xlsx(saldo_dir)
