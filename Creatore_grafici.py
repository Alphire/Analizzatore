import csv
import os
import os.path
from os import listdir
from os.path import isfile, join
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn


#NOTA: Non funziona sulla console windows
'''Settings per i colori dell'output'''
'''class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    '''

'''Dato che non funziona con il terminal'''
class bcolors:
    HEADER = ''
    OKBLUE = ''
    OKCYAN = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''


'''Metodo per aprire i file csv'''
def apri_file_csv(nome_file):
    '''Controlla che esiste il file nella cartella locale'''
    if os.path.isfile(nome_file) == True:
        nome_file = str(nome_file)
        #Prendi la targhetta per sapere il nome della variabile
        label = nome_file.removesuffix(".csv")
        print(bcolors.OKCYAN + "In apertura di %s" %nome_file + bcolors.ENDC)
        with open(nome_file, newline='') as file_csv:
            lettore_csv = csv.reader(file_csv, delimiter=',')
            next(lettore_csv, None)
            arr = []
            for row in lettore_csv:
                arr.append(row)
            print(bcolors.OKBLUE + "Dimensionalità del file: %i punti" %len(arr) + bcolors.ENDC)
            giorni = int(len(arr)/24)
            print(bcolors.OKBLUE + "Tradotto in giorni --> circa %i" %giorni + "gg" + bcolors.ENDC)
            return arr, label
    else:
        print(bcolors.FAIL + "Non sembra esserci alcun file il nome: '%s" %nome_file + "'" +  bcolors.ENDC)
        print(bcolors.WARNING + "Ricorda di inserire il nome completo del file, compreso il '.csv'" + bcolors.ENDC)
        exit()


def confronta_tempi(arr):
    '''Controllo delle dimensioni'''
    for i in range(len(arr)):
        try:
            if len(arr[i]) == len(arr[i+1]):
                pass
            else:
                print(bcolors.FAIL + "Errore: Dimensioni non rispettate fra i file csv" + bcolors.ENDC)
        except:
            pass
    '''Controllo delle date'''
    for i in range(len(arr)):
        for z in range(len(arr[0])):
            try:
                if arr[i][z][0] == arr[i+1][z][0]:
                    pass
                else:
                    print(bcolors.FAIL + "Errore: Le date non corrispondono" + bcolors.ENDC)
            except:
                pass


def confronta_dim(arr1,arr2):
    if len(arr1) == len(arr2):
        pass
    else:
        print(bcolors.FAIL + "Errore: Dimensionalità non corrisponde" + bcolors.ENDC)


def estraiDati(serie):
    colonna = []
    for i in range(len(serie)):
        if serie[i][1] == '':
            colonna.append(float(0))
        else:
            colonna.append(float(serie[i][1]))
    return colonna


# Metodo per creare da due serie dati, una matrice di grafici, suddivisa in n periodi (Lunghezza serie / num_grafici)
def creaMatriceGrafici(serie1,serie2,labels,num_graf):
    x,y = [],[]
    for i in range(len(serie1)):
        if serie1[i][1] == '':
            x.append(float(0))
        elif serie2[i][1] == '':
            y.append(float(0))
        else:
            x.append(float(serie1[i][1]))
            y.append(float(serie2[i][1]))
    confronta_dim(x,y)
    colore_storico = np.arange(len(x))
    if type(num_graf) == int and num_graf > 0 and num_graf <= 12:
        if num_graf == 1:
            fig, graf = plt.subplots(1, 1, sharex=True, sharey=True)
            graf.scatter(x,y, c=colore_storico, cmap='viridis', linestyle='None', label=labels[1], marker='x', alpha=0.4)
            graf.set_xlabel(labels[0], fontsize=15)
            graf.set_ylabel(labels[1], fontsize=15)
            graf.legend()
            graf.grid()
            plt.show()
        elif num_graf == 2:
            righe = 1
            colonne = 2
            fig, graf = plt.subplots(righe, colonne, sharex=True, sharey=True)
            start = 0
            delta = int(len(x)/num_graf)
            for z in range(2):
                graf[z].scatter(x[start:start+delta],y[start:start+delta],c=np.arange(delta), linestyle='None',
                                label='Periodo ' + str(z), marker='x', alpha=0.4)
                graf[z].set_xlabel(labels[0], fontsize=15)
                graf[z].set_ylabel(labels[1], fontsize=15)
                graf[z].legend()
                graf[z].grid()
                start += delta
            plt.show()
        elif num_graf == 4:
            righe = 2
            colonne = 2
        elif num_graf == 6:
            righe = 2
            colonne = 3
        elif num_graf == 8:
            righe = 2
            colonne = 4
        elif num_graf == 10:
            righe = 2
            colonne = 5
        elif num_graf == 11 or num_graf == 12:
            righe = 3
            colonne = 4
        fig, graf = plt.subplots(righe, colonne, sharex=True, sharey=True)
        start = 0
        delta = int(len(x) / num_graf)
        #TOFIX: Quando i grafici sono due questo diventa un problema.
        for i in range(righe):
            for z in range(colonne):
                try:
                    graf[i][z].scatter(x[start:(start + delta)], y[start:(start + delta)], c=np.arange(delta),
                                       linestyle='None', label='Periodo ' + str(i) + ' ' + str(z), marker='x',
                                       alpha=0.4)
                    graf[i][z].set_xlabel(labels[0], fontsize=10)
                    graf[i][z].set_ylabel(labels[1], fontsize=10)
                    graf[i][z].legend()
                    graf[i][z].grid()
                    start += delta
                except:
                    graf[i][z].scatter(x[start:], y[start:], c=np.arange(len(x[start:])),
                                       linestyle='None', label='Periodo ' + str(i) + ' ' + str(z), marker='x',
                                       alpha=0.4)
                    graf[i][z].set_xlabel(labels[0], fontsize=10)
                    graf[i][z].set_ylabel(labels[1], fontsize=10)
                    graf[i][z].legend()
                    graf[i][z].grid()
        plt.tight_layout()
        plt.show()
    else:
        print(
            bcolors.FAIL + "Inserisci un numero valido per la quantità di grafci da visualizzare, il massimo è 12." + bcolors.ENDC)
        print(bcolors.WARNING + "Per quesrtioni grafiche un numero dispari di grafici non è ammesso" + bcolors.ENDC)
        exit()


def creaGrafico2D(x,y, labels_dati, split):
    # Trasformo i giorni in numero di punti dati
    split = int(split * 24)
    #print(bcolors.OKBLUE + "In creazione..." + bcolors.ENDC)
    if type(split) == int and split > 0:
        fig, graf = plt.subplots(1,2, sharex=True, sharey=True)
        graf[0].scatter(x[:-split], y[:-split], c=np.arange(len(x[:-split])), linestyle='None',
                        marker='x', alpha=0.4)
        graf[0].set_xlabel(labels_dati[0], fontsize=15)
        graf[0].set_ylabel(labels_dati[1], fontsize=15)
        graf[0].grid()
        graf[0].set_title("Periodo di analisi")
        graf[1].scatter(x[-split:], y[-split:], c="red", linestyle='None',
                        marker='x', alpha=0.4)
        graf[1].set_xlabel(labels_dati[0], fontsize=15)
        graf[1].set_ylabel(labels_dati[1], fontsize=15)
        graf[1].grid()
        graf[1].set_title("Periodo di confronto di %i giorni" %int(split/24))
    else:
        colore = np.arange(len(x))
        plt.scatter(x,y, c=colore , linestyle='None', marker='x', alpha=0.4, label=labels_dati[1])
        plt.xlabel(labels_dati[0])
        plt.ylabel(labels_dati[1])
        plt.legend()
        plt.grid()
    plt.tight_layout()
    plt.show()


def creaPermutazioni(serie,labels_dati,giorni_analisi):
    if type(giorni_analisi) == int and giorni_analisi > 0:
        colonne = []
        for i in range(len(serie)):
            colonne.append((estraiDati(serie[i])))
        matrice = pd.DataFrame(colonne).transpose()
        matrice.columns = labels_dati
        for i in range(len(labels_dati)):
            z = 1
            try:
                while z + i < len(labels_dati):
                    lab_temp = [labels_dati[i], labels_dati[i+z]]
                    creaGrafico2D(matrice[labels_dati[i]], matrice[labels_dati[i+z]], lab_temp, giorni_analisi)
                    z += 1
            except:
                pass
    else:
        colonne = []
        for i in range(len(serie)):
            colonne.append((estraiDati(serie[i])))
        matrice = pd.DataFrame(colonne).transpose()
        matrice.columns = labels_dati
        for i in range(len(labels_dati)):
            z = 1
            try:
                while z + i < len(labels_dati):
                    lab_temp = [labels_dati[i], labels_dati[i+z]]
                    creaGrafico2D(matrice[labels_dati[i]], matrice[labels_dati[i+z]], lab_temp)
                    z += 1
            except:
                pass
    exit()


def analizzaDati(serie, tipo_analisi, labels_dati):
    tipi_accettati = ["Correlazione", "Confronta"]
    print(bcolors.WARNING + "Tipi di analisi accettati :\n%s" %tipi_accettati + bcolors.ENDC)
    colonne = []
    for i in range(len(serie)):
        colonne.append((estraiDati(serie[i])))
    matrice = pd.DataFrame(colonne).transpose()
    matrice.columns = labels_dati
    print(matrice)
    for i in range(len(tipi_accettati)):
        if tipo_analisi != tipi_accettati[i]:
            pass
        elif tipo_analisi == tipi_accettati[i]:
            print(bcolors.OKBLUE + "Analisi scelta --> %s" %tipi_accettati[i] + bcolors.ENDC)
            #Smista i metodi
            if i == 0: #Ovvero: Correlazione
                correlationMatrix = matrice.corr()
                sn.heatmap(correlationMatrix, annot=True, cmap="viridis")
                plt.show()
            elif i == 1: #Ovvero Confronta
                #TODO: Da fare
                giorni_analisi = input(int(bcolors.HEADER + "Inserisci il numero di giorni di analisi: " + bcolors.ENDC))
                dati_comp = input(int(bcolors.HEADER + "Quali grafici vuoi comparare? Ne puoi sceglierne due: "
                                                       "\n %s" %labels_dati +bcolors.ENDC))
                max_values = []
                min_values = []
                for colonna in matrice:
                    max_values = matrice[colonna].max()
                    min_values = matrice[colonna].min()

                pass
            else:
                pass
        else:
            print(bcolors.WARNING + "Nessuna analisi scelta" +  bcolors.ENDC)


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


def starter(autoinserimento):
    tipo_metodi = ["Matrice", "Analizzatore", "Permutazioni"]
    flag_inserisci_file = 0
    dati = []
    solo_y = []
    labels_dati = []
    if autoinserimento == 1:
        files = autoInserimentoDati()
        print(files)
        for i in range(len(files)):
            a = apri_file_csv(files[i])
            dati.append(a[0])
            labels_dati.append(a[1])
    else:
        print(bcolors.WARNING + "Inserisici per primo il dataset di riferimento (quello comune a tutti)" + bcolors.ENDC)
        while flag_inserisci_file == 0:
            nom_file = input("Nome del file da aprire: ")
            a = apri_file_csv(nom_file)
            dati.append(a[0])
            labels_dati.append(a[1])
            continua = input(bcolors.HEADER + "Vuoi inserire altri files? [Sì - premi 's']  [No - premi 'n']" + bcolors.ENDC + "\n")
            if continua == 's':
                pass
            else:
                flag_inserisci_file = 1
    confronta_tempi(dati)
    tipo_metodo = input("Che metodo vuoi usare?\n%s\n"  %tipo_metodi)
    for i in range(len(tipo_metodi)):
        if tipo_metodo == "Matrice" or tipo_metodo == "matrice":
            # Crea matrice di grafici
            num_graf = int(input(bcolors.HEADER + "Inserisci numero grafici: " + bcolors.ENDC))
            creaMatriceGrafici(dati[0],dati[1],labels_dati,num_graf)
        elif tipo_metodo == "Analizzatore" or tipo_metodo == "analizzatore":
            # Analizza dati
            tipo_analisi = input(str(bcolors.HEADER + "Inserisci che tipo di analisi si vuole fare: " + bcolors.ENDC))
            analizzaDati(dati, tipo_analisi, labels_dati)
        elif tipo_metodo == "Permutazioni" or "permutazioni":
            # Crea grafici per ogni permutazione
            num_giorni_analisi = int(input(bcolors.HEADER + "Inserisci il numero di giorni di analisi: " + bcolors.ENDC))
            creaPermutazioni(dati,labels_dati,num_giorni_analisi)
    else:
        print("Nessun metodo trovato...")
        exit()


if __name__ == "__main__":
    print("_" * 110)
    print("\n"
            "#####                                                         ##### \n"
            "#     # #####  ######   ##   #####  ####  #####  ######       #     # #####    ##   ###### #  ####  # \n"
            "#       #    # #       #  #    #   #    # #    # #            #       #    #  #  #  #      # #    # # \n"
            "#       #    # #####  #    #   #   #    # #    # #####        #  #### #    # #    # #####  # #      # \n"
            "#       #####  #      ######   #   #    # #####  #            #     # #####  ###### #      # #      # \n"
            "#     # #   #  #      #    #   #   #    # #   #  #            #     # #   #  #    # #      # #    # # \n"
            " #####  #    # ###### #    #   #    ####  #    # ######        #####  #    # #    # #      #  ####  # ")
    print("_" * 110)
    starter(1)
