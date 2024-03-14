import csv
import numpy as np
import statistics
import matplotlib.pyplot as plt

common_list_of_means = []  #wspolna lista srednich, jesli wiecej niz 1 grupa w kolumnie. jesli tylko 1 grupa w kolumnie to i tak wartosci laduja tutaj

def load_data(csv_file):
    # load glomax data file
    ldata = []
    with open(csv_file, 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            ldata.append(row)
    return ldata

def load_sampleid(txt_file):
    # load txt file with IDs of samples
    file = open(txt_file).readlines()
    sample_id_list = []
    for id in file:
        sample_id_list.append(id.rstrip('\n'))
    return sample_id_list
        
def convert_string_to_float(string):
    # convert strings to float (csv files are loaded as strings)
    read1 = []
    read2 = []
    n = 8  # zawsze 8, bo od A do H jest 8 wierszy ;)
    for i in range(10,18):   # (0,n)
        for element in string[i]:
            if element == "X":
                read1.append(0)
            else:
                read1.append(float(element))
                
    for i in range(21,29):  
        for element in string[i]:
            if element == "X":
                read2.append(0)
            else:
                read2.append(float(element))
    return read1, read2

def convert_and_calculate(float_read1, float_read2, x = None, y = None):
    # converts to numpy array, calculate mean
    # convert to numpy array
    a = np.array(float_read1)
    b = np.array(float_read2)
    
    # calculate read1 / read2
    read1_read2 = a / b
    read1_read2.shape = (8,12)
    # wyliczenie sredniej przez stworzenie listy tylko z wartosciami float()
    #i srednia z tej listy (potrzebne zeby pominac NaNy, ktore tworza sie
    #przez dzielenie 0/0 w dzieleniu read1 / read2
    do_sredniej = []
    list_of_means = []
    for column in range(12):
        for number in read1_read2[x:y,column]:   # wykorzystanie numpy [wiersz,columna]
            if number == float(number):  # pomija NaN'y, dodaje do listy tylko liczby
                do_sredniej.append(number)
        if len(do_sredniej) > 1:       # jesli koniec column (zostaja same nany) to nie licz sredniej
            srednia = statistics.mean(do_sredniej)
        else:
            break
        do_sredniej = []  # zresetowanie listy i loop od nowa
        list_of_means.append(srednia)
    return list_of_means

def display_results(common_list_of_means):
    printed_result_of_both = []
    
    for lista in common_list_of_means: # common_list_of_means sklada sie z wielu list (jesli jest wiele grup w jednej kolumnie). 
        printed_result_of_both.append(list(zip(load_sample_id, lista)))

    for result_of_one_list in printed_result_of_both:  # ten loop wybiera pojedyncze listy, ktore nastepnie loopuje zeby wyciagnac sampleID i mean kazdej z probek (kolumn)
        for sampleid, mean in result_of_one_list:
            print(sampleid, mean)

    #matplotlib
    for lista in common_list_of_means:
        plt.xticks(np.arange(12), load_sample_id, rotation = 90)  # opisy osi x
        plt.plot(lista)
    plt.show()
    
        
load_data = load_data('sample33.csv')
load_sample_id = load_sampleid('sampleID.txt')
float_read1, float_read2 = convert_string_to_float(load_data)


# populate common_list_of_means, SOME KIND OF LOOP/LOGIC NEEDED
# first list of means:
make_array_and_calculate = convert_and_calculate(float_read1, float_read2, y = 4)
common_list_of_means.append(make_array_and_calculate)
# second list of mean:
#make_array_and_calculate = convert_and_calculate(float_read1, float_read2, x = -6)
#common_list_of_means.append(make_array_and_calculate)

display_results(common_list_of_means)
    
'''
jesli plytka ma w kolumnach rozne zawartosci, np.
kolumna 1: 4 studzienki komórki PMG
           4 studzienki komórki PMG92b
to wywolujac funkcje convert_and_calculate() oprocz argumentow float_read1, float_read2,
przekazujemy argumenty x i y, oznaczajace poczatek i koniec (zakres wierszy)
(read1_read2[x:y,column])
na przyklad:
    4 pierwsze studzienki komórki PMG:
    convert_and_calculate(float_read1, float_read2, y = 4) -> wiersze 0,1,2,3 (ale zakres do 4), x pozostaje None
    (read1_read2[:4,column])
    4 ostatnie studzienki komórki PMG92b:
    convert_and_calculate(float_read1, float_read2, x = -4)
    (read1_read2[-4:,column])
    
    
x i y jesli nie beda przekazane w funkcji to domyslnie sa rowne None, liczac cala kolumne.

chyba moze to ogarnac jakas funcja if? jesli np n = 2 to wywoluj dwa razy z x i y, jesli nie to
wywoluj tylko raz z cala kolumna.
'''


