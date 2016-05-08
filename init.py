import sys
from ngram import NGram

class Plagiarism:
	def __init__(self,text):
		self.ng=NGram()
		file = open(text,"r")
		linea = file.readline()
		while linea != '':
			if linea != '\n':
				self.ng.add(linea)
			linea = file.readline()
		self.lsn=list(self.ng);
		file.close()

	def verify(self,text_compare):
		results = []
		dictio = []
		file2 = open(text_compare,"r")
		linea2 = file2.readline()
		while linea2 != '':	
			if linea2 != '\n':
				dictio += [self.ng.items_sharing_ngrams(linea2)]
				compares = 0.0
				for parrafo in self.lsn:
					comp = NGram.compare(parrafo,linea2)
					if compares < comp:
						compares = comp
				results += [compares]
			linea2 = file2.readline()
		file2.close()

		major_ocurrences=[]
		for d in dictio:
			major=0
			for val in d.values():
				if major<val:
					major=val
			major_ocurrences+=[major]
			

		avg_perc=0.0
		for r in results:
			avg_perc+=r
		avg_perc=avg_perc/len(results)

		print("Mayor numero de ocurrencias por parrafo del texto copia: "+repr(major_ocurrences))
		print("Porcentaje Similitud: "+repr(avg_perc))

if __name__ == '__main__':
	Plagio=Plagiarism("texto1.txt")
	Plagio.verify("texto2.txt")