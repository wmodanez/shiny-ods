import pandas as pd

from pathlib import Path
from shiny import App, ui, reactive
from shinyswatch import theme

df_objetivo: pd.DataFrame = pd.read_csv(Path(__file__).parent / 'db/objetivos.csv', sep=';')
df_metas: pd.DataFrame = pd.read_csv(Path(__file__).parent / 'db/metas.csv', sep=';')
df_indicadores: pd.DataFrame = pd.read_csv(Path(__file__).parent / 'db/indicadores.csv', sep=';')

app_ui = ui.page_fluid(
    ui.card(
        ui.layout_columns(
            ui.tags.img(src='/img/sgg.png', width="50%", height="100%"),
            ui.tags.img(src='/img/imb720.png', width="50%", height="100%"),
            ui.tags.h1('Instituto Mauro Borges - ODS - Agenda 2030', style="text-align: center;"),
            col_widths=[-1, 3, 2, 6]
        ),
        id='card_top_menu',
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
                            # display='no-display',
                            # spacing=0,
                        ),
                    ) for index, row in df_objetivo.iterrows()
                ],
            ),
            ui.tags.a('Créditos', href='#', style='text-align: left;'),
        open='always',
        ),
        ui.card(
            ui.card_header(ui.tags.h3('Objetivos de Desenvolvimento Sustentável')),
            ui.card_body(ui.tags.p('Os Objetivos de Desenvolvimento Sustentável são \
                            um apelo global à ação para acabar com a pobreza, proteger o meio ambiente \
                            e o clima e garantir que as pessoas, em todos os lugares, possam \
                            desfrutar de paz e de prosperidade. Estes são os objetivos para os \
                            quais as Nações Unidas estão contribuindo a fim de que possamos atingir a \
                            Agenda 2030 no Brasil.'),
                         ui.tags.p('Clique nos ícones ao lado para saber mais sobre cada um dos ODS.'),
                         ui.tags.a('Fonte: ONU Brasil', href='https://brasil.un.org/pt-br/sdgs', target='_blank'),),
            id='card_principal', #style='display: none;',
            full_screen=True,
        ),
        ui.layout_columns(
            ui.output_ui('dynamic_card'),
            ui.card(
                ui.card_header("Column 1 Header"),
                ui.card_body("This is the body of column 1."),
                ui.card_footer("Column 1 Footer"),
                id='card1', style='display: none;',
            ),
            ui.card(
                ui.card_header("Column 2 Header"),
                ui.card_body("This is the body of column 2."),
                ui.card_footer("Column 2 Footer"),
                id='card2', style='display: none;',
            ),
            col_widths=[6, 6]
        ),
    ),
    title="Instituto Mauro Borges - ODS - Agenda 2030",
    theme=theme.zephyr
)

www_dir = Path(__file__).parent / "www"

app_ui.head_content = ui.tags.head(
    ui.tags.link(rel="icon", href='favicon.ico', type="image/x-icon")
)

def server(input, output, session):
    pass


app = App(app_ui, server, static_assets=www_dir)