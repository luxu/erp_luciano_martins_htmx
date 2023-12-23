import re
from pathlib import Path

import fitz

path = "bb.pdf"
# path = "bb2.pdf"
filename = Path.joinpath(Path.home(), Path("Desktop"), path)
doc = fitz.open(filename)
tabelas = doc[0].get_text().split("Data")[1:]
padrao = r"\b\d{2}/\d{2}\b"
cont = 1
table_lancamentos = None
pontilhado = "-" * 20
lista_contas_parceladas = []
for page in tabelas:
    texts = page.split("\n")
    line = ""
    for text in texts:
        # if 'INSTITUTO' in line:
        #     print(line)
        if "Lançamentos em processamento" in text:
            table_lancamentos = tabelas[-1]
            break
        else:
            if match := re.search(padrao, text):
                line = text
            if "," in text:
                line += text
                # if re.search(padrao, line) and 'PARC' not in line:
                if "PARC" in line:
                    lista_contas_parceladas.append(line)
                else:
                    if re.search(padrao, line):
                        print(f"{line}")
                        cont += 1
                        line = ""
    if table_lancamentos:
        break
if lista_contas_parceladas:
    print(f"{pontilhado} CONTAS PARCELADAS {pontilhado}")
    for parcela in lista_contas_parceladas:
        print(parcela)
if table_lancamentos:
    texts = table_lancamentos.split("\n")
    line = ""
    print(f"{pontilhado} LANÇAMENTOS FUTUROS {pontilhado}")
    for text in texts[3:]:
        if match := re.search(padrao, text):
            line = text
        else:
            line += text
        if "," in text:
            print(line)
            line = ""
