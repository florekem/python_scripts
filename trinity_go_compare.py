import csv
from collections import defaultdict 
from collections import Counter

'''
README.md

Sluzy do uzyskania GO i odpowiadajacych mu TRANSCRIPT_ID,TERM, DEFINITION,ONTOLOGY 
na podstawie polaczonych arkuszy z pliku 'go-info.xlsx' na zasadzie:
	- utworzenie oddzielnych list dla goid, definition, ontology, term, transcripts_id
	- wladowanie do nich odpowiednich danych i zzipowanie do jednej listy
	- utorzenie listy hitdata TYLKO z transcript-id na podstawie pliku PBS48+IVF48vsMIM48.xlsx (plik bez GO do zbadania)
	- odwzorowanie listy hitdata na zzipowanych listach z danymi: 
		jesli dany transcipt-id z hitdata pojawil sie w 'go-info.xlsx' (zzipowany plik z danymi)
		jest zapisywany do pliku wynikowego (output_do_zliczenia.csv) wraz z odpowiadajacymi mu danymi (goid, definition, ontology itd...)
	- plik _do_zliczenia jest nastepnie zliczany:
		- utworzenie list, z list utworzenie slownika (key,value na podstawie list)
		- zapisanie do pliku wynikowego key + value rozdzielone @
'''

#uzyskanie pliku wynikowego z 'transcipt-id' wraz z odpowiadajacymi 
#mu danymi (goid, definition, ontology itd...)

def funkcja1(file_name1):
	goid = []
	definition = []
	ontology = []
	term = []
	transcripts_id = []
	transcripts_id_split = []
	
	
	with open(file_name1, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		
		for row in reader:
			data = [str(row['goid']), str(row['definition']), str(row['ontology']), str(row['term']), str(row['transcripts_id'])]
			
			#problem stanowiło tworzenie listy wewnątrz listy (efekt .split), rozwiązaniem było:
			transcripts_id_split = data[4].split(',')	#utworzenie rozerwanych transcripts_id (single_transcript) i przypisanie ich do zmiennej,
														#czyli utworzenie listy w locie,
			
			for single_transcript in transcripts_id_split:	#która jest następnie iterowana i na jej podstawie appendowane pozostałe wartośći.
				transcripts_id.append(single_transcript)	#już do pojedynczych single_transcript, tym samym do każdego single_transript trafia ten sam goid i ontology
				goid.append(data[0])
				definition.append(data[1])
				ontology.append(data[2])
				term.append(data[3])
	
	global zipp
	zipp = list(zip(goid, definition, ontology, term, transcripts_id))		#(j,k,l,m,n) --> 
	
	return zipp


def funkcja2(filename2):
	
	global hitdata
	hitdata = []
	
	with open(filename2, newline='') as csvfile:
		reader2 = csv.DictReader(csvfile)
		
		for row in reader2:
			data2 = [str(row['transcript-id'])]
			hitdata.append(data2[0])
			
			
	return hitdata

def funkcja3():		#FUNKCJE MOGA MIEC WIELE ARGUMENTOW!!! JAK WYKORZYSTAC DRUGI ARGUMENT?
			
	f = open("output_do_zliczenia.csv", "a") #append -> UWAGA kasuj plik wynikowy, bo bedzie do niego dodawac przy ponowynym uruchomieniu skryptu.
	f.write('transcripts_id' + '@' + 'goid' + '@' + 'definition' + '@' + 'ontology' + '@' + 'term' + '\n')			#dodanie naglowkow kolumn
			
	for i in hitdata:			#przeszukuj hitdata
		for j,k,l,m,n in zipp:		#jednoczesnie przeszukuj baze danych
			if i == n:			#jesli transcripts_id z bazy danych bedzie rowny transcript-id z hitdata, zapisz do pliku goid + ontology + term + definition
								#(odpowiedajace danemu transcript_id
				
				f.write(n + '@' + j + '@' + k + '@' + l + '@' + m + '\n')
	


#zliczenie:

def funkcja4(file_name3):
	slownik = {}
	goid = []
	termANDdefinition = []

	with open(file_name3, newline='') as csvfile:
		reader2 = csv.DictReader(csvfile, delimiter = '@')		#delimiter - wskazanie czym byly rozdzielane.
		
		for row in reader2:
			data2 = [str(row['goid']), str(row['term']), str(row['definition']), str(row['ontology'])]
			
			goid.append(data2[0])	#value w slowniku
			termANDdefinition.append(data2[1] + '@' + data2[2] + '@' + data2[3]) #key w slowniku
		
	zipp2 = list(zip(termANDdefinition,goid))	
	
	#print(zipp2)
	
	
	for line in zipp2:					#WAZNE! JAK ROBIC SLOWNIK Z LIST. POWTARZAJACE SIE KLUCZE(KEY) W LISCIE W SLOWNIKU SA JUZ ZGRUPOWANE I TYLKO RAZ
		if line[0] in slownik:			#A WARTOSCI PRZYPISANE POZOSTAJA W JEDNYM KLUCZU
			slownik[line[0]].append(line[1])
		else:
			slownik[line[0]] = [line[1]]
	
	print(slownik)
		
	f = open('output_zliczone.csv', 'w')
		
	for k,v in slownik.items():
		f.write(str(v[0]) + '@' + k + '@' + str(len(v)) + '\n') 		#wyliczenie ile razy jakis GO pojawil sie w danym kluczu
		
	
	#kluczem jest tu termANDdefinition -> polaczone przez @ trzy kolumny (term, definition, ontology)
	#(ktore zawsze sobie odpowiadaja i moga byc uznane za jedna),
	#rozdzielane w calcu, sortowane i gotowe ;)

	
funkcja1('go-info.csv')
funkcja2('PBS48+IVF48vsMIM48_EDITED.csv')

funkcja3()

funkcja4('output_do_zliczenia.csv')

#funkcja5(funkcja4)

	

			
