import csv
import math
import os
import os.path
import random
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["toolbar"] = "toolmanager"
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.backend_tools import ToolBase, ToolToggleBase
import numpy as np
import seaborn as sn
import  time
from sklearn.linear_model import BayesianRidge
from colorama import init ,Fore, Back, Style
init()


'''Settings per i colori dell'output'''
class bcolors:
    HEADER = Fore.LIGHTYELLOW_EX
    OKBLUE = Fore.BLUE
    OKCYAN = Fore.CYAN
    OKGREEN = Fore.GREEN
    WARNING = Fore.LIGHTYELLOW_EX
    FAIL = Fore.RED
    ENDC = Style.RESET_ALL


def versione(num, giorno):
    print(Back.WHITE + Fore.BLACK + f"Versione {num} --- Del giorno : {giorno}" + Style.RESET_ALL)
    print(Back.LIGHTWHITE_EX + Fore.BLACK + "Di Alberto Bonetti" + Style.RESET_ALL)


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


'''Dividi file csv in anni'''
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


'''Metodo per aprire i file csv'''
def apri_file_csv(nome_file):
    '''Controlla che esiste il file nella cartella locale'''
    if os.path.isfile(nome_file) == True:
        nome_file = str(nome_file)
        #Prendi la targhetta per sapere il nome della variabile
        label = nome_file.removesuffix(".csv")
        print(Back.BLUE + "In apertura di %s" %nome_file + Style.RESET_ALL)
        with open(nome_file, newline='') as file_csv:
            lettore_csv = csv.reader(file_csv, delimiter=',')
            next(lettore_csv, None)
            arr = []
            for row in lettore_csv:
                arr.append(row)
            print(bcolors.OKCYAN + "Dimensionalità del file: %i punti" %len(arr) + bcolors.ENDC)
            giorni = int(len(arr)/24)
            print(bcolors.OKCYAN + "Tradotto in giorni --> circa %i" %giorni + "gg" + bcolors.ENDC)
            print(Back.WHITE + "-" * 100 + Style.RESET_ALL)
            return arr, label
    else:
        print(bcolors.FAIL + "Non sembra esserci alcun file il nome: '%s" %nome_file + "'" +  bcolors.ENDC)
        print(bcolors.WARNING + "Ricorda di inserire il nome completo del file, compreso il '.csv'" + bcolors.ENDC)
        exit()


def confronta_tempi(arr):
    '''Controllo delle dimensioni'''
    flag_err_date, flag_err_dim = False, False
    for i in range(len(arr)):
        try:
            if len(arr[i]) == len(arr[i+1]):
                pass
            else:
                flag_err_dim = True
        except:
            pass
    '''Controllo delle date'''
    for i in range(len(arr)):
        for z in range(len(arr[0])):
            try:
                if arr[i][z][0] == arr[i+1][z][0]:
                    pass
                else:
                    flag_err_date = True
            except:
                pass
    if flag_err_date == True:
        print(bcolors.FAIL + "Errore: Le date non corrispondono" + bcolors.ENDC)
    if flag_err_dim == True:
        print(bcolors.FAIL + "Errore: Dimensioni non rispettate fra i file csv" + bcolors.ENDC)


def confronta_dim(*arr):
    for i in range(len(arr)):
        if (i + 1) < len(arr):
            if len(arr[i]) == len(arr[i+1]):
                pass
            else:
                print(bcolors.FAIL + f"Errore: Dimensionalità non corrisponde"
                                     f"\nDimensioni discordanti --> {len(arr[i])} != {len(arr[i+1])}" + bcolors.ENDC)


def estraiDati(serie):
    colonna = []
    for i in range(len(serie)):
        try:
            if serie[i][1] == '':
                colonna.append(float(0))
            else:
                colonna.append(float(serie[i][1]))
        except:
            colonna.append(float(0))
    return colonna


def estraiGiorni(serie):
    colonna = []
    for i in range(len(serie)):
        colonna.append(str(serie[i][0]))
    return colonna


def confrontaSerieMultiple(serie, labels_dati):

    colonne = []
    date = []
    for i in range(len(serie)):
        colonne.append(estraiDati(serie[i]))
        date.append(estraiGiorni(serie[i]))
    matrice = pd.DataFrame(colonne).transpose()
    matrice_date = pd.DataFrame(date).transpose()
    matrice_date.columns = labels_dati
    matrice.columns = labels_dati
    print(matrice)
    for i in range(len(labels_dati)):
        print(bcolors.HEADER + "#" + str(i + 1) + f" = {labels_dati[i]}" + bcolors.ENDC)
    scelta_num_confronti = int(input(bcolors.HEADER + "Quante serie vuoi inserire? 2 o 3? " +bcolors.ENDC))
    scelta_x1 = str(input(
        bcolors.HEADER + "SETTAGGIO DI X1 --> Inserisci il numero identificativo del set di dati da utilizzare: "
        + bcolors.ENDC))
    scelta_y1 = str(input(
        bcolors.HEADER + "SETTAGGIO DI Y1 --> Inserisci il numero identificativo del set di dati da utilizzare: "
        + bcolors.ENDC))
    scelta_x2 = str(input(
        bcolors.HEADER + "SETTAGGIO DI X2 --> Inserisci il numero identificativo del set di dati da utilizzare: "
        + bcolors.ENDC))
    scelta_y2 = str(input(
        bcolors.HEADER + "SETTAGGIO DI Y2 --> Inserisci il numero identificativo del set di dati da utilizzare: "
        + bcolors.ENDC))
    if scelta_num_confronti == 3:
        scelta_x3 = str(input(
            bcolors.HEADER + "SETTAGGIO DI X3 --> Inserisci il numero identificativo del set di dati da utilizzare: "
            + bcolors.ENDC))
        scelta_y3 = str(input(
            bcolors.HEADER + "SETTAGGIO DI Y3 --> Inserisci il numero identificativo del set di dati da utilizzare: "
            + bcolors.ENDC))
    treshold = float(input(bcolors.HEADER + "Soglia usata per eliminare i punti al di sotto di un certo valore di x: "
                           + bcolors.ENDC))
    if int(scelta_x1)-1 >= 0 and int(scelta_x1)-1 <= len(labels_dati):
        scelta_x1 = int(scelta_x1)-1
    if int(scelta_x2) - 1 >= 0 and int(scelta_x2) - 1 <= len(labels_dati):
        scelta_x2 = int(scelta_x2)-1
    if scelta_num_confronti == 3:
        if int(scelta_x3) - 1 >= 0 and int(scelta_x3) - 1 <= len(labels_dati):
            scelta_x3 = int(scelta_x3)-1
        if int(scelta_y3) - 1 >= 0 and int(scelta_y3) - 1 <= len(labels_dati):
            scelta_y3 = int(scelta_y3) - 1
    if int(scelta_y1)-1 >= 0 and int(scelta_y1)-1 <= len(labels_dati):
        scelta_y1 = int(scelta_y1)-1
    if int(scelta_y2)-1 >= 0 and int(scelta_y2)-1 <= len(labels_dati):
        scelta_y2 = int(scelta_y2)-1

    #Elimina dalla matrice i valori al di sotto del treshold
    indexNames = matrice[matrice[labels_dati[scelta_x1]] <= treshold].index
    matrice.loc[indexNames,labels_dati[scelta_y1]] = np.nan
    indexNames = matrice[matrice[labels_dati[scelta_x2]] <= treshold].index
    matrice.loc[indexNames, labels_dati[scelta_y2]] = np.nan

    for i in range(len(matrice_date.columns)):
        if matrice_date[labels_dati[i]][len(matrice_date[labels_dati[i]]) - 1] is None:
            pass
        else:
            indice_con_maggior_num_date = i
    if scelta_num_confronti == 3:
        indexNames = matrice[matrice[labels_dati[scelta_x3]] <= treshold].index
        matrice.loc[indexNames, labels_dati[scelta_y3]] = np.nan

    x = matrice[labels_dati[scelta_x1]].values.transpose()
    y = matrice[labels_dati[scelta_y1]].values.transpose()
    x2 = matrice[labels_dati[scelta_x2]].values.transpose()
    y2 = matrice[labels_dati[scelta_y2]].values.transpose()
    if scelta_num_confronti == 3:
        x3 = matrice[labels_dati[scelta_x3]].values.transpose()
        y3 = matrice[labels_dati[scelta_y3]].values.transpose()

    righe = 3
    colonne = 4
    fig, graf = plt.subplots(righe, colonne, sharex=True, sharey=True, constrained_layout=True)

    # Illumina il grafico selezionato e creane uno nuovo
    def ispezionaAzione(event):
        # print("Entrato nell'asse: ", event.inaxes)
        event.inaxes.patch.set_facecolor((0.972, 0.772, 0.549))
        event.canvas.draw()
        '''x = event.inaxes.lines[0].get_xdata()
        y = event.inaxes.lines[0].get_ydata()'''
        #TODO: Aggiungere informazioni in questo grafico, tipo la media, la deviazione, etc.
        riferimento_1 = event.inaxes.collections[0]._offsets
        riferimento_2 = event.inaxes.collections[1]._offsets
        # Per ricavare il titolo del grafico
        titolo = str(event.inaxes.title)
        titolo = titolo.split("'")[1]
        # Per le linee della media
        linee = event.inaxes.lines
        # print(y)
        # print(event.inaxes.lines[0].get_xdata())
        x1_temp, y1_temp, x2_temp, y2_temp, x3_temp, y3_temp = [], [], [], [], [], []
        x_linea, y_linea = [],[]
        for i in range(len(riferimento_1)):
            x1_temp.append(riferimento_1[i][0])
            y1_temp.append(riferimento_1[i][1])
        for i in range(len(riferimento_2)):
            x2_temp.append(riferimento_2[i][0])
            y2_temp.append(riferimento_2[i][1])
        fig, zoom_graf = plt.subplots(1, 1, sharex=True, sharey=True)
        zoom_graf.scatter(x1_temp, y1_temp, c='blue',
                          linestyle='None', marker='x', label=labels_dati[scelta_y1],
                          alpha=0.4)
        zoom_graf.scatter(x2_temp, y2_temp, c='red',
                          linestyle='None', marker='x', label=labels_dati[scelta_y2],
                          alpha=0.4)
        for i in range(len(linee)):
            zoom_graf.plot(linee[i].get_xdata(), linee[i].get_ydata())

        zoom_graf.set_title(titolo)
        if scelta_num_confronti == 3:
            riferimento_3 = event.inaxes.collections[2]._offsets
            for i in range(len(riferimento_3)):
                x3_temp.append(riferimento_3[i][0])
                y3_temp.append(riferimento_3[i][1])
            zoom_graf.scatter(x3_temp, y3_temp, c='green',
                              linestyle='None', marker='x', label=labels_dati[scelta_y3],
                              alpha=0.4)
        plt.legend()
        plt.grid()
        plt.show()

    def leave_axes(event):
        #print("Uscito dall'asse: ", event.inaxes)
        event.inaxes.patch.set_facecolor('white')
        event.canvas.draw()

    #Ripristina il colore dopo aver lasciato il grafico
    fig.canvas.mpl_connect('axes_leave_event', leave_axes)

    #Classe per il pulsante custom ispeziona
    class PulsanteIspeziona(ToolToggleBase):
        image = r"ispeziona.png"
        description = 'Seleziona un grafico da isolare'
        default_toggled = False
        def enable(self, event=None):
            print("Pronto")
            self.mouse_clikkato_id = fig.canvas.mpl_connect('button_press_event', ispezionaAzione)
        def disable(self, event=None):
            print("No")
            fig.canvas.mpl_disconnect(self.mouse_clikkato_id)


    # Toolmanager, inserisci il botone
    tm = fig.canvas.manager.toolmanager
    tm.add_tool("ispeziona", PulsanteIspeziona)
    fig.canvas.manager.toolbar.add_tool(tm.get_tool("ispeziona"), "toolgroup")

    start = 0
    delta = int(len(x) / 12) #8784 punti per un anno
    #delta = int(8784/12)

    for i in range(righe):
        for z in range(colonne):
            #try:
            graf[i][z].scatter(x[start:(start + delta)], y[start:(start + delta)], c='blue',
                               linestyle='None', marker='x', label = labels_dati[scelta_y1],
                               alpha=0.4)
            graf[i][z].scatter(x2[start:(start + delta)], y2[start:(start + delta)], c='red',
                               linestyle='None', marker='x', label = labels_dati[scelta_y2],
                               alpha=0.4)
            try:
                graf[i][z].set_title(f'Dal {matrice_date[labels_dati[indice_con_maggior_num_date]][start][5:10]} al'
                                     f' {matrice_date[labels_dati[indice_con_maggior_num_date]][start + delta][5:10]}')
            except:
                graf[i][z].set_title(f'Dal {matrice_date[labels_dati[indice_con_maggior_num_date]][start][5:10]} al'
                                     f' {matrice_date[labels_dati[indice_con_maggior_num_date]][len(matrice_date[labels_dati[indice_con_maggior_num_date]])-1][5:10]}')
            if scelta_num_confronti == 3:
                graf[i][z].scatter(x3[start:(start + delta)], y3[start:(start + delta)], c='green',
                                   linestyle='None', marker='x', label=labels_dati[scelta_y3],
                                   alpha=0.4)

            '''#Riquadri fra y-max e y-min
            y_max_loc = y[start:(start + delta)].max()
            y_min_loc = y[start:(start + delta)].min()
            graf[i][z].fill_between([treshold,x.max()], y_max_loc, y_min_loc, alpha=0.2, color='blue')
            y2_max_loc = y2[start:(start + delta)].max()
            y2_min_loc = y2[start:(start + delta)].min()
            graf[i][z].fill_between([treshold,x.max()], y2_max_loc, y2_min_loc, alpha=0.2, color='red')'''
            print(Back.WHITE + Fore.BLACK + f"Periodo {i + 1,z + 1}:" + Style.RESET_ALL)

            print(Back.WHITE + Fore.BLUE + f'{labels_dati[scelta_y1]}: Deviazione: {np.nanvar(y[start:(start + delta)])} Media: '
                              f'{np.nanmean(y[start:(start + delta)])}' + Style.RESET_ALL)
            print(Back.WHITE + Fore.RED + f'{labels_dati[scelta_y2]}: Deviazione: {np.nanvar(y2[start:(start + delta)])} Media: '
                             f'{np.nanmean(y2[start:(start + delta)])}' + Style.RESET_ALL)
            if scelta_num_confronti == 3:
                print(
                    Back.WHITE + Fore.GREEN + f'Deviazione di {labels_dati[scelta_y3]}: {np.nanvar(y3[start:(start + delta)])}' + Style.RESET_ALL)
            print(f"Delta media {labels_dati[scelta_y1]} - {labels_dati[scelta_y2]} = "
                                            f"{np.nanmean(y[start:(start + delta)]) - np.nanmean(y2[start:(start + delta)])}")
            #Linee della media
            y_media = np.full((len(x),1), np.nanmean(y[start:(start + delta)]))
            graf[i][z].plot(x, y_media, c='blue', label=f'Media di {labels_dati[scelta_y1]}', linestyle='--', alpha= 0.5)
            y2_media = np.full((len(x), 1), np.nanmean(y2[start:(start + delta)]))
            graf[i][z].plot(x, y2_media, c='red', label=f'Media di {labels_dati[scelta_y2]}', linestyle='--', alpha= 0.5)
            if scelta_num_confronti == 3:
                y3_media = np.full((len(x), 1), np.nanmean(y3[start:(start + delta)]))
                graf[i][z].plot(x, y3_media, c='green', label=f'Media di {labels_dati[scelta_y3]}', linestyle='--',
                                alpha=0.5)
                print(
                    Back.WHITE + Fore.GREEN + f'{labels_dati[scelta_y3]}: Deviazione: {np.nanvar(y3[start:(start + delta)])} Media: '
                                 f'{np.nanmean(y3[start:(start + delta)])}' + Style.RESET_ALL)
            #Colora la differenza fra le due medie
            delta_numeri = np.nanmean(y[start:(start + delta)]) - np.nanmean(y2[start:(start + delta)])
            #graf[i][z].text(treshold, delta_numeri/2 + y2[start:(start + delta)].mean(),r'$\Delta = ' + str(delta_numeri))
            if scelta_num_confronti != 3:
                if np.nanmean(y[start:(start + delta)]) >=  np.nanmean(y2[start:(start + delta)]):
                    graf[i][z].fill_between([treshold, matrice[labels_dati[scelta_x1]].max(skipna=True)], np.nanmean(y[start:(start + delta)]),
                                            np.nanmean(y2[start:(start + delta)]), alpha=0.2, color='yellow')
                else:
                    graf[i][z].fill_between([treshold, matrice[labels_dati[scelta_x1]].max(skipna=True)], np.nanmean(y[start:(start + delta)]),
                                            np.nanmean(y2[start:(start + delta)]), alpha=0.2, color='green')
            #Visualizzazzione dei grafici
            #graf[i][z].legend()
            graf[i][z].grid()
            start += delta
            '''except:
                graf[i][z].scatter(x[start:], y[start:], c='blue',
                                   linestyle='None', marker='x', label = labels_dati[scelta_y1],
                                   alpha=0.4)
                graf[i][z].scatter(x2[start:(start + delta)], y2[start:(start + delta)], c='red',
                                   linestyle='None', marker='x', label = labels_dati[scelta_y2],
                                   alpha=0.4)
                if scelta_num_confronti == 3:
                    graf[i][z].scatter(x3[start:(start + delta)], y3[start:(start + delta)], c='green',
                                       linestyle='None', marker='x', label=labels_dati[scelta_y3],
                                       alpha=0.4)
                graf[i][z].set_xlabel(labels_dati[scelta_x1], fontsize=10)
                #Lineee della media
                y_media = np.full((len(x),1), np.nanmean(y[start:].mean()))
                graf[i][z].plot(x, y_media, c='blue', label=f'Media di {labels_dati[scelta_y1]}')
                y2_media = np.full((len(x), 1), np.nanmean(y2[start:].mean()))
                graf[i][z].plot(x, y2_media, c='red', label=f'Mediaa di {labels_dati[scelta_y2]}')
                # Visualizzazzione dei grafici
                graf[i][z].legend()
                graf[i][z].grid()'''
    '''pienoSchermo = plt.get_current_fig_manager()
    pienoSchermo.full_screen_toggle()'''
    #TODO:
    '''if scelta_num_confronti == 3:
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=3, mode="expand", borderaxespad=0.)
    else:
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=2, mode="expand", borderaxespad=0.)'''

    leg = plt.legend()
    plt.show()


# Metodo per creare da due serie dati, una matrice di grafici, suddivisa in n periodi (Lunghezza serie / num_grafici)
def creaMatriceGrafici(serie1,serie2,labels,num_graf):
    x,y = [],[]
    x_data , y_data = [], []
    confronta_dim(serie1,serie2)
    for i in range(len(serie1)):
        x_data.append(serie1[i][0])
        y_data.append(serie2[i][0])
        x_data[i] = x_data[i][:10]
        y_data[i] = y_data[i][:10]
        if serie1[i][1] == '':
            x.append(float())
        else:
            x.append(float(serie1[i][1]))
        if serie2[i][1] == '':
            y.append(float())
        else:
            y.append(float(serie2[i][1]))
    confronta_dim(x,y)
    colore_storico = np.arange(len(x))
    if type(num_graf) == int and num_graf > 0 and num_graf <= 12:
        if num_graf == 1:
            fig, graf = plt.subplots(1, 1, sharex=True, sharey=True)
            im = graf.scatter(x,y, c=colore_storico, cmap='viridis', linestyle='None', label=labels[1], marker='x', alpha=0.4)
            graf.set_xlabel(labels[0], fontsize=15)
            graf.set_ylabel(labels[1], fontsize=15)
            plt.colorbar(im, ax=graf)
            #graf.legend()
            graf.grid()
            plt.show()
        elif num_graf == 2:
            righe = 1
            colonne = 2
            fig, graf = plt.subplots(righe, colonne, sharex=True, sharey=True, constrained_layout=True)
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
        fig, graf = plt.subplots(righe, colonne, sharex=True, sharey=True, constrained_layout=True)
        start = 0
        delta = int(len(x) / num_graf)
        #TOFIX: Quando i grafici sono due questo diventa un problema.
        for i in range(righe):
            for z in range(colonne):
                try:
                    graf[i][z].scatter(x[start:(start + delta)], y[start:(start + delta)], c=np.arange(delta),
                                       linestyle='None', marker='x',
                                       alpha=0.4)
                    graf[i][z].set_title(f'Dal {x_data[start]} al {x_data[start + delta]}')
                    graf[i][z].set_xlabel(labels[0], fontsize=10)
                    graf[i][z].set_ylabel(labels[1], fontsize=10)
                    #graf[i][z].legend()
                    graf[i][z].grid()
                    start += delta
                except:
                    graf[i][z].scatter(x[start:], y[start:], c=np.arange(len(x[start:])),
                                       linestyle='None', marker='x',
                                       alpha=0.4)
                    graf[i][z].set_title(f'Dal {x_data[start]} al {x_data[-1]}')
                    graf[i][z].set_xlabel(labels[0], fontsize=10)
                    graf[i][z].set_ylabel(labels[1], fontsize=10)
                    #graf[i][z].legend()
                    graf[i][z].grid()
        #plt.tight_layout()
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
        fig, graf = plt.subplots(1,2, sharex=True, sharey=True, constrained_layout=True)
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
    #plt.tight_layout()
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
                print(Back.RED + Fore.LIGHTWHITE_EX + "IN FASE DI SVILUPPO ---- NON USARLA" + Style.RESET_ALL)
                giorni_analisi = int(input(bcolors.HEADER + "Inserisci il numero di giorni di analisi: " + bcolors.ENDC))
                #NOTA: Ricorda di commentarlo via se usi un csv di prova
                giorni_analisi = giorni_analisi * 24
                for i in range(len(labels_dati)):
                    print(bcolors.HEADER + "#" + str(i + 1) + f" = {labels_dati[i]}" + bcolors.ENDC)
                scelta_gra_1 = str(input(
                    bcolors.HEADER + "SETTAGGIO DI X --> Inserisci il numero identificativo del set di dati da utilizzare: "
                    + bcolors.ENDC))
                scelta_gra_2 = str(input(
                    bcolors.HEADER + "SETTAGGIO DI Y --> Inserisci il numero identificativo del set di dati da utilizzare: "
                    + bcolors.ENDC))
                if int(scelta_gra_1) - 1 <= len(labels_dati) and int(scelta_gra_1) - 1 >= 0 \
                        and int(scelta_gra_2) - 1 <= len(labels_dati) and int(scelta_gra_2) - 1 >= 0:
                    indice1 = int(int(scelta_gra_1) - 1)
                    indice2 = int(int(scelta_gra_2) - 1)
                    label_tem = []
                    label_tem.append(labels_dati[indice1])
                    label_tem.append(labels_dati[indice2])
                colonne_interessate = [matrice[label_tem[0]], matrice[label_tem[1]]]
                matrice_interessata = pd.DataFrame(colonne_interessate).transpose()
                matrice_interessata.columns = label_tem
                print(matrice_interessata)
                soglia_allarme = int(input(bcolors.HEADER + "Inserisci la percentuale di soglia allarme (ovviamente compresa fra 0 e 100): \n"
                      + bcolors.ENDC))
                soglia_discostamento = int(input(bcolors.HEADER + "Inserisci la soglia di discostamento: \n" + bcolors.ENDC))
                soglia_discostamento = soglia_discostamento * 24
                if soglia_allarme >= 0 and soglia_allarme <=100 and soglia_discostamento >= 0 \
                        and soglia_discostamento < len(matrice_interessata):
                    soglia_allarme = soglia_allarme/100
                    #print(matrice_interessata[label_tem[0]][len(matrice_interessata[label_tem[0]]) - 1])
                    x_fuori, y_fuori = [], []
                    for i in range(len(matrice_interessata[label_tem[0]][-giorni_analisi:])):

                        printProgressBar(i,len(matrice_interessata[label_tem[0]][-giorni_analisi:]),
                                         prefix="Progresso", suffix="Completo", length=50)
                        limite_sup_x = float(matrice_interessata[label_tem[0]][len(matrice_interessata[label_tem[0]]) - 1 - i] + matrice_interessata[label_tem[0]][len(matrice_interessata[label_tem[0]]) - 1 - i] * soglia_allarme)
                        limite_inf_x = float(matrice_interessata[label_tem[0]][len(matrice_interessata[label_tem[0]]) - 1 - i] - matrice_interessata[label_tem[0]][len(matrice_interessata[label_tem[0]]) - 1 - i] * soglia_allarme)
                        condizione_x = matrice_interessata[label_tem[0]][:-giorni_analisi].between(limite_inf_x, limite_sup_x)

                        limite_sup_y = float(matrice_interessata[label_tem[1]][len(matrice_interessata[label_tem[1]]) - 1 - i] + matrice_interessata[label_tem[1]][len(matrice_interessata[label_tem[1]]) - 1 - i] * soglia_allarme)
                        limite_inf_y = float(matrice_interessata[label_tem[1]][len(matrice_interessata[label_tem[1]]) - 1 - i] - matrice_interessata[label_tem[1]][len(matrice_interessata[label_tem[1]]) - 1 - i] * soglia_allarme)
                        condizione_y = matrice_interessata[label_tem[1]][:-giorni_analisi].between(limite_inf_y, limite_sup_y)
                        conteggio = 0
                        #TODO: è da rivedere sta logica
                        for z in range(len(condizione_y)):
                            if condizione_x[z] == False or condizione_y[z] == False:
                                conteggio += 1

                        if conteggio >= len(matrice_interessata[label_tem[0]][-giorni_analisi:]) - soglia_discostamento\
                                and conteggio <= len(matrice_interessata[label_tem[0]][-giorni_analisi:]):
                                #Indicano per quali x ed y non rientrano le x ed y di analisi.
                                x_fuori.append(matrice_interessata[label_tem[0]]
                                               [len(matrice_interessata[label_tem[0]]) - 1 - i])
                                y_fuori.append(matrice_interessata[label_tem[1]]
                                               [len(matrice_interessata[label_tem[1]]) - 1 - i])
                    #Ora devo creare il grafico
                    x_train = matrice_interessata[label_tem[0]][:-giorni_analisi]
                    y_train = matrice_interessata[label_tem[1]][:-giorni_analisi]
                    fig, graf = plt.subplots(1, 2, sharex= True, sharey= True, constrained_layout=True)
                    graf[0].scatter(x_train, y_train, c=np.arange(len(x_train)), linestyle='None',
                                    marker='x', alpha=0.4)
                    graf[0].set_xlabel(label_tem[0], fontsize=15)
                    graf[0].set_ylabel(label_tem[1], fontsize=15)
                    graf[0].grid()
                    graf[0].set_title("Periodo di analisi")
                    graf[1].scatter(x_fuori, y_fuori, c="red", linestyle='None',
                                    marker='x', alpha=0.4)
                    graf[1].set_xlabel(label_tem[0], fontsize=15)
                    graf[1].set_ylabel(label_tem[1], fontsize=15)
                    graf[1].grid()
                    graf[1].set_title(f"Periodo di confronto di {int(giorni_analisi/24)} giorni, disc = "
                                      f"{soglia_discostamento}")
                    #plt.tight_layout()
                    plt.show()
                    #print(indici)
                else:
                    print(bcolors.FAIL + "SOGLIA NON VALIDA!" + bcolors.ENDC)
                #print(deltas)
                pass
            else:
                pass
        else:
            print(bcolors.FAIL + "Nessuna analisi scelta" +  bcolors.ENDC)


'''Inserisci tutti i file .csv presenti nella cartella del programma'''
def autoInserimentoDati():
    nome_files = []
    for file in os.listdir():
        if file[-3:] == "csv":
            nome_files.append(file)
        else:
            pass
    return nome_files


def starter(autoinserimento):
    tipo_metodi = ["Matrice (premi 'm')", "Analizzatore (premi 'a')",
                   "Permutazioni (premi 'p')","Stesse x, diverse y (premi 'z')",
                                              "Divivi file csv in anni (premi 'd')"]
    flag_inserisci_file = 0
    dati = []
    labels_dati = []
    #Inserimento dei file
    if autoinserimento == 1:
        files = autoInserimentoDati()
        print(bcolors.WARNING + str(files) + bcolors.ENDC)
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
            continua = input(bcolors.HEADER + "Vuoi inserire altri files? [Sì - premi 's']  [No - premi 'n']" +
                             bcolors.ENDC + "\n")
            if continua == 's':
                pass
            else:
                flag_inserisci_file = 1
    confronta_tempi(dati)
    #Scelta del metodo
    tipo_metodo = input(bcolors.HEADER + "Che metodo vuoi usare?\n%s\n"  %tipo_metodi + bcolors.ENDC)
    if tipo_metodo == "Matrice" or tipo_metodo == "matrice" or tipo_metodo == 'M' or tipo_metodo == 'm':
        # Crea matrice di grafici
        num_graf = int(input(bcolors.HEADER + "Inserisci numero grafici: " + bcolors.ENDC))
        for i in range(len(labels_dati)):
            print(bcolors.HEADER + "#" + str(i+1) + f" = {labels_dati[i]}" + bcolors.ENDC)
        scelta_gra_1 = str(input(
            bcolors.HEADER + "SETTAGGIO DI X --> Inserisci il numero identificativo del set di dati da utilizzare: "
            + bcolors.ENDC))
        scelta_gra_2 = str(input(
            bcolors.HEADER + "SETTAGGIO DI Y --> Inserisci il numero identificativo del set di dati da utilizzare: "
            + bcolors.ENDC))
        if int(scelta_gra_1)-1 <= len(dati) and int(scelta_gra_1)-1 >=0 \
                and int(scelta_gra_2)-1 <= len(dati) and int(scelta_gra_2)-1 >=0:
            indice1 = int(int(scelta_gra_1) - 1)
            indice2 = int(int(scelta_gra_2) - 1)
            label_tem = []
            label_tem.append(labels_dati[indice1])
            label_tem.append(labels_dati[indice2])
            creaMatriceGrafici(dati[indice1],dati[indice2],label_tem,num_graf)
    elif tipo_metodo == "Analizzatore" or tipo_metodo == "analizzatore" or tipo_metodo == 'A' or tipo_metodo == 'a':
        # Analizza dati
        print(bcolors.HEADER + 'Tipi accettati: ["Correlazione", "Confronta"]' + bcolors.ENDC)
        tipo_analisi = input(str(bcolors.HEADER + "Inserisci che tipo di analisi si vuole fare: " + bcolors.ENDC))
        #TODO: è meglio non scriverlo ma ricavare i metodi disponibili
        analizzaDati(dati, tipo_analisi, labels_dati)
    elif tipo_metodo == "Permutazioni" or tipo_metodo == "permutazioni" or tipo_metodo == 'P' or tipo_metodo == 'p':
        # Crea grafici per ogni permutazione
        num_giorni_analisi = int(input(bcolors.HEADER + "Inserisci il numero di giorni di analisi: "
                                       + bcolors.ENDC))
        creaPermutazioni(dati,labels_dati,num_giorni_analisi)
    elif tipo_metodo == 'z' or tipo_metodo == 'Z':
        confrontaSerieMultiple(dati, labels_dati)
    elif tipo_metodo == 'd' or tipo_metodo == 'D':
        nome_files = autoInserimentoDati()
        for i in range(len(nome_files)):
            print(Back.WHITE + Fore.BLACK + "#" + str(i + 1) + f" - {nome_files[i]}")
        scelta = int(input("Scegli quale file csv estrarre: "))
        if scelta - 1 >= 0 and scelta - 1 <= len(nome_files):
            scelta = scelta - 1
            print(f"Estrazione di {nome_files[scelta]} in corso...")
            a = apri_file_csv(nome_files[scelta])
            dati = a[0]
            targa = a[1]
            dividi_in_anni(dati, targa)
            print(Style.RESET_ALL)
        else:
            print("Numero non valido!")
    else:
        print("Nessun metodo trovato...")
        exit()


if __name__ == "__main__":
    versione("0.0.9", "09/12/2021")
    print("_" * 110)
    print(Back.WHITE + Fore.BLACK + "\n"    
            "#####                                                         ##### \n"
            "#     # #####  ######   ##   #####  ####  #####  ######       #     # #####    ##   ###### #  ####  # \n"
            "#       #    # #       #  #    #   #    # #    # #            #       #    #  #  #  #      # #    # # \n"
            "#       #    # #####  #    #   #   #    # #    # #####        #  #### #    # #    # #####  # #      # \n"
            "#       #####  #      ######   #   #    # #####  #            #     # #####  ###### #      # #      # \n"
            "#     # #   #  #      #    #   #   #    # #   #  #            #     # #   #  #    # #      # #    # # \n"
            " #####  #    # ###### #    #   #    ####  #    # ######        #####  #    # #    # #      #  ####  # ")
    print( Style.RESET_ALL + "_" * 110)
    '''    logo = open("logo.txt", "r")
    for i in logo.readlines():
        print(i)'''
    ''''''
    starter(1)
