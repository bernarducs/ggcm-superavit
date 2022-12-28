"""fp.unidade_orcamentaria

Este módulo retorna dataframe relativo as unidade orçamentárias e,
poder administrativo.
"""

import pandas as pd


def tab_po_ug(dir) -> pd.DataFrame:
    cols_po = [
        'Unidade Orçamentária',
        'UG',
        'PO',
        'PO Nomenclatura',
        'Filtro Administração',
    ]

    return pd.read_excel(
        f'{dir}/dicionário PO-UG.xlsx',
        dtype={'UG': 'str'},
        usecols=cols_po,
    )
