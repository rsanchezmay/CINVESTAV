import numpy as np

################################        Modules             ################################
#   import and read documents
import sys
sys.path.append("C:/Users/lenovo/Desktop/RF_Parametros_corregido")
from app.doc_process.decoder_s2p import decoder_s2p as decode

from app.doc_process.decoder_s2p import params_complex_destructure as fracc

#   export documents
from app.doc_process.doc_out import doc_out

#   graphs
from app.operations.graphs.smith_chart import smith_chart
from app.operations.graphs.polar_graph import polar_graph
from app.operations.graphs.rect_graph import rect_graph



####################################           Proyecto 2          ##################################

def delta_inverse(array):
    delta = array[0][1] * array[1][0] - array[0][0] * array[1][1]
    return delta


z0 = 50

y0 = 1 / z0

lines = []

s11 = []


def s_to_t(params):
    delta = delta_inverse(params)
    i11 = 1 / params[1][0]
    i12 = -params[1][1] / params[1][0]
    i21 = params[0][0] / params[1][0]
    i22 = delta / params[1][0]
    array_params = (
        str(i11),
        str(i12),
        str(i21),
        str(i22)
    )
    return array_params

def main_menu():
    inicio = input(
        "Por favor indique en donde quiere graficar: [1 = Gráfica Cartesiana, 2 = Gráfica polar, 3=Carta de Smith ] ")
    if inicio == '1':
        rect_graph("./output/Calibrado.s2p")
    elif inicio == '2':
        polar_graph("./output/Calibrado.s2p")
    elif inicio == '3':
        smith_chart("./output/Calibrado.s2p")
    else:
        print("*******************************************************************************")
        print("             ¡Volvamos a intentarlo!           ")
        main_menu()

def converter(route_thru, route_line, route_reflect1, route_reflect2):
    list_thru = decode(route_thru)
    list_line = decode(route_line)
    list_w1 = decode(route_reflect1)

    lines.append(f"!Nueva Lista de parametros corregidos \n")
    # lines.append("# frec param1 param2  param3  param4 \n")
    lines.append("# Hz S RI R 50 \n")

    for i in range(len(list_thru)):
        ### thru
        thru_params = fracc(list_thru[i])
        frecs = thru_params[0]
        array_thru_s = (
        [[complex(thru_params[1]), complex(thru_params[2])], [complex(thru_params[3]), complex(thru_params[4])]])
        thru_array_np_s = np.array(
            [[complex(thru_params[1]), complex(thru_params[2])], [complex(thru_params[3]), complex(thru_params[4])]])
        thru_t = s_to_t(array_thru_s)
        thru_matriz_t = np.array([[complex(thru_t[0]), complex(thru_t[1])], [complex(thru_t[2]), complex(thru_t[3])]])
        thru_matriz_inverse_t = np.linalg.inv(thru_matriz_t)  # Calculo de Inversa de Thru

        ###     line
        line_params = fracc(list_line[i])
        array_line_s = (
        [[complex(line_params[1]), complex(line_params[2])], [complex(line_params[3]), complex(line_params[4])]])
        line_t = s_to_t(array_line_s)
        line_matriz_t = np.array([[complex(line_t[0]), complex(line_t[1])], [complex(line_t[2]), complex(line_t[3])]])

        ###     reflect1
        w1_params = fracc(list_w1[i])
        # array_w1_s = ([[complex(w1_params[1]), complex(w1_params[2])], [complex(w1_params[3]), complex(w1_params[4])]])
        w1_matriz_np_s = np.array(
            [[complex(w1_params[1]), complex(w1_params[2])], [complex(w1_params[3]), complex(w1_params[4])]])
        # w1_results =  s_to_t(array_w1_s)
        # w1_matriz = np.array([[complex(w1_results[0]), complex(w1_results[1])], [complex(w1_results[2]), complex(w1_results[3])]])

        ###     Operando
        t = line_matriz_t.dot(thru_matriz_inverse_t)

        result = np.roots([t[1][0], t[1][1] - t[0][0], -t[0][1]])

        if abs(result[0]) > abs(result[1]):
            ac = result[0]
            b = result[1]
        else:
            ac = result[1]
            b = result[0]

        ac_inv = 1 / ac

        det_thru_s = np.linalg.det(thru_array_np_s)  # - determinante de S

        d = -det_thru_s

        g = 1 / thru_array_np_s[1][0]

        e = thru_array_np_s[0][0]

        f = -thru_array_np_s[1][1]

        phi = ((ac * f) - d) / (ac - e)

        beta_alpha = (e - b) / (d - (b * f))

        w1 = w1_matriz_np_s[0][0]

        w2 = w1_matriz_np_s[1][1]

        a1 = np.sqrt(
            ((d - b * f) * (b - w1) * (1 + beta_alpha * w2)) / ((1 - ac_inv * e) * (phi + w2) * (ac_inv * w1 - 1)))

        a_est = (b - w1) / (w1 * ac_inv - 1)

        a2 = -a1

        a1_dif = abs(a_est - a1)

        a2_dif = abs(a_est - a2)

        if a2_dif > a1_dif:

            a = a1

        else:

            a = a2

        c = a / ac

        alpha = (d - b * f) / (a - c * e)

        beta = (e - b) / (a - c * e)

        r22_p22 = (g * (ac - e)) / (ac - b)

        num1 = (r22_p22 * (a - b * c) * (alpha - beta * phi) * (
                    alpha * t[0][1] - beta * t[0][0] + b * beta * t[1][0] - b * alpha * t[1][1]))

        den1 = (c * beta * t[1][1] - c * beta * t[0][1] - a * beta * t[1][0] + a * alpha * t[1][1])

        s11_dut = num1 / den1

        num2 = r22_p22 * (a - b * c) * (alpha - beta * phi) * (
                    c * phi * t[0][1] - c * t[0][0] + a * (t[1][0] - phi * t[1][1]))

        s22_dut = num2 / den1

        num3 = r22_p22 * (a - b * c) * (alpha - beta * phi)

        s21_dut = num3 / den1

        num4_01 = r22_p22 * (a - b * c) * (alpha - beta * phi) * (t[0][0]) - phi * t[0][1] - b * t[1][0] + b * phi * \
                  t[1][1]
        num4_02 = (num4_01 / den1) + s11_dut * s22_dut
        s12_dut = num4_02 / s21_dut

        line = [s11_dut, s21_dut, s12_dut, s22_dut]
        l = np.array([x for x in line])
        real = [x.real for x in l]
        imag = [x.imag for x in l]

        line = []
        lines.append(frecs + " ")
        for k in range(len(real)):
            lines.append(f"\t")
            lines.append(str(real[k]) + " ")
            lines.append(f"\t")
            lines.append(str(imag[k]) + " ")
            lines.append(f"\t")

        lines.append("\n")

    doc_out("./output/Calibrado.s2p", lines)
    print("Archivo de Correcciones Generado en /output/")
    main_menu()
    print("Graficando Archivo Corregido  ...")
    #




if __name__ == '__main__':
    # print("Grafica Original de Valores Medidos")
    # smith_chart("./input/ATF38143_VGS_-0.5V_VDS_3.0V.s2p")
    print("Calibrando ...")
    converter("./input/Thru.s2p", "./input/Line.s2p", "./input/Open_P1.s2p", "./input/Open_P2.s2p")