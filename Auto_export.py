import csv
import os
import os.path
from colorama import init ,Fore, Back, Style
init()


'''Inserisci tutti i file .csv presenti nella cartella del programma'''
def autoInserimentoDati():
    nome_files = []
    for file in os.listdir():
        #print(file[-3:])
        if file[-3:] == "csv":
            nome_files.append(file)
        else:
            pass
    return nome_files


def apri_file_csv(nome_file):
    with open(nome_file, newline='') as file_csv:
        label = nome_file.removesuffix(".csv")
        lettore_csv = csv.reader(file_csv, delimiter=',')
        next(lettore_csv, None)
        arr = []
        for row in lettore_csv:
            arr.append(row)
        return arr, label


def dividi_in_anni(dati, targa):
    divisione_anni = []
    tmp = []
    anno_base = dati[0][0][:4]
    for i in range(len(dati)):
        if dati[i][0][:4] != anno_base:
            divisione_anni.append(tmp)
            tmp = []
            tmp.append(dati[i])
            anno_base = dati[i][0][:4]
        else:
            tmp.append(dati[i])
    for i in range(len(divisione_anni)):
        f = open(targa+f' - {divisione_anni[i][0][0][:4]}.csv', 'w', newline='')
        scrittore = csv.writer(f)
        for z in range(len(divisione_anni[i])):
            if z == 0:
                scrittore.writerow(["Data", "Misura"])
            scrittore.writerow(divisione_anni[i][z])
    f.close()
    print(len(divisione_anni))


if __name__ == "__main__":
    nome_files = autoInserimentoDati()
    for i in range(len(nome_files)):
        print(Back.WHITE + Fore.BLACK + "#" + str(i + 1)  + f" - {nome_files[i]}")
    scelta = int(input("Scegli quale file csv estrarre: "))
    if scelta-1 >= 0 and scelta-1 <= len(nome_files):
        scelta = scelta-1
        print(f"Estrazione di {nome_files[scelta]} in corso...")
        a = apri_file_csv(nome_files[scelta])
        dati = a[0]
        targa = a[1]
        dividi_in_anni(dati, targa)
        print(Style.RESET_ALL)
    else:
        print("Numero non valido!")
