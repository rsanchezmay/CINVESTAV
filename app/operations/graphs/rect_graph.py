from skrf import Network
import matplotlib.pyplot as plt
from app.operations.graphs.select import select

def rect_graph(route):
    line = Network(route)
    i = select()
    i[0] != 5 and line.plot_s_complex(m=i[0],n=i[1]  #   Only one param

        )
    i[0] == 5 and line.plot_s_complex(        #     All params

        )
    plt.show()