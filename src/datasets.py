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


def plano_contas(sinteticas=True):
    df = pd.read_csv(
        'src/datasets/plano_de_contas/manual_plano_de_contas.txt',
        sep=';',
        encoding='latin-1'
        )
    df['CONTA'] = df['CONTA'].str.replace('.', '', regex=False).astype('int')
    if sinteticas:
        df.query('ES == "S"', inplace=True)

    return df


def vgeral_txt_xlsx(dir):
    cols_visao_geral = [
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
    pattern = r'(\d{6})'

    saldo_txts = [f for f in os.listdir(dir) if f.endswith('.txt')]
    dfs = list()
    for saldo_txt in saldo_txts:
        mes_ano_str = re.findall(pattern, saldo_txt)[0]

        df = pd.read_csv(
            f'{dir}/{saldo_txt}',
            sep=';',
            usecols=cols_visao_geral,
            decimal=',',
            thousands='.',
            dtype={'Conta': 'O', 'Orgao': 'O', 'Unidade': 'O'},
        )
        df['INFORMAÇÃO COMPLEMENTAR'] = ''
        df['CONTA'] = df.Conta.str.replace('.', '', regex=False).astype('int')
        df['MES_NUM'] = int(mes_ano_str[:-4])
        df['UG'] = df['Orgao'] + df['Unidade'].str.zfill(2)
        df.drop(['Conta', 'Orgao', 'Unidade'], axis=1, inplace=True)
        df['arquivo'] = 'P-PURA'
        dfs.append(df)

    df = pd.concat(dfs)
    # df.to_excel(
    #     f'src/datasets/outputs/visao_geral_{mes_ano_str}.xlsx', index=False
    # )
    return df


def saldo_txt_para_xlsx(dir):
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

        df_saldo = df_saldo.assign(arquivo='F-PURA')
        if 'FinPerm' in saldo_txt:
            df_saldo = df_saldo.assign(arquivo='MISTA')

        dfs.append(df_saldo)

    df = pd.concat(dfs)
    df['MES_NUM'] = df['MÊS'].map(MESES)
    df['UG'] = df['UNIDADE ORÇAMENTÁRIA'].str.replace('.', '', regex=False)
    df.drop(['MÊS', 'UNIDADE ORÇAMENTÁRIA'], axis=1, inplace=True)
    
    # df.to_excel(f'src/datasets/outputs/saldo_mensal.xlsx', index=False)

    return df


if __name__ == '__main__':
    saldo_dir = 'src/datasets/saldo_mensal'
    df_saldos = saldo_txt_para_xlsx(saldo_dir)
    contas_saldo = df_saldos['CONTA'].unique().tolist()
    
    visao_geral_dir = 'src/datasets/visao_geral'
    df_vgeral = vgeral_txt_xlsx(visao_geral_dir)
    df_vgeral.query('CONTA != @contas_saldo', inplace=True)

    vgeral_cols = ['Ano', 'CONTA', 'INFORMAÇÃO COMPLEMENTAR', 'Saldo Mês Anterior', 'Movimento Débito no mês', 'Movimento Crédito no mês', 'Saldo Atual', 'Natureza', 'arquivo', 'MES_NUM', 'UG']
    saldos_cols = ['ANO', 'CONTA', 'INFORMAÇÃO COMPLEMENTAR', 'SALDO INICIAL', 'MOV DÉBITO', 'MOV CRÉDITO', 'SALDO FINAL', 'NATUREZA FINAL', 'arquivo', 'MES_NUM', 'UG']
    df_vgeral = df_vgeral[vgeral_cols]
    df_vgeral.columns = saldos_cols

    df = pd.concat([df_vgeral, df_saldos], ignore_index=True).sort_values(['MES_NUM', 'CONTA', 'UG'])
    
    df['classe'] = df.CONTA.astype('str').str[:1].astype('int8')
    df.query('classe == [1, 2, 7, 8]', inplace=True)

    cols_categ = [
        'UG',
        'CONTA',
        'NATUREZA FINAL',
        'arquivo',
    ]

    df[cols_categ] = df[cols_categ].astype('category')
    df['MES'] = df['MES_NUM'].map({v: k for k, v in MESES.items()})

    df_plano_contas = plano_contas(True)
    contas_analiticas = df_plano_contas['CONTA'].tolist()
    df.query('CONTA == @contas_analiticas', inplace=True)

    cols_po = ['Unidade Orçamentária', 'UG', 'PO', 'PO Nomenclatura']
    df_po_ug = pd.read_excel('src/datasets/PO-UG/dicionário PO-UG.xlsx', dtype={'UG': 'str'}, usecols=cols_po)

    df_resultado = df.merge(df_po_ug, on='UG')
    df_resultado.to_excel('src/datasets/outputs/resultado.xlsx', index=False)






'''
Teste  Escolher 1 conta (3 contas no total) de 1 UG (14.01) 

F/pura - 111110200 1.1.1.1.1.02.00
Mista - 213110101 2.1.3.1.1.01.01
P/pura - 123110101 1.2.3.1.1.01.01

A prova dos 9 é o BV global
'''