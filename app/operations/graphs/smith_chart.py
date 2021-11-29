from skrf import Network
import matplotlib.pyplot as plt
from app.operations.graphs.select import select

def smith_chart(route):
    line = Network(route)

    i = select()
    i[0] != 5 and line.plot_s_smith(m=i[0], n=i[1],  # Only one param
                                    r=1,
                                    chart_type='s',
                                    show_legend=True,
                                    draw_labels=True,
                                    draw_vswr=True)
    i[0] == 5 and line.plot_s_smith(  # All params
        chart_type='s',
        show_legend=True,
        draw_labels=True,
        draw_vswr=True)
    plt.show()


if __name__ == '__main__':
    smith_chart('./input/Line.s2p')