#Importando pacotes python. 
import sys #responsável pelo processo em "parallel"
import subprocess #responsável por conectar com ambiente linux
import os #fornece uma interface para interagir com ambiente linux

#Recebe as informações dos ID correspondentes aos SSR, para o "parallel"
input = sys.argv[1]
ssr_file, count = input.split("\t")

# Abrindo o arquivo que contém os SSR preditos.
arquivo = open(ssr_file,'r')

while True:
	linha = arquivo.readline()     #Funcao para ler cada linha do arquivo
	if linha == "":			#Caso encontre linhe vazia, pare o processo.
		break
	linha = linha.replace('\n','') #Substitui tudo que for linha vazia (enter), por nada.	
	coluna = linha.split("\t")      #Dividindo a linha em pedaços com as informações necessárias. 

	#Definindo uma variável para cada divisão feita anteriormente.
	
	ID = coluna[0] #Receberá informação da região do SSR. Por exemplo: scaffold131516_size1187
	size = int(coluna[4]) #Receberá informação do tamanho do SSR. Por exemplo: 12          
	start = int(coluna[5]) #Receberá informação da posição de início do SSR. Por exemplo: 17
	end = int(coluna[6]) #Receberá informação da posição de fim do SSR. Por exemplo: 28

	# Arquivos em formato bed dos indivíduos de H11648/Agave sisalana que serão utilizados no módulo subtract do Bedtools.
	file_beds = [indivíduo1.bed, indivíduo2.bed...]
	
	# Bloco responsável por gerar os arquivos de saída do bedtools subtract para cada indivíduo.
	for bed in file_beds: 
		file_out = bed+"_"+ID+"_"+str(start)+"-"+str(end)+".bed" #Gerando um padrão de nome para os arquivos de saída
		name_ssr = ssr_file+str(count)+".bed" #Gerando o arquivo bed correspondente ao SSR do "parallel". 
		not_used = "not_used"+str(count)+".bed" #Gerando os arquivos que não são úteis para o encontro das regiões de sobreposição.
		used = "used"+str(count)+".bed" #Gerando os arquivos que são úteis para o encontro das regiões de sobreposição.
	
		# Bloco responsável por criar um arquivo temporário com as informações ID, começo e fim do SSR.
		f = open(ssr_file+str(count)+".bed", "w") 
		f.write(ID+"\t"+str(start)+"\t"+str(end))
		f.close()

		# Bloco responsável por gerar os arquivos do Bedtools subtract e os arquivos de saída com as regiões de reads que se sobrepõem nos SSR.
		out = subprocess.run("/usr/bin/bedtools subtract -a "+bed+" -b "+name_ssr+" -A > "+not_used, shell=True, check=True, text=True)
		print(out)
		out = subprocess.run("/usr/bin/bedtools subtract -a "+bed+" -b "+name_ssr+" >"+used, shell=True, check=True, text=True)
		print(out)
		out = subprocess.run("diff "+used+" "+not_used+" > " +file_out, shell=True, text=True)
		print(out)

		if os.stat(file_out).st_size == 0:
		     print("rm "+file_out)
		     subprocess.run("rm "+file_out, shell=True, check=True, text=True)
		

	#break
		
arquivo.close()
