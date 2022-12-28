"""tabela_superavit.py

Arquivo que retorna um pd.Dataframe para apuração do superávit.
"""

import pandas as pd
import fp

DATASETS_DIR = 'src/datasets'

saldo_dir = f'{DATASETS_DIR}/saldo_mensal'
df_saldos = fp.tab_saldo_txt_para_xlsx(saldo_dir)

visao_geral_dir = f'{DATASETS_DIR}/visao_geral'
df_vgeral = fp.tab_vgeral_txt_xlsx(visao_geral_dir)

contas_saldo = df_saldos['CONTA'].unique().tolist()
df_vgeral.query('CONTA != @contas_saldo', inplace=True)

df = pd.concat([df_vgeral, df_saldos], ignore_index=True).sort_values(
    ['MES_NUM', 'CONTA', 'UG']
)

df['classe'] = df.CONTA.astype('str').str[:1].astype('int8')
df.query('classe == [1, 2, 7, 8]', inplace=True)

cols_categ = ['UG', 'CONTA', 'NATUREZA FINAL', 'ATRIBUTO1', 'ATRIBUTO2']

df[cols_categ] = df[cols_categ].astype('category')
df['MES'] = df['MES_NUM'].map({v: k for k, v in fp.MESES.items()})

df_plano_contas = fp.tab_plano_contas(f'{DATASETS_DIR}/plano_de_contas', True)
contas_analiticas = df_plano_contas['CONTA'].tolist()
df.query('CONTA == @contas_analiticas', inplace=True)

df_po_ug = fp.tab_po_ug(f'{DATASETS_DIR}/PO-UG')

df_resultado = df.merge(df_po_ug, on='UG')
df_resultado.to_excel('src/datasets/outputs/resultado.xlsx', index=False)
