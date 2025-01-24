import matplotlib.pyplot as plt
import numpy as np
from shiny.express import ui, input, render

with ui.sidebar():
    ui.input_slider("n", "N", 0, 100, 20)

ui.page_opts(title='Teste do titulo do Shiny', fillable=True)


@render.plot(alt="A histogram")
def histogram():
    np.random.seed(19680801)
    x = 100 + 15 * np.random.randn(437)
    plt.hist(x, input.n(), density=True)
