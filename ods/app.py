import pandas as pd

from pathlib import Path
from shiny import App, ui
from shinyswatch import theme

from functools import lru_cache

@lru_cache(maxsize=1)
def load_objetivos():
    df_objetivo: pd.DataFrame = pd.read_csv(Path(__file__).parent / 'db/objetivos.csv', sep=';')
    return df_objetivo

@lru_cache(maxsize=1)
def load_metas():
    df_metas: pd.DataFrame = pd.read_csv(Path(__file__).parent / 'db/metas.csv', sep=';')
    return df_metas

@lru_cache(maxsize=1)
def load_indicadores():
    df_indicadores: pd.DataFrame = pd.read_csv(Path(__file__).parent / 'db/indicadores.csv', sep=';')
    return df_indicadores

def create_tabset_for_objetivo(objetivo_id):
    metas = load_metas()
    indicadores = load_indicadores()
    tabs = []
    for _, meta in metas[metas['ID_OBJETIVO'] == objetivo_id].iterrows():
        meta_id = meta['ID_META']
        indicadores_produzidos = indicadores[(indicadores['ID_META'] == meta_id) & (indicadores['STATUS'] == 'Produzido')]
        if not indicadores_produzidos.empty:
            tab_content = ui.div(
            ui.p(meta['DESC_META']),
            ui.div(
                ui.tags.h5('Indicadores'),
                ui.navset_card_tab(
                *[
                    ui.nav_panel(
                    indicador['ID_INDICADOR'],
                    ui.p(indicador['DESC_INDICADOR'])
                    ) for _, indicador in indicadores_produzidos.iterrows()
                ]
                )
            ),
            )
            tabs.append(ui.nav_panel(meta_id, tab_content))
    return ui.navset_pill(*tabs)

cards = [
    ui.card(
        ui.card_header(ui.tags.h3(row['RES_OBJETIVO'] if row['ID_OBJETIVO'] == 'Objetivo 0' else row['ID_OBJETIVO'] + ' - ' + row['RES_OBJETIVO'])),
        ui.card_body(
            ui.tags.p(row['DESC_OBJETIVO']),
            create_tabset_for_objetivo(row['ID_OBJETIVO'])
        ),
        id=f"card_objetivo{index}",
        style='display: block; width: 100%; height: 60vh; margin-top: -15px' 
            if index == 0 else 'display: none; width: 100%; height: 60vh; margin-top: -15px',
    ) for index, row in load_objetivos().iterrows()
]

app_ui = ui.page_fluid(
    ui.card(
        ui.layout_columns(
            ui.tags.img(src='/img/sgg.png', width="50%", height="100%"),
            ui.tags.img(src='/img/imb720.png', width="50%", height="100%"),
            ui.tags.h1('Instituto Mauro Borges - ODS - Agenda 2030', style="text-align: center;"),
            col_widths=[-1, 3, 2, 6]
        ),
        id='card_top_menu',
        style='margin-top: 15px; margin-right: 15px;',
    ),
    ui.page_sidebar(
        ui.sidebar(      
            ui.tags.a(ui.input_dark_mode(id="dark_mode", mode="light",), align="right"),                      
            ui.layout_columns(
                col_widths=[4, 4, 4],
                *[
                    ui.div(
                        ui.tags.img(
                            src=row['BASE64'],
                            alt=f'objetivo{index}',
                            width="100%",
                            height="100%",
                            style='cursor: pointer;',
                            id=f"objetivo{index}",
                            onclick=f"""
                                document.querySelectorAll('[id^="card_objetivo"]').forEach(card => card.style.display = 'none');
                                document.getElementById('card_objetivo{index}').style.display = 'block';
                            """
                        ),
                    ) for index, row in load_objetivos().iterrows()
                ],
            ),
            ui.tags.a('Créditos', href='#', style='text-align: left;'),            
        open='desktop',
        id='sidebar',
        ),
    *cards,
    ),
    title="Instituto Mauro Borges - ODS - Agenda 2030",
    theme=theme.materia,
)

www_dir = Path(__file__).parent / "www"

app_ui.head_content = ui.tags.head(
    ui.tags.link(rel="icon", href='favicon.ico', type="image/x-icon")
)

def server(input, output, session):
    pass

app = App(app_ui, server, static_assets=www_dir)