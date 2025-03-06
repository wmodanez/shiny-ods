import pandas as pd
from pathlib import Path
from shiny import App, ui, render
from shinyswatch import theme
from functools import lru_cache
import asyncio
import aiofiles
import io

@lru_cache(maxsize=1)
def load_objetivos():
    df_objetivo: pd.DataFrame = pd.read_csv(
        Path(__file__).parent / 'db/objetivos.csv', sep=';'
    )
    return df_objetivo


@lru_cache(maxsize=1)
def load_metas():
    df_metas: pd.DataFrame = pd.read_csv(
        Path(__file__).parent / 'db/metas.csv', sep=';'
    )
    return df_metas


@lru_cache(maxsize=1)
def load_indicadores():
    df_indicadores: pd.DataFrame = pd.read_csv(
        Path(__file__).parent / 'db/indicadores.csv', sep=';'
    )
    return df_indicadores


async def load_resultados(indicador_id: str) -> pd.DataFrame:
    try:
        parquet_path = Path(__file__).parent / f'db/resultados/indicador{indicador_id}.parquet'
        
        if not parquet_path.exists():
            print(f"Arquivo não encontrado: {parquet_path}")
            return pd.DataFrame()
        
        # Lê o arquivo Parquet de forma assíncrona
        async with aiofiles.open(parquet_path, 'rb') as f:
            content = await f.read()
            df_resultado = pd.read_parquet(io.BytesIO(content))
        
        # Remove espaços extras dos nomes das colunas
        df_resultado.columns = df_resultado.columns.str.strip()
        
        # Remove espaços extras dos valores
        for col in df_resultado.columns:
            if df_resultado[col].dtype == 'object':
                df_resultado[col] = df_resultado[col].str.strip()
        
        return df_resultado
        
    except Exception as e:
        print(f"Erro ao carregar arquivo Parquet: {e}")
        return pd.DataFrame()


cards = [
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivos de Desenvolvimento Sustentável")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Os Objetivos de Desenvolvimento Sustentável (ODS) são um conjunto de 17 objetivos globais estabelecidos pela Assembleia Geral das Nações Unidas em 2015. Eles visam acabar com a pobreza, proteger o planeta e garantir que todas as pessoas desfrutem de paz e prosperidade até 2030."),
            ),
        ),
        id="card_objetivo0",
        style='display: block; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 1 - Erradicação da Pobreza")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Erradicar a pobreza em todas as suas formas, em todos os lugares"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 1.1",
                        ui.p("Até 2030, erradicar a pobreza extrema para todas as pessoas em todos os lugares, atualmente medida como pessoas vivendo com menos de US$ 1,90 por dia"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 1.1.1",
                                    ui.p("Proporção da população vivendo abaixo da linha de pobreza internacional, por sexo, idade, condição perante o trabalho e localização geográfica (urbano/rural)"),
                                    ui.output_data_frame("indicador_1_1_1"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 1.2",
                        ui.p("Até 2030, reduzir pelo menos à metade a proporção de homens, mulheres e crianças, de todas as idades, que vivem na pobreza, em todas as suas dimensões, de acordo com as definições nacionais"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 1.2.1",
                                    ui.p("Proporção da população vivendo abaixo da linha de pobreza nacional, por sexo, idade, condição perante o trabalho e localização geográfica (urbano/rural)"),
                                    ui.output_data_frame("indicador_1_2_1"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 1.5",
                        ui.p("Até 2030, construir a resiliência dos pobres e daqueles em situação de vulnerabilidade, e reduzir a exposição e vulnerabilidade destes a eventos extremos relacionados com o clima e outros choques e desastres econômicos, sociais e ambientais"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 1.5.1",
                                    ui.p("Número de mortes, pessoas desaparecidas e pessoas diretamente afetadas atribuído a desastres por 100 mil habitantes"),
                                    ui.output_data_frame("indicador_1_5_1"),
                                ),
                                ui.nav_panel(
                                    "Indicador 1.5.4",
                                    ui.p("Proporção de governos locais que adotam e implementam estratégias locais de redução de risco de desastres em linha com as estratégias nacionais de redução de risco de desastres"),
                                    ui.output_data_frame("indicador_1_5_4"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
        id="card_objetivo1",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 2 - Fome Zero")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Acabar com a fome, alcançar a segurança alimentar e melhoria da nutrição e promover a agricultura sustentável"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 2.1",
                        ui.p("Até 2030, acabar com a fome e garantir o acesso de todas as pessoas, em particular os pobres e as pessoas em situações vulneráveis, incluindo crianças, a alimentos seguros, nutritivos e suficientes durante todo o ano"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 2.1.2",
                                    ui.p("Prevalência de insegurança alimentar moderada ou grave, baseada em escala de insegurança alimentar"),
                                    ui.output_data_frame("indicador_2_1_2"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 2.5",
                        ui.p("Até 2020, manter a diversidade genética de sementes, plantas cultivadas, animais de criação e domesticados e suas respectivas espécies selvagens, inclusive por meio de bancos de sementes e plantas diversificados e bem geridos em nível nacional, regional e internacional"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 2.5.1",
                                    ui.p("Número de recursos genéticos vegetais e animais para a alimentação e agricultura, protegidos a médio ou longo prazo em instalações de conservação"),
                                    ui.output_data_frame("indicador_2_5_1"),
                                )
                            )
                        )
                    ),
                )
            ),
        ),
        id="card_objetivo2",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 3 - Saúde e Bem-estar")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Assegurar uma vida saudável e promover o bem-estar para todos, em todas as idades"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 3.1",
                        ui.p("Até 2030, reduzir a taxa de mortalidade materna global para menos de 70 mortes por 100.000 nascidos vivos"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 3.1.1",
                                    ui.p("Razão de mortalidade materna"),
                                    ui.output_data_frame("indicador_3_1_1"),
                                ),
                                ui.nav_panel(
                                    "Indicador 3.1.2",
                                    ui.p("Proporção de nascimentos assistidos por pessoal de saúde qualificado"),
                                    ui.output_data_frame("indicador_3_1_2"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 3.2",
                        ui.p("Até 2030, acabar com as mortes evitáveis de recém-nascidos e crianças menores de 5 anos"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 3.2.1",
                                    ui.p("Taxa de mortalidade em menores de 5 anos"),
                                    ui.output_data_frame("indicador_3_2_1"),
                                ),
                                ui.nav_panel(
                                    "Indicador 3.2.2",
                                    ui.p("Taxa de mortalidade neonatal"),
                                    ui.output_data_frame("indicador_3_2_2"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 3.3",
                        ui.p("Até 2030, acabar com as epidemias de AIDS, tuberculose, malária e doenças tropicais negligenciadas, e combater a hepatite, doenças transmitidas pela água, e outras doenças transmissíveis"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 3.3.2",
                                    ui.p("Incidência de tuberculose por 100.000 habitantes"),
                                    ui.output_data_frame("indicador_3_3_2"),
                                ),
                                ui.nav_panel(
                                    "Indicador 3.3.3",
                                    ui.p("Taxa de incidência da malária por 1.000 habitantes"),
                                    ui.output_data_frame("indicador_3_3_3"),
                                ),
                                ui.nav_panel(
                                    "Indicador 3.3.4",
                                    ui.p("Taxa de incidência da hepatite B por 100 mil habitantes"),
                                    ui.output_data_frame("indicador_3_3_4"),
                                ),
                                ui.nav_panel(
                                    "Indicador 3.3.5",
                                    ui.p("Número de pessoas que necessitam de intervenções contra doenças tropicais negligenciadas (DTN)"),
                                    ui.output_data_frame("indicador_3_3_5"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 3.4",
                        ui.p("Até 2030, reduzir em um terço a mortalidade prematura por doenças não transmissíveis via prevenção e tratamento, e promover a saúde mental e o bem-estar"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 3.4.1",
                                    ui.p("Taxa de mortalidade por doenças do aparelho circulatório, tumores malignos, diabetes mellitus e doenças crônicas respiratórias"),
                                    ui.output_data_frame("indicador_3_4_1"),
                                ),
                                ui.nav_panel(
                                    "Indicador 3.4.2",
                                    ui.p("Taxa de mortalidade por suicídio"),
                                    ui.output_data_frame("indicador_3_4_2"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 3.6",
                        ui.p("Até 2020, reduzir pela metade as mortes e os ferimentos globais por acidentes em estradas"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 3.6.1",
                                    ui.p("Taxa de mortalidade por acidentes de trânsito"),
                                    ui.output_data_frame("indicador_3_6_1"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 3.7",
                        ui.p("Até 2030, garantir o acesso universal aos serviços de saúde sexual e reprodutiva, incluindo o planejamento familiar, informações e educação, bem como a integração da saúde reprodutiva em estratégias e programas nacionais"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 3.7.2",
                                    ui.p("Número de nascidos vivos de mães adolescentes (grupos etários 10-14 e 15-19) por 1.000 mulheres destes grupos etários"),
                                    ui.output_data_frame("indicador_3_7_2"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 3.9",
                        ui.p("Até 2030, reduzir substancialmente o número de mortes e doenças por produtos químicos perigosos, contaminação e poluição do ar e água do solo"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 3.9.2",
                                    ui.p("Taxa de mortalidade atribuída a fontes de água inseguras, saneamento inseguro e falta de higiene"),
                                    ui.output_data_frame("indicador_3_9_2"),
                                ),
                                ui.nav_panel(
                                    "Indicador 3.9.3",
                                    ui.p("Taxa de mortalidade atribuída a intoxicação não intencional"),
                                    ui.output_data_frame("indicador_3_9_3"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 3.a",
                        ui.p("Fortalecer a implementação da Convenção-Quadro para o Controle do Tabaco em todos os países, conforme apropriado"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 3.a.1",
                                    ui.p("Prevalência do consumo atual de tabaco na população de 15 anos ou mais"),
                                    ui.output_data_frame("indicador_3_a_1"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
        id="card_objetivo3",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 4 - Educação de Qualidade")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Assegurar a educação inclusiva e equitativa e de qualidade, e promover oportunidades de aprendizagem ao longo da vida para todos"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 4.1",
                        ui.p("Até 2030, garantir que todas as meninas e meninos completem o ensino primário e secundário gratuito, equitativo e de qualidade"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Indicador 4.1.2",
                                    ui.p("Taxa de conclusão do ensino fundamental e ensino médio"),
                                    ui.output_data_frame("indicador_4_1_2"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 4.2",
                        ui.p("Até 2030, garantir que todos os meninos e meninas tenham acesso a um desenvolvimento de qualidade na primeira infância, cuidados e educação pré-escolar, de modo que eles estejam prontos para o ensino primário"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "4.2.1.2",
                                    ui.p("Proporção das pessoas de 5 anos de idade que frequentam escola de acordo com a situação do domicílio"),
                                    ui.output_data_frame("indicador_4_2_1_2"),
                                ),
                                ui.nav_panel(
                                    "4.2.1.3",
                                    ui.p("Proporção das pessoas de 5 anos de idade que frequentam escola em relação ao sexo"),
                                    ui.output_data_frame("indicador_4_2_1_3"),
                                ),
                                ui.nav_panel(
                                    "4.2.1.4",
                                    ui.p("Proporção das pessoas de 5 anos de idade que frequentam escola, em relação ao percentual das pessoas em ordem crescente de rendimento domiciliar per capita"),
                                    ui.output_data_frame("indicador_4_2_1_4"),
                                ),
                                ui.nav_panel(
                                    "4.2.2",
                                    ui.p("Taxa de participação no ensino organizado (um ano antes da idade oficial de ingresso no ensino fundamental), por sexo"),
                                    ui.output_data_frame("indicador_4_2_2"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 4.5",
                        ui.p("Até 2030, eliminar as disparidades de gênero na educação e garantir a igualdade de acesso a todos os níveis de educação e formação profissional para os mais vulneráveis"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "4.5.1",
                                    ui.p("Índices de paridade (mulher/homem, rural/urbano, 1º/5º quintis de renda e outros como população com deficiência, populações indígenas e populações afetadas por conflitos, à medida que os dados estejam disponíveis) para todos os indicadores nesta lista que possam ser desagregados"),
                                    ui.output_data_frame("indicador_4_5_1"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 4.a",
                        ui.p("Construir e melhorar instalações físicas para educação, apropriadas para crianças e sensíveis às deficiências e ao gênero, e que proporcionem ambientes de aprendizagem seguros e não violentos, inclusivos e eficazes para todos"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "4.a.1",
                                    ui.p("Proporção de escolas com acesso a: (a) eletricidade; (b) internet para fins pedagógicos; (c) computadores para fins pedagógicos; (d) infraestrutura e materiais adaptados para alunos com deficiência; (e) água potável; (f) instalações sanitárias separadas por sexo; e (g) instalações básicas para lavagem das mãos"),
                                    ui.output_data_frame("indicador_4_a_1"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 4.c",
                        ui.p("Até 2030, aumentar substancialmente o contingente de professores qualificados, inclusive por meio da cooperação internacional para a formação de professores, nos países em desenvolvimento, especialmente os países menos desenvolvidos e pequenos Estados insulares em desenvolvimento"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "4.c.1",
                                    ui.p("Proporção de professores que receberam a qualificação mínima exigida, por nível de ensino"),
                                    ui.output_data_frame("indicador_4_c_1"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
        id="card_objetivo4",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 5 - Igualdade de Gênero")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Alcançar a igualdade de gênero e empoderar todas as mulheres e meninas"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 5.4",
                        ui.p("Reconhecer e valorizar o trabalho de assistência e doméstico não remunerado, por meio da disponibilização de serviços públicos, infraestrutura e políticas de proteção social, bem como a promoção da responsabilidade compartilhada dentro do lar e da família, conforme os contextos nacionais"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "5.4.1.2",
                                    ui.p("Percentual de tempo gasto em trabalho doméstico não remunerado e cuidados por sexo e raça"),
                                    ui.output_data_frame("indicador_5_4_1_2"),
                                ),
                                ui.nav_panel(
                                    "5.4.1.3",
                                    ui.p("Percentual de tempo gasto em trabalho doméstico não remunerado e cuidados"),
                                    ui.output_data_frame("indicador_5_4_1_3"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 5.5",
                        ui.p("Garantir a participação plena e efetiva das mulheres e a igualdade de oportunidades para a liderança em todos os níveis de tomada de decisão na vida política, econômica e pública"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "5.5.1",
                                    ui.p("Proporção de assentos ocupados por mulheres em (a) parlamentos nacionais e (b) governos locais"),
                                    ui.output_data_frame("indicador_5_5_1"),
                                ),
                                ui.nav_panel(
                                    "5.5.1.1",
                                    ui.p("Número de assentos ocupados por mulheres na Câmara de Vereadores"),
                                    ui.output_data_frame("indicador_5_5_1_1"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
        id="card_objetivo5",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 6 - Água Potável e Saneamento")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Garantir disponibilidade e manejo sustentável da água e saneamento para todos"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 6.1",
                        ui.p("Até 2030, alcançar o acesso universal e equitativo a água potável e segura para todos"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "6.1.1",
                                    ui.p("Proporção da população que utiliza serviços de água potável gerenciados de forma segura"),
                                    ui.output_data_frame("indicador_6_1_1"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 6.2",
                        ui.p("Até 2030, alcançar o acesso a saneamento e higiene adequados e equitativos para todos, e acabar com a defecação a céu aberto, prestando especial atenção às necessidades das mulheres e meninas e daqueles em situação de vulnerabilidade"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "6.2.1",
                                    ui.p("Proporção da população que utiliza (a) serviços de saneamento gerenciados de forma segura e (b) instalações para lavagem das mãos com água e sabão"),
                                    ui.output_data_frame("indicador_6_2_1"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 6.4",
                        ui.p("Até 2030, aumentar substancialmente a eficiência do uso da água em todos os setores e garantir a retirada e o abastecimento sustentável de água doce para enfrentar a escassez de água, e reduzir substancialmente o número de pessoas que sofrem com a escassez de água"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "6.4.1",
                                    ui.p("Alteração da eficiência no uso da água ao longo do tempo"),
                                    ui.output_data_frame("indicador_6_4_1"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 6.6",
                        ui.p("Até 2020, proteger e restaurar ecossistemas relacionados com a água, incluindo montanhas, florestas, zonas úmidas, rios, aquíferos e lagos"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "6.6.1",
                                    ui.p("Alteração na extensão dos ecossistemas relacionados a água ao longo do tempo"),
                                    ui.output_data_frame("indicador_6_6_1"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
        id="card_objetivo6",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 7 - Energia Acessível e Limpa")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Garantir acesso à energia barata, confiável, sustentável e renovável para todos"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 7.1",
                        ui.p("Até 2030, garantir o acesso universal a serviços de energia modernos, confiáveis e a preços acessíveis"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "7.1.1",
                                    ui.p("Percentagem da população com acesso à eletricidade"),
                                    ui.output_data_frame("indicador_7_1_1"),
                                ),
                                ui.nav_panel(
                                    "7.1.2",
                                    ui.p("Percentagem da população com acesso primário a combustíveis e tecnologias limpos"),
                                    ui.output_data_frame("indicador_7_1_2"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
        id="card_objetivo7",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 8 - Trabalho Decente e Crescimento Econômico")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Promover o crescimento econômico sustentado, inclusivo e sustentável, emprego pleno e produtivo e trabalho decente para todos"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 8.3",
                        ui.p("Promover políticas orientadas para o desenvolvimento que apoiem as atividades produtivas, geração de emprego decente, empreendedorismo, criatividade e inovação, e incentivar a formalização e o crescimento das micro, pequenas e médias empresas, inclusive através do acesso a serviços financeiros"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "8.3.1",
                                    ui.p("Taxa de informalidade das pessoas de 15 anos ou mais de idade ocupadas na semana de referência, por sexo, setor de atividade do trabalho principal e existência de deficiência"),
                                    ui.output_data_frame("indicador_8_3_1"),
                                ),
                                ui.nav_panel(
                                    "8.3.1.2",
                                    ui.p("Taxa de informalidade das pessoas de 15 anos ou mais de idade ocupadas na semana de referência, por atividade principal de trabalho"),
                                    ui.output_data_frame("indicador_8_3_1_2"),
                                ),
                                ui.nav_panel(
                                    "8.3.1.3",
                                    ui.p("Taxa de informalidade das pessoas de 15 anos ou mais de idade ocupadas na semana de referência, por existência de deficiência"),
                                    ui.output_data_frame("indicador_8_3_1_3"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 8.5",
                        ui.p("Até 2030, alcançar o emprego pleno e produtivo e trabalho decente para todas as mulheres e homens, incluindo os jovens e as pessoas com deficiência, e remuneração igual para trabalho de igual valor"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "8.5.1",
                                    ui.p("Rendimento médio por hora real das pessoas de 15 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos, por sexo, grupo de idade, grupamento ocupacional do trabalho principal e existência de deficiência"),
                                    ui.output_data_frame("indicador_8_5_1"),
                                ),
                                ui.nav_panel(
                                    "8.5.1.2",
                                    ui.p("Rendimento médio por hora real das pessoas de 15 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos, por grupo de idade"),
                                    ui.output_data_frame("indicador_8_5_1_2"),
                                ),
                                ui.nav_panel(
                                    "8.5.1.3",
                                    ui.p("Rendimento médio por hora real das pessoas de 15 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos, por grupamento ocupacional no trabalho principal"),
                                    ui.output_data_frame("indicador_8_5_1_3"),
                                ),
                                ui.nav_panel(
                                    "8.5.1.4",
                                    ui.p("Rendimento médio por hora real das pessoas de 15 anos ou mais de idade ocupadas na semana de referência com rendimento de trabalho, habitualmente recebido em todos os trabalhos, por existência de deficiência"),
                                    ui.output_data_frame("indicador_8_5_1_4"),
                                ),
                                ui.nav_panel(
                                    "8.5.2",
                                    ui.p("Taxa de desocupação, por sexo, grupo de idade e existência de deficiência"),
                                    ui.output_data_frame("indicador_8_5_2"),
                                ),
                                ui.nav_panel(
                                    "8.5.2.2",
                                    ui.p("Taxa de desocupação, na semana de referência, das pessoas de 15 anos ou mais de idade, por sexo"),
                                    ui.output_data_frame("indicador_8_5_2_2"),
                                ),
                                ui.nav_panel(
                                    "8.5.2.3",
                                    ui.p("Taxa de desocupação, na semana de referência, das pessoas de 15 anos ou mais de idade, por grupo de idade"),
                                    ui.output_data_frame("indicador_8_5_2_3"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 8.6",
                        ui.p("Até 2020, reduzir substancialmente a proporção de jovens sem emprego, educação ou formação"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "8.6.1",
                                    ui.p("Percentual de pessoas de 15 a 24 anos não ocupadas, não estudantes e que não estão em treinamento para um trabalho"),
                                    ui.output_data_frame("indicador_8_6_1"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
        id="card_objetivo8",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 9 - Indústria, Inovação e Infraestrutura")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Construir infraestruturas resilientes, promover a industrialização inclusiva e sustentável e fomentar a inovação"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 9.2",
                        ui.p("Promover uma industrialização inclusiva e sustentável e, até 2030, aumentar significativamente a participação da indústria no setor de emprego e no PIB, de acordo com as circunstâncias nacionais, e dobrar sua participação nos países menos desenvolvidos"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "9.2.1",
                                    ui.p("Valor adicionado da indústria em proporção do PIB e per capita"),
                                    ui.output_data_frame("indicador_9_2_1"),
                                ),
                                ui.nav_panel(
                                    "9.2.2",
                                    ui.p("Emprego na indústria em proporção do emprego total"),
                                    ui.output_data_frame("indicador_9_2_2"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 9.b",
                        ui.p("Apoiar o desenvolvimento tecnológico, a pesquisa e a inovação nacionais nos países em desenvolvimento, inclusive garantindo um ambiente político propício para, entre outras coisas, diversificação industrial e agregação de valor às commodities"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "9.b.1",
                                    ui.p("Proporção do valor adicionado nas indústrias de média e alta intensidade tecnológica no valor adicionado total"),
                                    ui.output_data_frame("indicador_9_b_1"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
        id="card_objetivo9",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 11 - Cidades e Comunidades Sustentáveis")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Tornar as cidades e os assentamentos humanos inclusivos, seguros, resilientes e sustentáveis"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 11.3",
                        ui.p("Até 2030, aumentar a urbanização inclusiva e sustentável, e as capacidades para o planejamento e gestão de assentamentos humanos participativos, integrados e sustentáveis em todos os países"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "11.3.2",
                                    ui.p("Proporção de cidades com uma estrutura de participação direta da sociedade civil no planejamento e gestão urbana que opera de forma regular e democrática"),
                                    ui.output_data_frame("indicador_11_3_2"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 11.5",
                        ui.p("Até 2030, reduzir significativamente o número de mortes e o número de pessoas afetadas por catástrofes e substancialmente diminuir as perdas econômicas diretas causadas por elas em relação ao produto interno bruto global, incluindo os desastres relacionados à água, com o foco em proteger os pobres e as pessoas em situação de vulnerabilidade"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "11.5.1",
                                    ui.p("Número de mortes, pessoas desaparecidas e pessoas diretamente afetadas atribuído a desastres por 100 mil habitantes"),
                                    ui.output_data_frame("indicador_11_5_1"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 11.b",
                        ui.p("Até 2020, aumentar substancialmente o número de cidades e assentamentos humanos adotando e implementando políticas e planos integrados para a inclusão, a eficiência dos recursos, mitigação e adaptação à mudança do clima, a resiliência a desastres"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "11.b.2",
                                    ui.p("Proporção de governos locais que adotam e implementam estratégias locais de redução de risco de desastres em linha com as estratégias nacionais de redução de risco de desastres"),
                                    ui.output_data_frame("indicador_11_b_2"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
        id="card_objetivo11",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 13 - Ação Contra a Mudança Global do Clima")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Tomar medidas urgentes para combater a mudança climática e seus impactos"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 13.1",
                        ui.p("Fortalecer a resiliência e a capacidade de adaptação a riscos relacionados ao clima e às catástrofes naturais em todos os países"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "13.1.1",
                                    ui.p("Número de mortes, pessoas desaparecidas e pessoas diretamente afetadas atribuído a desastres por 100 mil habitantes"),
                                    ui.output_data_frame("indicador_13_1_1"),
                                ),
                                ui.nav_panel(
                                    "13.1.3",
                                    ui.p("Proporção de governos locais que adotam e implementam estratégias locais de redução de risco de desastres em linha com as estratégias nacionais de redução de risco de desastres"),
                                    ui.output_data_frame("indicador_13_1_3"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 13.2",
                        ui.p("Integrar medidas da mudança do clima nas políticas, estratégias e planejamentos nacionais"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "13.2.2",
                                    ui.p("Emissões de gases do efeito estufa diretos, por fonte de emissão de gases de efeito estufa"),
                                    ui.output_data_frame("indicador_13_2_2"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
        id="card_objetivo13",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 16 - Paz, Justiça e Instituições Eficazes")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Promover sociedades pacíficas e inclusivas para o desenvolvimento sustentável, proporcionar o acesso à justiça para todos e construir instituições eficazes, responsáveis e inclusivas em todos os níveis"),
                ui.tags.h4('Metas'),
                ui.navset_pill(
                    ui.nav_panel(
                        "Meta 16.1",
                        ui.p("Reduzir significativamente todas as formas de violência e as taxas de mortalidade relacionada em todos os lugares"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "16.1.1",
                                    ui.p("Número de vítimas de homicídios intencionais por 100 mil habitantes, por ano"),
                                    ui.output_data_frame("indicador_16_1_1"),
                                ),
                                ui.nav_panel(
                                    "16.1.1.2",
                                    ui.p("Número de vítimas de homicídios intencionais por 100 mil habitantes, por grupo de idade"),
                                    ui.output_data_frame("indicador_16_1_1_2"),
                                ),
                                ui.nav_panel(
                                    "16.1.1.3",
                                    ui.p("Número de vítimas de homicídios intencionais por 100 mil habitantes, por sexo e grupo de idade"),
                                    ui.output_data_frame("indicador_16_1_1_3"),
                                ),
                                ui.nav_panel(
                                    "16.1.1.4",
                                    ui.p("Número de vítimas de homicídios intencionais por 100 mil habitantes, por sexo"),
                                    ui.output_data_frame("indicador_16_1_1_4"),
                                ),
                                ui.nav_panel(
                                    "16.1.3",
                                    ui.p("Pessoas de 18 anos ou mais de idade que sofreram violência nos últimos 12 meses, por sexo e situação de domicílio"),
                                    ui.output_data_frame("indicador_16_1_3"),
                                ),
                                ui.nav_panel(
                                    "16.1.3.1",
                                    ui.p("Pessoas de 18 anos ou mais de idade que sofreram violência nos últimos 12 meses, por grupo de idade e situação de domicílio"),
                                    ui.output_data_frame("indicador_16_1_3_1"),
                                ),
                                ui.nav_panel(
                                    "16.1.3.2",
                                    ui.p("Pessoas de 18 anos ou mais de idade que sofreram violência nos últimos 12 meses, por nível de instrução e situação de domicílio"),
                                    ui.output_data_frame("indicador_16_1_3_2"),
                                ),
                                ui.nav_panel(
                                    "16.1.3.3",
                                    ui.p("Pessoas de 18 anos ou mais de idade que sofreram violência nos últimos 12 meses, por cor ou raça e situação de domicílio"),
                                    ui.output_data_frame("indicador_16_1_3_3"),
                                ),
                                ui.nav_panel(
                                    "16.1.3.4",
                                    ui.p("Pessoas de 18 anos ou mais de idade que sofreram violência nos últimos 12 meses, por rendimento mensal domiciliar per capita e situação de domicílio"),
                                    ui.output_data_frame("indicador_16_1_3_4"),
                                )
                            )
                        )
                    ),
                    ui.nav_panel(
                        "Meta 16.9",
                        ui.p("Até 2030, fornecer identidade legal para todos, incluindo o registro de nascimento"),
                        ui.div(
                            ui.tags.h5('Indicadores'),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "16.9.1",
                                    ui.p("Proporção de crianças com menos de 5 anos cujos nascimentos foram registrados por uma autoridade civil, por idade"),
                                    ui.output_data_frame("indicador_16_9_1"),
                                )
                            )
                        )
                    )
                )
            ),
        ),
        id="card_objetivo16",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 10 - Redução das Desigualdades")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Reduzir a desigualdade dentro dos países e entre eles"),
                ui.tags.h4('Não existem indicadores para esse objetivo.'),
            ),
        ),
        id="card_objetivo10",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 12 - Consumo e Produção Responsáveis")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Assegurar padrões de produção e de consumo sustentáveis"),
                ui.tags.h4('Não existem indicadores para esse objetivo.'),
            ),
        ),
        id="card_objetivo12",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 14 - Vida na Água")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Conservar e promover o uso sustentável dos oceanos, dos mares e dos recursos marinhos para o desenvolvimento sustentável"),
                ui.tags.h4('Não existem indicadores para esse objetivo.'),
            ),
        ),
        id="card_objetivo14",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 15 - Vida Terrestre")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Proteger, recuperar e promover o uso sustentável dos ecossistemas terrestres, gerir de forma sustentável as florestas, combater a desertificação, deter e reverter a degradação da terra e deter a perda de biodiversidade"),
                ui.tags.h4('Não existem indicadores para esse objetivo.'),
            ),
        ),
        id="card_objetivo15",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    ),
    ui.card(
        ui.card_header(
            ui.tags.h3("Objetivo 17 - Parcerias e Meios de Implementação")
        ),
        ui.card_body(
            ui.div(
                ui.tags.p("Fortalecer os meios de implementação e revitalizar a parceria global para o desenvolvimento sustentável"),
                ui.tags.h4('Não existem indicadores para esse objetivo.'),
            ),
        ),
        id="card_objetivo17",
        style='display: none; width: 100%; height: 60vh; margin-top: -15px'
    )
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
            ui.tags.a(ui.input_dark_mode(id="dark_mode", mode="light"), align="right"),
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
                    ) for index, row in load_objetivos().sort_index().iterrows()
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
    @render.data_frame
    async def indicador_1_1_1():
        df = await load_resultados("1.1.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_1_2_1():
        df = await load_resultados("1.2.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_1_5_1():
        df = await load_resultados("1.5.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_1_5_4():
        df = await load_resultados("1.5.4")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_2_1_2():
        df = await load_resultados("2.1.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_3_1_1():
        df = await load_resultados("3.1.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_3_1_2():
        df = await load_resultados("3.1.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_3_2_1():
        df = await load_resultados("3.2.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_3_2_2():
        df = await load_resultados("3.2.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_3_3_2():
        df = await load_resultados("3.3.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_3_3_3():
        df = await load_resultados("3.3.3")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_3_3_4():
        df = await load_resultados("3.3.4")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_3_4_1():
        df = await load_resultados("3.4.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_3_4_2():
        df = await load_resultados("3.4.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_3_6_1():
        df = await load_resultados("3.6.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_4_1_2():
        df = await load_resultados("4.1.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_4_2_1():
        df = await load_resultados("4.2.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_4_2_1_2():
        df = await load_resultados("4.2.1.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_4_2_1_3():
        df = await load_resultados("4.2.1.3")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_4_2_1_4():
        df = await load_resultados("4.2.1.4")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_4_2_2():
        df = await load_resultados("4.2.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_4_5_1():
        df = await load_resultados("4.5.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_5_4_1():
        df = await load_resultados("5.4.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_5_4_1_2():
        df = await load_resultados("5.4.1.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_5_4_1_3():
        df = await load_resultados("5.4.1.3")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_6_1_1():
        df = await load_resultados("6.1.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_6_2_1():
        df = await load_resultados("6.2.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_6_4_1():
        df = await load_resultados("6.4.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_6_6_1():
        df = await load_resultados("6.6.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_7_1_1():
        df = await load_resultados("7.1.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_7_1_2():
        df = await load_resultados("7.1.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_8_3_1():
        df = await load_resultados("8.3.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_8_3_1_2():
        df = await load_resultados("8.3.1.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_8_3_1_3():
        df = await load_resultados("8.3.1.3")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_8_5_1():
        df = await load_resultados("8.5.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_8_5_1_2():
        df = await load_resultados("8.5.1.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_8_5_1_3():
        df = await load_resultados("8.5.1.3")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_8_5_1_4():
        df = await load_resultados("8.5.1.4")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_8_5_2():
        df = await load_resultados("8.5.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_8_5_2_2():
        df = await load_resultados("8.5.2.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_8_5_2_3():
        df = await load_resultados("8.5.2.3")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_8_6_1():
        df = await load_resultados("8.6.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_9_2_1():
        df = await load_resultados("9.2.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_9_2_2():
        df = await load_resultados("9.2.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_9_b_1():
        df = await load_resultados("9.b.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_11_3_2():
        df = await load_resultados("11.3.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_11_5_1():
        df = await load_resultados("11.5.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_11_b_2():
        df = await load_resultados("11.b.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_13_1_1():
        df = await load_resultados("13.1.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_13_1_3():
        df = await load_resultados("13.1.3")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_13_2_2():
        df = await load_resultados("13.2.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_16_1_1():
        df = await load_resultados("16.1.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_16_1_1_2():
        df = await load_resultados("16.1.1.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_16_1_1_3():
        df = await load_resultados("16.1.1.3")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_16_1_1_4():
        df = await load_resultados("16.1.1.4")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_16_1_3():
        df = await load_resultados("16.1.3")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_16_1_3_1():
        df = await load_resultados("16.1.3.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_16_1_3_2():
        df = await load_resultados("16.1.3.2")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_16_1_3_3():
        df = await load_resultados("16.1.3.3")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_16_1_3_4():
        df = await load_resultados("16.1.3.4")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    @render.data_frame
    async def indicador_16_9_1():
        df = await load_resultados("16.9.1")
        if df.empty:
            return render.DataGrid(pd.DataFrame({'Mensagem': ['Nenhum dado disponível para este indicador.']}))
        return render.DataGrid(df)

    # Registrar os outputs
    output.indicador_1_1_1 = indicador_1_1_1
    output.indicador_1_2_1 = indicador_1_2_1
    output.indicador_1_5_1 = indicador_1_5_1
    output.indicador_1_5_4 = indicador_1_5_4
    output.indicador_2_1_2 = indicador_2_1_2
    output.indicador_3_1_1 = indicador_3_1_1
    output.indicador_3_1_2 = indicador_3_1_2
    output.indicador_3_2_1 = indicador_3_2_1
    output.indicador_3_2_2 = indicador_3_2_2
    output.indicador_3_3_2 = indicador_3_3_2
    output.indicador_3_3_3 = indicador_3_3_3
    output.indicador_3_3_4 = indicador_3_3_4
    output.indicador_3_4_1 = indicador_3_4_1
    output.indicador_3_4_2 = indicador_3_4_2
    output.indicador_3_6_1 = indicador_3_6_1
    output.indicador_4_1_2 = indicador_4_1_2
    output.indicador_4_2_1 = indicador_4_2_1
    output.indicador_4_2_1_2 = indicador_4_2_1_2
    output.indicador_4_2_1_3 = indicador_4_2_1_3
    output.indicador_4_2_1_4 = indicador_4_2_1_4
    output.indicador_4_2_2 = indicador_4_2_2
    output.indicador_4_5_1 = indicador_4_5_1
    output.indicador_5_4_1_2 = indicador_5_4_1_2
    output.indicador_5_4_1_3 = indicador_5_4_1_3
    output.indicador_6_1_1 = indicador_6_1_1
    output.indicador_6_2_1 = indicador_6_2_1
    output.indicador_6_4_1 = indicador_6_4_1
    output.indicador_6_6_1 = indicador_6_6_1
    output.indicador_7_1_1 = indicador_7_1_1
    output.indicador_7_1_2 = indicador_7_1_2
    output.indicador_8_3_1 = indicador_8_3_1
    output.indicador_8_3_1_2 = indicador_8_3_1_2
    output.indicador_8_3_1_3 = indicador_8_3_1_3
    output.indicador_8_5_1 = indicador_8_5_1
    output.indicador_8_5_1_2 = indicador_8_5_1_2
    output.indicador_8_5_1_3 = indicador_8_5_1_3
    output.indicador_8_5_1_4 = indicador_8_5_1_4
    output.indicador_8_5_2 = indicador_8_5_2
    output.indicador_8_6_1 = indicador_8_6_1
    output.indicador_9_2_1 = indicador_9_2_1
    output.indicador_9_2_2 = indicador_9_2_2
    output.indicador_9_b_1 = indicador_9_b_1
    output.indicador_11_3_2 = indicador_11_3_2
    output.indicador_11_5_1 = indicador_11_5_1
    output.indicador_11_b_2 = indicador_11_b_2
    output.indicador_13_1_1 = indicador_13_1_1
    output.indicador_13_1_3 = indicador_13_1_3
    output.indicador_13_2_2 = indicador_13_2_2
    output.indicador_16_1_1 = indicador_16_1_1
    output.indicador_16_1_1_2 = indicador_16_1_1_2
    output.indicador_16_1_1_3 = indicador_16_1_1_3
    output.indicador_16_1_1_4 = indicador_16_1_1_4
    output.indicador_16_1_3 = indicador_16_1_3
    output.indicador_16_9_1 = indicador_16_9_1

app = App(app_ui, server, static_assets=www_dir)