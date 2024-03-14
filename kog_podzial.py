import csv
from collections import defaultdict 
from collections import Counter

litera = []
kog_number = []
plikcsv = 'kog_base.csv'
plikcsv2 = 'hitdata.txt'
NCBIhits = []
output = []

res = defaultdict(list)

with open(plikcsv, newline='') as csvfile:
	reader = csv.DictReader(csvfile)
	
	for row in reader:
		data = [str(row['litera']), str(row['kog_number'])]
		
		for i in data[0]:				#rozdzielenie 'zbitych' literek na pojedyncze
			litera.append(i)
			kog_number.append(data[1])
		
kog_base_list = list(zip(litera,kog_number))		#lista krotek [X, 123]; baza oznaczeń KOG (do której litery przyporządkowane są numery KOGxxx)

		
#print(zipped)
			
with open(plikcsv2, newline='') as csvfile:
	reader2 = csv.DictReader(csvfile)
	for row in reader2:
		data = [str(row['Accession'])]	
	
		NCBIhits.append(data[0])			#stworzenie z pliku hitdata (zawiera wynik wypluty przez NCBI KOG) listy


for key,value in kog_base_list:					#przeszukiwanie listy kog_base_list względem listy NCBIhits. Jeśli w liście NCBIhits pojawi się 
	for i in NCBIhits:							#dany hit KOGxxx doda do listy odpowiadającą mu literkę
		if i == value:
			output.append(key)
			
output_counted = Counter(output)						#zlicza powtarzające się literki z listy output, tworząc słownik

print(output_counted)

output_counted_summed = sum(output_counted.values())		#suma wartości wszystkich kluczy -> do obliczenia procentowego





kategoria_1 = ['J','A','K','L','B']
suma_kategorii_1 = []

kategoria_2 = ['D','Y','V','T','M','N','Z','W','U','O']
suma_kategorii_2 = []

kategoria_3 = ['C','G','E','F','H','I','P','Q']
suma_kategorii_3 = []

kategoria_4 = ['R','S','X']
suma_kategorii_4 = []


for key,value in output_counted.items():
	for i in kategoria_1:
		if key == i:
			suma_kategorii_1.append(value)
	for i in kategoria_2:
		if key == i:
			suma_kategorii_2.append(value)
	for i in kategoria_3:
		if key == i:
			suma_kategorii_3.append(value)
	for i in kategoria_4:
		if key == i:
			suma_kategorii_4.append(value)


f = open("output.csv", "w")

for key,value in output_counted.items():
	procentowo = value * 100 / output_counted_summed								#wyliczenie procentowe
	out = f.write('%s,%d,%f' % (key, output_counted[key], procentowo) + "\n")		#output zapisany do pliku PRZYKŁAD JAK UZYWAC f.write dla więcej niż jednego argumentu
	
	

f.write(',,,razem: ,' + str(output_counted_summed) + '\n')	
f.write( '\n' + ',,,' + 'INFORMATION STORAGE AND PROCESSING: ,' + str(sum(suma_kategorii_1)))
f.write('\n' + ',,,' + 'CELLULAR PROCESSES AND SIGNALING: ,' + str(sum(suma_kategorii_2)))
f.write('\n' + ',,,' + 'METABOLISM: ,' + str(sum(suma_kategorii_3)))
f.write('\n' + ',,,' + 'POORLY CHARACTERIZED: ,' + str(sum(suma_kategorii_4)))


		





