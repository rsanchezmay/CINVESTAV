from skrf import Network
import matplotlib.pyplot as plt
from app.operations.graphs.select import select


def polar_graph(route):
    line = Network(route)
    i = select()
    i[0] != 5 and line.plot_s_polar(m=i[0],n=i[1]  #   Only one param

        )
    i[0] == 5 and line.plot_s_polar(        #     All params

        )
    plt.show()

