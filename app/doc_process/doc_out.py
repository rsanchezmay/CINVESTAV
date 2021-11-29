def doc_out(route, text):
    parametros = []
    archivo = open(route, "wt", encoding="utf8")
    archivo.writelines(text)

    archivo.close()

    return parametros


if __name__ == '__main__':
    doc_out("./output/results.s2p", "yo escribi aqui")
