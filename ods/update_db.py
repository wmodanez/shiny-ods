import json.decoder
import time
from functools import lru_cache
from pathlib import Path

import openpyxl
import pandas as pd
import requests
from openpyxl.utils.dataframe import dataframe_to_rows


def df_to_excel(df, ws, name_sheet, header=False, index=False, startrow=0, startcol=0):
    """
    Escreve um DataFrame df em uma planilha openpyxl ws.
    Parâmetros:
    df (DataFrame): O DataFrame a ser escrito na planilha.
    ws (Workbook): O objeto de planilha openpyxl onde o DataFrame será escrito.
    name_sheet (str): O nome da nova aba a ser criada na planilha.
    header (bool, opcional): Se True, escreve os nomes das colunas do DataFrame. Padrão é False.
    index (bool, opcional): Se True, escreve os índices do DataFrame. Padrão é False.
    startrow (int, opcional): A linha inicial onde os dados serão escritos. Padrão é 0.
    startcol (int, opcional): A coluna inicial onde os dados serão escritos. Padrão é 0.
    Retorna:
    Workbook: O objeto de planilha openpyxl com o DataFrame escrito.
    """
    """Write DataFrame df to openpyxl worksheet ws"""

    rows = dataframe_to_rows(df, header=header, index=index)
    ws.create_sheet(name_sheet)
    ws.active = ws[name_sheet]

    for r_idx, row in enumerate(rows, startrow + 1):
        for c_idx, value in enumerate(row, startcol + 1):
            ws.active.cell(row=r_idx, column=c_idx).value = value
    return ws


def get_sidra_data(indicador):
    """
    Obtém dados da API SIDRA para o indicador fornecido.
    Parâmetros:
    indicador (str): URL do indicador para o qual os dados devem ser obtidos.
    Retorna:
    dict: Dados obtidos da API SIDRA se a solicitação for bem-sucedida.
    None: Se a solicitação falhar após o número máximo de tentativas.
    Exceções:
    Exceção genérica capturada e tratada com tentativas de reconexão.
    Notas:
    - A função tenta obter dados da API SIDRA até um máximo de 5 tentativas.
    - Em caso de falha, espera 5 segundos antes de tentar novamente.
    - A codificação da resposta é definida como 'UTF-8'.
    """
    """Get data from SIDRA API for the given indicator"""
    # url = f'{indicador}/json/data?formato=json'

    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = requests.get(indicador, timeout=90)
            response.encoding = 'UTF-8'

            if response.status_code == 200:
                data = response.json()
                return data

        except Exception as e:
            retry_count += 1
            if retry_count == max_retries:
                print(f'Erro de conexão após {max_retries + 1} tentativas para o indicador {indicador}: {e}')
            else:
                print(f'Tentativa {retry_count} falhou. Tentando novamente em 5 segundos...')
                time.sleep(5)
    return None


@lru_cache(maxsize=1)
def load_indicadores():
    df_indicadores: pd.DataFrame = pd.read_csv(
        Path(__file__).parent / 'db/indicadores.csv', sep=';'
    )
    df_indicadores = df_indicadores[df_indicadores['RBC'] == True]
    return df_indicadores


URL_BASE = 'https://apisidra.ibge.gov.br/values'

list_indicadores = {
    'Objetivo1': {
        'Meta1.1': {
            'Indicador 1.1.1': '/t/5817/n1/all/n3/all/v/all/p/all/d/v9617%201'
        },
        'Meta1.2': {
            'Indicador 1.2.1': '/t/5877/n1/all/n3/all/v/all/p/all/d/v9948%201'
        },
        'Meta1.5': {
            'Indicador 1.5.1': '/t/6689/n1/all/n3/all/v/all/p/all/d/v9619%201',
            'Indicador 1.5.4': '/t/6673/n1/all/n3/all/v/all/p/all/d/v9600%201'
        }
    },
    'Objetivo2': {
        'Meta2.1': {
            'Indicador 2.1.2': '/t/6665/n1/all/v/all/p/all/c12404/all/d/v800%201,v2133%201,v9591%201,v9592%201,v9593%201,v9594%201'
        },
        'Meta2.5': {
            'Indicador 2.5.1': '/t/6745/n1/all/v/all/p/all'
        },
        'Meta2.a': {
            'Indicador 2.a.1': '/t/6840/n1/all/v/all/p/all/d/v9963%202,v9964%202,v9965%202',
            'Indicador 2.a.2': '/t/6833/n1/all/v/all/p/all/d/v10104%201,v10105%201,v10106%201'
        },
        'Meta2.b': {
            'Indicador 2.b.1': '/t/6932/n1/all/v/all/p/all/d/v10066%202,v10325%202'
        }
    },
    'Objetivo3': {
        'Meta3.1': {
            'Indicador 3.1.1': '/t/6694/n1/all/n3/all/v/all/p/all/d/v9730%201',
            'Indicador 3.1.2': '/t/7498/n1/all/n3/all/v/all/p/all/d/v11598%201'
        },
        'Meta3.2': {
            'Indicador 3.2.1': '/t/6695/n1/all/n3/all/v/all/p/all/d/v9731%201',
            'Indicador 3.2.2': '/t/6696/n1/all/n3/all/v/all/p/all/d/v9732%201'
        },
        'Meta3.3': {
            'Indicador 3.3.2': '/t/8417/n1/all/n3/all/v/all/p/last%2014/c2/all/c58/all/d/v9733%201',
            'Indicador 3.3.3': '/t/9040/n3/all/n1103/all/v/12763,12764/p/all/d/v12763%201',
            'Indicador 3.3.4': '/t/8414/n1/all/n3/all/v/9613,12381/p/all/c58/all/c2/all/d/v12381%201',
            'Indicador 3.3.5': '/t/9043/n1/all/n3/all/v/all/p/all/c2/all/c58/all/c12963/all'
        },
        'Meta3.4': {
            'Indicador 3.4.1': '/t/4277/n1/all/n3/all/v/11754,12948/p/all/c2/all/c58/all/d/v11754%202',
            'Indicador 3.4.2': '/t/8183/n1/all/n3/all/v/11704,11705/p/last%2022/c2/all/c58/all/d/v11704%201'
        },
        'Meta3.5': {
            'Indicador 3.5.2': '/t/5878/n1/all/v/all/p/all/d/v7068%201'
        },
        'Meta3.6': {
            'Indicador 3.6.1': '/t/4408/n1/all/n3/all/v/9734,11728/p/last%2021/c2/all/c58/all/d/v9734%201'
        },
        'Meta3.7': {
            'Indicador 3.7.2': '/t/8174/n1/all/n3/all/v/9433,11687/p/all/c58/all/d/v11687%201'
        },
        'Meta3.9': {
            'Indicador 3.9.2': '/t/8191/n1/all/n3/all/v/9737,11725/p/last%2017/c2/all/c58/all/d/v9737%201',
            'Indicador 3.9.3': '/t/8192/n1/all/n3/all/v/11726,11727/p/last%2020/c2/all/c58/all/d/v11726%202'
        },
        'Meta3.a': {
            'Indicador 3.a.1': '/t/8416/n1/all/n3/all/v/all/p/all/c2/all/d/v12360%201,v12361%201,v12382%201'
        }
    },
    'Objetivo4': {
        'Meta4.1': {
            'Indicador 4.1.2': '/t/4731/n1/all/n3/all/v/4721/p/all/c582/all/d/v4721%201'
        },
        'Meta4.2': {
            'Indicador 4.2.1.3': '/t/9038/n1/all/n3/all/v/9310/p/all/c1/all/d/v9310%201',
            'Indicador 4.2.1.2': '/t/9036/n1/all/n3/all/v/9310/p/all/c2/all/d/v9310%201',
            'Indicador 4.2.1.4': '/t/9039/n1/all/n3/all/v/9310/p/all/c1019/all/d/v9310%201',
            'Indicador 4.2.2': '/t/4734/n1/all/n3/all/v/4775,4796/p/all/c2/all/d/v4796%201'
        },
        'Meta4.5': {
            'Indicador 4.5.1': '/t/6674/n1/all/n3/all/v/all/p/all/d/v9601%202,v9603%202,v12746%202'
        },
        'Meta4.a': {
            'Indicador 4.a.1': '/t/7783/n1/all/n3/all/v/all/p/all/c812/all/d/v11084%201,v11085%201,v11086%201'
        },
        'Meta4.c': {
            'Indicador 4.c.1': '/t/7981/n3/all/n1/all/v/all/p/all/c813/all/d/v9610%201'
        }
    },
    'Objetivo5': {
        'Meta5.4': {
            'Indicador 5.4.1': '/t/6681/n1/all/n3/all/v/9471/p/all/c2/all/c58/all/d/v9471%201',
            'Indicador 5.4.1.2': '/t/6743/n1/all/n3/all/v/9471/p/all/c2/all/c86/all/d/v9471%201',
            'Indicador 5.4.1.3': '/t/9519/n1/all/n3/all/v/9471/p/all/c2/all/c1/all/d/v9471%201'
        },
        'Meta5.5': {
            'Indicador 5.5.1': '/t/6692/n1/all/n3/all/v/all/p/all/d/v9726%201',
            'Indicador 5.5.1.1': '/t/6693/n1/all/n3/all/v/all/p/all/d/v9729%201',
            'Indicador 5.5.1.2': '/t/7590/n1/all/v/all/p/all/c86/all/d/v9729%201',
            'Indicador 5.5.1.3': '/t/7584/n1/all/v/all/p/all/c86/all/d/v9726%201',
            'Indicador 5.5.2': '/t/9752/n1/all/n2/all/v/9437/p/all/c58/all/d/v9437%201',
            'Indicador 5.5.2.1': '/t/9763/n1/all/n2/all/v/9437/p/all/c86/all/d/v9437%201',
            'Indicador 5.5.2.2': '/t/9762/n1/all/n2/all/v/9437/p/all/c888/all/d/v9437%201'
        },
        'Meta5.b': {
            'Indicador 5.b.1': '/t/6863/n1/all/n2/all/v/5039/p/all/c2/all/c1/6795/d/v5039%201',
            'Indicador 5.b.1.1': '/t/6864/n1/all/n2/all/v/5039/p/all/c2/all/c86/all/d/v5039%201',
            'Indicador 5.b.1.2': '/t/6865/n1/all/n2/all/v/5039/p/all/c2/all/c58/all/d/v5039%201'
        }
    },
    'Objetivo6': {
        'Meta6.1': {
            'Indicador 6.1.1': '/t/9787/n1/all/n3/all/v/9484/p/all/d/v9484%201',
            'Indicador 6.1.1.1': '/t/9788/n1/all/v/9484/p/all/c2/all/d/v9484%201',
            'Indicador 6.1.1.2': '/t/9789/n1/all/v/9484/p/all/c58/95253/d/v9484%201',
            'Indicador 6.1.1.3': '/t/9790/n1/all/v/9484/p/all/c86/all/d/v9484%201',
            'Indicador 6.1.1.4': '/t/9791/n1/all/v/9484/p/all/c1/all/d/v9484%201'
        },
        'Meta6.2': {
            'Indicador 6.2.1': '/t/6835/n1/all/n3/all/v/all/p/all/d/v10107%201'
        },
        'Meta6.3': {
            'Indicador 6.3.2': '/t/7076/n121/all/n1/all/v/all/p/all/d/v10232%202'
        },
        'Meta6.4': {
            'Indicador 6.4.1': '/t/6968/n1/all/n3/all/v/all/p/all/c4/all/d/v10564%202,v12771%202',
            'Indicador 6.4.2': '/t/7077/n121/all/n1/all/v/all/p/all/d/v10233%201'
        },
        'Meta6.5': {
            'Indicador 6.5.1': '/t/6724/n1/all/v/all/p/all/d/v9772%201,v10228%201,v10229%201,v10230%201,v10231%201',
            'Indicador 6.5.2': '/t/6725/n1/all/v/all/p/all/d/v6839%202,v6840%202,v6841%202'
        },
        'Meta6.6': {
            'Indicador 6.6.1': '/t/9042/n1/all/n3/all/v/all/p/all/c1499/all/c1500/all/d/v12769%201,v12770%201'
        },
        'Meta6.a': {
            'Indicador 6.a.1': '/t/7145/n1/all/v/all/p/all/c873/all/d/v10284%201'
        },
        'Meta6.b': {
            'Indicador 6.b.1': '/t/9044/n1/all/v/all/p/all/c1/all'
        }
    },
    'Objetivo7': {
        'Meta7.1': {
            'Indicador 7.1.1': '/t/9740/n1/all/n3/all/v/10137/p/all/d/v10137%201',
            'Indicador 7.1.2': '/t/9731/n1/all/n3/all/v/9135/p/all/d/v9135%201'
        },
        'Meta7.2': {
            'Indicador 7.2.1': '/t/6592/n1/all/v/all/p/all/d/v9340%201'
        },
        'Meta7.3': {
            'Indicador 7.3.1': '/t/6593/n1/all/v/all/p/all/d/v9338%203'
        },
        'Meta7.b': {
            'Indicador 7.b.1': '/t/7283/n1/all/v/all/p/all/d/v10527%202'
        }
    },
    'Objetivo8': {
        'Meta8.1': {
            'Indicador 8.1.1': '/t/6601/n1/all/v/all/p/all/d/v9347%201'
        },
        'Meta8.2': {
            'Indicador 8.2.1': '/t/6602/n1/all/v/all/p/all/d/v9348%202'
        },
        'Meta8.3': {
            'Indicador 8.3.1': '/t/9535/n1/all/n3/all/v/8883/p/all/c2/all/d/v8883%201',
            'Indicador 8.3.1.2': '/t/9538/n1/all/n3/all/v/8883/p/all/c12028/all/d/v8883%201',
            'Indicador 8.3.1.3': '/t/9547/n1/all/n3/all/v/8883/p/all/c839/all/d/v8883%201'
        },
        'Meta8.5': {
            'Indicador 8.5.1': '/t/9455/n1/all/n3/all/v/8828/p/all/c2/all/d/v8828%201',
            'Indicador 8.5.1.2': '/t/9456/n1/all/n3/all/v/8828/p/all/c58/all/d/v8828%201',
            'Indicador 8.5.1.3': '/t/9457/n1/all/n3/all/v/8828/p/all/c694/all/d/v8828%201',
            'Indicador 8.5.1.4': '/t/9516/n1/all/n3/all/v/8828/p/all/c839/all/d/v8828%201',
            'Indicador 8.5.2': '/t/9546/n1/all/n3/all/v/10004/p/all/c839/all/d/v10004%201',
            'Indicador 8.5.2.2': '/t/9694/n1/all/n3/all/v/10004/p/all/c2/all/d/v10004%201',
            'Indicador 8.5.2.3': '/t/9717/n1/all/n3/all/v/10004/p/all/c58/all/d/v10004%201'
        },
        'Meta8.6': {
            'Indicador 8.6.1': '/t/9415/n1/all/n3/all/v/8840/p/all/d/v8840%201'
        },
        'Meta8.7': {
            'Indicador 8.7.1': '/t/9785/n1/all/v/9480,9482/p/all/c2/all/d/v9480%201',
            'Indicador 8.7.1.2': '/t/9786/n1/all/v/9480,9482/p/all/c58/all/d/v9480%201'
        },
        'Meta8.10': {
            'Indicador 8.10.1': '/t/6603/n1/all/v/all/p/all/d/v9349%201,v9350%201',
            'Indicador 8.10.2': '/t/7522/n1/all/v/all/p/all/c2/all/d/v10828%201',
            'Indicador 8.10.2.1': '/t/6604/n1/all/v/all/p/all/d/v9501%201'
        }
    },
    'Objetivo9': {
        'Meta9.1': {
            'Indicador 9.1.2': '/t/9041/n1/all/v/all/p/all/c1501/all/c12607/all'
        },
        'Meta9.2': {
            'Indicador 9.2.1': '/t/6587/n1/all/n3/all/v/all/p/all/d/v9312%201',
            'Indicador 9.2.2': '/t/6608/n1/all/n3/all/v/all/p/all/d/v9314%201'
        },
        'Meta9.3': {
            'Indicador 9.3.1': '/t/8262/n1/all/v/all/p/all/c696/all/d/v11905%202',
            'Indicador 9.3.2': '/t/6842/n1/all/v/all/p/all/d/v12580%201'
        },
        'Meta9.4': {
            'Indicador 9.4.1': '/t/6795/n1/all/v/all/p/all/d/v9792%203'
        },
        'Meta9.5': {
            'Indicador 9.5.1': '/t/6610/n1/all/v/all/p/all/d/v9316%202',
            'Indicador 9.5.2': '/t/6611/n1/all/v/all/p/all'
        },
        'Meta9.b': {
            'Indicador 9.b.1': '/t/6609/n1/all/n3/all/v/all/p/all/d/v9315%201'
        },
        'Meta9.c': {
            'Indicador 9.c.1': '/t/7271/n1/all/v/all/p/all/c912/all/d/v10472%202'
        }
    },
    'Objetivo10': {
        'Meta10.1': {
            'Indicador 10.1.1': '/t/4755/n1/all/v/4957,4965/p/all/d/v4957%202,v4965%202'
        },
        'Meta10.2': {
            'Indicador 10.2.1': '/t/4758/n1/all/v/4969,4971/p/all/c2/all/d/v4971%201',
            'Indicador 10.2.2': '/t/4760/n1/all/v/4969,4971/p/all/c58/all/d/v4971%201'
        },
        'Meta10.4': {
            'Indicador 10.4.1': '/t/6614/n1/all/v/all/p/all/d/v9320%201'
        },
        'Meta10.5': {
            'Indicador 10.5.1.a': '/t/7716/n1/all/v/all/p/all/c1020/all/d/v11025%202',
            'Indicador 10.5.1.b': '/t/7717/n1/all/v/all/p/all/c1020/all/d/v11026%202',
            'Indicador 10.5.1.c': '/t/7718/n1/all/v/all/p/all/c1405/all/d/v11027%202',
            'Indicador 10.5.1.d': '/t/7719/n1/all/v/all/p/all/c1405/all/d/v11028%202',
            'Indicador 10.5.1.e': '/t/7732/n1/all/v/all/p/all/c1020/all/d/v11029%202',
            'Indicador 10.5.1.f': '/t/7733/n1/all/v/all/p/all/c1405/all/d/v11030%202',
            'Indicador 10.5.1.g': '/t/7734/n1/all/v/all/p/all/c1405/all/d/v11031%202'
        }
    },
    'Objetivo11': {
        'Meta11.1': {
            'Indicador 11.1.1': '/t/6585/n1/all/n3/all/v/all/p/all/d/v9326%201'
        },
        'Meta11.3': {
            'Indicador 11.3.2': '/t/7520/n1/all/n3/all/v/all/p/all/d/v10823%201'
        },
        'Meta11.4': {
            'Indicador 11.4.1': '/t/7800/n1/all/v/all/p/all/c1124/all/c11227/all/d/v11122%201'
        },
        'Meta11.5': {
            'Indicador 11.5.1': '/t/6689/n1/all/n3/all/v/all/p/all/d/v9619%201',
            'Indicador 11.5.2': '/t/8754/n1/all/v/all/p/all/d/v12581%202'
        },
        'Meta11.6': {
            'Indicador 11.6.1': '/t/8687/n1/all/n2/all/v/all/p/all/d/v6843%202,v6846%202',
            'Indicador 11.6.1.1': '/t/5904/n1/all/n2/all/v/all/p/all/c1425/all/d/v6844%202,v6845%202'
        },
        'Meta11.a': {
            'Indicador 11.a.1': '/t/7459/n1/all/v/all/p/all'
        },
        'Meta11.b': {
            'Indicador 11.b.1': '/t/6749/n1/all/v/all/p/all',
            'Indicador 11.b.2': '/t/6673/n1/all/n3/all/v/all/p/all/d/v9600%201'
        }
    },
    'Objetivo12': {
        'Meta12.1': {
            'Indicador 12.1.1': '/t/6690/n1/all/v/all/p/all'
        },
        'Meta12.4': {
            'Indicador 12.4.1': '/t/6815/n1/all/v/all/p/all'
        },
        'Meta12.5': {
            'Indicador 12.5.1': '/t/8904/n1/all/n2/all/v/all/p/all/d/v9275%202,v9276%202,v9277%202,v9278%202,v9279%202,v9280%202,v9281%202,v9282%202,v12660%202,v12661%202,v12663%202,v12664%202',
        },
        'Meta12.6': {
            'Indicador 12.6.1': '/t/7516/n1/all/n2/all/v/all/p/all/d/v10301%202',
            'Indicador 12.6.1.2': '/t/7517/n1/all/v/all/p/all/c319/all/d/v10301%202',
            'Indicador 12.6.1.3': '/t/7518/n1/all/v/all/p/all/c696/all/d/v10301%202'
        },
        'Meta12.a': {
            'Indicador 12.a.1': '/t/7283/n1/all/v/all/p/all/d/v10527%202'
        }
    },
    'Objetivo13': {
        'Meta13.1': {
            'Indicador 13.1.1': '/t/6689/n1/all/n3/all/v/all/p/all/d/v9619%201',
            'Indicador 13.1.2': '/t/6749/n1/all/v/all/p/all',
            'Indicador 13.1.3': '/t/6673/n1/all/n3/all/v/all/p/all/d/v9600%201'
        },
        'Meta13.2': {
            'Indicador 13.2.2': '/t/8454/n1/all/v/all/p/all/c1340/all'
        }
    },
    'Objetivo14': {
        'Meta14.5': {
            'Indicador 14.5.1': '/t/6688/n1/all/v/all/p/all/d/v6312%201'
        },
        'Meta14.6': {
            'Indicador 14.6.1': '/t/9033/n1/all/v/all/p/all/d/v12736%202'
        },
        'Meta14.b': {
            'Indicador 14.b.1': '/t/8752/n1/all/v/all/p/all/d/v12734%202'
        }
    },
    'Objetivo15': {
        'Meta15.1': {
            'Indicador 15.1.1': '/t/6843/n1/all/v/all/p/all/d/v9971%202',
            'Indicador 15.1.2': '/t/4962/n123/all/n1/all/v/all/p/all/d/v9272%201',
            'Indicador C15.1.c': '/t/6746/n123/1/n1/all/v/all/p/all/d/v9902%201'
        },
        'Meta15.2': {
            'Indicador 15.2.1': '/t/9774/n1/all/v/all/p/all/d/v9454%202,v9455%202,v9456%202,v9457%202,v9458%202'
        },
        'Meta15.4': {
            'Indicador 15.4.1': '/t/6729/n123/1/n1/all/v/all/p/all/d/v9899%201',
            'Indicador 15.4.2': '/t/6744/n1/all/v/all/p/all/d/v10001%202'
        },
        'Meta15.6': {
            'Indicador 15.6.1': '/t/6748/n1/all/v/all/p/all'
        }
    },
    'Objetivo16': {
        'Meta16.1': {
            'Indicador 16.1.1': '/t/6606/n1/all/n3/all/v/all/p/all/d/v9502%202',
            'Indicador 16.1.1.2': '/t/7877/n1/all/n3/all/v/all/p/all/c58/all/d/v9502%202',
            'Indicador 16.1.1.3': '/t/7876/n1/all/n3/all/v/all/p/all/c2/all/c58/all/d/v9502%202',
            'Indicador 16.1.1.4': '/t/7875/n1/all/n3/all/v/all/p/all/c2/all/d/v9502%202'
        },
        'Meta16.1.3': {
            'Indicador 16.1.3': '/t/8022/n1/all/n3/all/v/11392,11393,11394,11396,11397,11398,11399/p/all/c2/all/c1/all/d/v11392%203,v11393%203,v11394%203,v11396%201,v11397%201,v11398%201,v11399%201',
            'Indicador 16.1.3.1': '/t/8023/n1/all/n3/all/v/11392,11393,11394,11396,11397,11398/p/all/c58/all/c1/all/d/v11392%203,v11393%203,v11394%203,v11396%201,v11397%201,v11398%201',
            'Indicador 16.1.3.2': '/t/8024/n1/all/n3/all/v/11392,11393,11394,11396,11397,11398/p/all/c1568/all/c1/all/d/v11392%203,v11393%203,v11394%203,v11396%201,v11397%201,v11398%201',
            'Indicador 16.1.3.3': '/t/8025/n1/all/n3/all/v/11392,11393,11394,11396,11397,11398/p/all/c86/all/c1/all/d/v11392%203,v11393%203,v11394%203,v11396%201,v11397%201,v11398%201',
            'Indicador 16.1.3.4': '/t/8027/n1/all/n3/all/v/11392,11393,11394,11396,11397,11398/p/all/c652/all/c1/all/d/v11392%203,v11393%203,v11394%203,v11396%201,v11397%201,v11398%201'
        },
        'Meta16.6': {
            'Indicador 16.6.1': '/t/6605/n1/all/v/all/p/all/d/v9500%201,v11432%201'
        },
        'Meta16.7': {
            'Indicador 16.7.1': '/t/4710/n1/all/v/all/p/all/c1776/all/c2/all/d/v8980%201',
            'Indicador 16.7.1.1': '/t/4749/n1/all/v/all/p/all/c1776/all/c58/all/d/v8980%201'
        },
        'Meta16.9': {
            'Indicador 16.9.1': '/t/9544/n1/all/n3/all/v/all/p/all/d/v353%201,v373%201'
        },
        'Meta16.10': {
            'Indicador 16.10.2': '/t/6819/n1/all/v/all/p/all'
        }
    },
    'Objetivo17': {
        'Meta17.1': {
            'Indicador 17.1.1': '/t/7223/n1/all/v/all/p/all/d/v10414%201',
            'Indicador 17.1.2': '/t/6595/n1/all/v/all/p/all/d/v9341%201'
        },
        'Meta17.3': {
            'Indicador 17.3.2': '/t/6596/n1/all/v/all/p/all/d/v9342%202'
        },
        'Meta17.4': {
            'Indicador 17.4.1': '/t/6597/n1/all/v/all/p/all/d/v9343%202'
        },
        'Meta17.6': {
            'Indicador 17.6.1': '/t/6816/n1/all/v/all/p/all/c823/all/c1020/all/d/v9817%202'
        },
        'Meta17.8': {
            'Indicador 17.8.1': '/t/4752/n1/all/n2/all/v/2620,5000/p/all/c1/all/c2/all/d/v5000%201'
        }
    }
}

# Lista de colunas
list_colunas: list = {
    'Nível Territorial (Código)': 'CODG_NIV_TER',
    'Nível Territorial': 'DESC_NIV_TER',
    'Brasil e Unidade da Federação (Código)': 'CODG_UND_FED',
    'Brasil e Unidade da Federação': 'DESC_UND_FED',
    'Unidade da Federação e Brasil (Código)': 'CODG_UND_FED',
    'Unidade da Federação e Brasil': 'DESC_UND_FED',
    'Unidade da Federação e Total (Código)': 'CODG_UND_FED',
    'Unidade da Federação e Total': 'DESC_UND_FED',
    'Unidade de Medida (Código)': 'CODG_UND_MED',
    'Unidade de Medida': 'DESC_UND_MED',
    'Brasil (Código)': 'CODG_UND_FED',
    'Brasil': 'DESC_UND_FED',
    'Variável (Código)': 'CODG_VAR',
    'Variável': 'DESC_VAR',
    'Valor': 'VLR_VAR',
    'Ano (Código)': 'CODG_ANO',
    'Ano': 'DESC_ANO',
    'Grupo de idade': 'DESC_IDADE',
    'Sexo (Código)': 'CODG_SEXO',
    'Sexo': 'DESC_SEXO',
    'Sexo da pessoa de referência (Código)': 'CODG_SEXO',
    'Sexo da pessoa de referência': 'DESC_SEXO',
    'Grupo de idade (Código)': 'CODG_IDADE',
    'Situação de segurança alimentar existente no domicílio (Código)': 'CODG_SIT_SEG_ALI_DOM',
    'Situação de segurança alimentar existente no domicílio': 'DESC_SIT_SEG_ALI_DOM',
    'Cor ou raça (Código)': 'CODG_RACA',
    'Cor ou raça': 'DESC_RACA',
    'Tipo de doença (Código)': 'CODG_TIPO_DOENCA',
    'Tipo de doença': 'DESC_TIPO_DOENCA',
    'Biênio (Código)': 'CODG_BIENIO',
    'Biênio': 'DESC_BIENIO',
    'Definição do gasto com com saúde (Código)': 'CODG_DEF_GAST_SAUDE',
    'Definição do gasto com com saúde': 'DESC_DEF_GAST_SAUDE',
    'Grupos de idade e nível de ensino (Código)': 'COD_GRU_IDADE_NIV_ENS',
    'Grupos de idade e nível de ensino': 'DESC_GRU_IDADE_NIV_ENS',
    'Situação do domicílio (Código)': 'CODG_SIT_DOM',
    'Situação do domicílio': 'DESC_SIT_DOM',
    'Brasil e Grande Região (Código)': 'CODG_REGIAO',
    'Brasil e Grande Região': 'DESC_REGIAO',
    'Classes de percentual das pessoas em ordem crescente de rendimento domiciliar per capita (Código)': 'CODG_CLAS_PERC_REND_DOM_PER_CAP',
    'Classes de percentual das pessoas em ordem crescente de rendimento domiciliar per capita': 'DESC_CLAS_PERC_REND_DOM_PER_CAP',
    'Infraestrutura das escolas (Código)': 'CODG_INF_ESC',
    'Infraestrutura das escolas': 'DESC_INF_ESC',
    'Grupamento de atividade no trabalho principal (Código)': 'CODG_GRUP_ATIV_TRAB',
    'Grupamento de atividade no trabalho principal': 'DESC_GRUP_ATIV_TRAB',
    'Atividade do trabalho principal (Código)': 'CODG_ATV_TRAB',
    'Atividade do trabalho principal': 'DESC_ATV_TRAB',
    'Existência de deficiência (Código)': 'CODG_DEF',
    'Existência de deficiência': 'DESC_DEF',
    'Grupamento ocupacional no trabalho principal - PNADC (Código)': 'CODG_GRUP_OCUP_TRAB_PNAD',
    'Grupamento ocupacional no trabalho principal - PNADC': 'DESC_GRUP_OCUP_TRAB_PNAD',
    'Tipo de Movimentação (Código)': 'CODG_TIP_MOV',
    'Tipo de Movimentação': 'DESC_TIP_MOV',
    'Tipo de meio de transporte (Código)': 'CODG_TIP_MEIO_TRANSP',
    'Tipo de meio de transporte': 'DESC_TIP_MEIO_TRANSP',
    'Atividades da indústria, do setor de eletricidade e gás e dos serviços selecionados (Código)': 'CODG_ATV_IND_SET_IND',
    'Atividades da indústria, do setor de eletricidade e gás e dos serviços selecionados': 'DESC_ATV_IND_SET_IND',
    'Tipo de cobertura da telefonia móvel (Código)': 'CODG_TIP_COB_TEF_MOV',
    'Tipo de cobertura da telefonia móvel': 'DESC_TIP_COB_TEF_MOV',
    'Meses do ano (Código)': 'CODG_MES_ANO',
    'Meses do ano': 'DESC_MES_ANO',
    'Trimestres do ano (Código)': 'CODG_TRI_ANO',
    'Trimestres do ano': 'DESC_TRI_ANO',
    'Sexênio (Código)': 'CODG_SEXENIO',
    'Sexênio': 'DESC_SEXENIO',
    'Tipo de patrimônio (Código)': 'CODG_TIP_PATR',
    'Tipo de patrimônio': 'DESC_TIP_PATR',
    'Nível de governo (Código)': 'CODG_NIV_GOV',
    'Nível de governo': 'DESC_NIV_GOV',
    'Disposição final (Código)': 'CODG_DISP_FINAL',
    'Disposição final': 'DESC_DISP_FINAL',
    'Triênio (Código)': 'CODG_TRIENIO',
    'Triênio': 'DESC_TRIENIO',
    'Faixas de pessoal ocupado (Código)': 'CODG_FAI_PESS_OCUP',
    'Faixas de pessoal ocupado': 'DESC_FAI_PESS_OCUP',
    'Fonte de emissão de gases de efeito estufa (Código)': 'CODG_FONT_EMIS_GAS_EFEITO_EST',
    'Fonte de emissão de gases de efeito estufa': 'DESC_FONT_EMIS_GAS_EFEITO_EST',
    'Bioma e Brasil (Código)': 'CODG_BIOMA',
    'Bioma e Brasil': 'DESC_BIOMA',
    'Classificação de montanha (Kapos) (Código)': 'CODG_KAPOS',
    'Classificação de montanha (Kapos)': 'DESC_KAPOS',
    'Nível de instrução (Código)': 'CODG_NIV_INSTR',
    'Nível de instrução': 'DESC_NIV_INSTR',
    'Etapa de ensino (Código)': 'CODG_ETAPA_ENS',
    'Etapa de ensino': 'DESC_ETAPA_ENS',
    'Rendimento mensal domiciliar per capita (Código)': 'CODG_REND_MENSAL_DOM_PER_CAP',
    'Rendimento mensal domiciliar per capita': 'DESC_REND_MENSAL_DOM_PER_CAP',
    'Nível na instituição pública (Código)': 'CODG_NIV_INST_PUBL',
    'Nível na instituição pública': 'DESC_NIV_INST_PUBL',
    'Velocidade de ligação (Código)': 'CODG_VEL_LIGACAO',
    'Velocidade de ligação': 'DESC_VEL_LIGACAO',
    'Região Hidrográfica e Brasil (Código)': 'CODG_REG_HIDR',
    'Região Hidrográfica e Brasil': 'DESC_REG_HIDR',
    'Setor de atividade (Código)': 'CODG_SET_ATIV',
    'Setor de atividade': 'DESC_SET_ATIV',
    'Ecossistema relacionado à água (Código)': 'CODG_ECO_REL_AGUA',
    'Ecossistema relacionado à água': 'DESC_ECO_REL_AGUA',
    'Tipo de dinâmica do ecossistema relacionada à agua (Código)': 'CODG_TIP_DIN_ECO_REL_AGUA',
    'Tipo de dinâmica do ecossistema relacionada à agua': 'DESC_TIP_DIN_ECO_REL_AGUA',
    'Tipo de desembolso bruto de ajuda oficial (Código)': 'CODG_TIP_DESB_BRUTO_AJUDA_OFICIAL',
    'Tipo de desembolso bruto de ajuda oficial': 'DESC_TIP_DESB_BRUTO_AJUDA_OFICIAL'
}

LIST_COL_PADRAO: list = {'CODG_UND_MED', 'CODG_UND_FED', 'CODG_VAR', 'VLR_VAR', 'CODG_ANO'}

df_und_med = pd.DataFrame(columns=['CODG_UND_MED', 'DESC_UND_MED'])
df_variavel = pd.DataFrame(columns=['CODG_VAR', 'DESC_VAR'])
df_filtro = pd.DataFrame(columns=['CODG_VAR', 'DESC_VAR'])

for objetivo in list_indicadores.keys():
    workbook = openpyxl.Workbook()
    workbook.remove(workbook.active)
    for meta in list_indicadores[objetivo].keys():
        for indicador in list_indicadores[objetivo][meta].keys():
            link = URL_BASE + str(list_indicadores[objetivo][meta].get(indicador))
            try:
                df_temp = pd.DataFrame(get_sidra_data(link))
                df_temp.columns = df_temp.iloc[0]
                df_temp = df_temp[1:]
                df_temp = df_temp.rename(columns=list_colunas)
                df_temp.insert(0, 'ID_INDICADOR', f'Indicador {indicador.split("Indicador")[1]}')
                df_und_med = pd.concat([df_und_med, df_temp[['CODG_UND_MED', 'DESC_UND_MED']]])
                df_filtro = pd.concat([df_filtro, df_temp[['CODG_VAR', 'DESC_VAR']]])
                try:
                    df_temp = df_temp.drop(
                        columns=['CODG_NIV_TER', 'DESC_NIV_TER', 'DESC_UND_MED', 'DESC_VAR', 'DESC_ANO'])
                except KeyError as e:
                    print(f'Erro ao remover colunas do indicador: {indicador}')
                list_var: list = list(df_temp['CODG_VAR'].value_counts().to_dict().keys())
                if len(list_var) > 1:
                    print(indicador)
                    df_combined = pd.DataFrame()
                    for cod_var in list_var:
                        df_temp_var = df_temp[df_temp['CODG_VAR'] == cod_var].copy()
                        df_temp_var['SUB_INDICADOR'] = cod_var
                        df_combined = pd.concat([df_combined, df_temp_var], ignore_index=True)
                    workbook = df_to_excel(df_combined, workbook, indicador, header=True)
                else:
                    workbook = df_to_excel(df_temp, workbook, indicador, header=True)
                try:
                    df_other_columns = df_temp.drop(columns=LIST_COL_PADRAO)
                except KeyError as e:
                    print(f'Erro ao remover colunas do indicador: {indicador}')
                if len(df_other_columns.columns) > 1:
                    for coluna in df_other_columns:
                        if 'CODG' in coluna:
                            df_other_columns['TIPO_CAMPO'] = coluna
            except json.decoder.JSONDecodeError as e:
                print(f'Erro ao processar o arquivo {indicador}.csv: {e}')

        print(f'Planilha {indicador}.csv criada.')
        objetivo_xlx = str(Path(__file__).parent) + f'/db/resultados/{objetivo}.xlsx'
        workbook.save(objetivo_xlx)

        df_und_med.to_csv(str(Path(__file__).parent) + f'/db/unidade_medida.csv', index=False)
        # df_filtro.columns = ['id_filt', 'desc_filt']
        df_filtro.to_csv(str(Path(__file__).parent) + f'/db/filtro.csv', index=False)
    print(f'{objetivo} finalizado!')
