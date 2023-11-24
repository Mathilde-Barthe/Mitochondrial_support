#! /usr/bin/env python
import argparse
import textwrap
import os
from collections import Counter

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
description=textwrap.dedent('''\
The program convert diploid Fasta file of multiple individuals ( with allele1 followed by the allele2 of an individual) into IUPAC consensus fasta file. 
This script transform lower cases into upper cases, so becarefull if you want to keep the lower case information
Author: Mathilde Barthe
Github: 
''')
)

parser.add_argument('-r', '--read_count', help ="File output from bam-readcount")
parser.add_argument('-d', '--diagnostic_positions', help="List of the diagnostic positions (DP) with the tab separated format 'position \\t nucleotide \\t species'")
parser.add_argument('-i', '--ID', help = "The name of the individuals")
parser.add_argument('-o', '--output', help ="Name of the output file")  


args = parser.parse_args()
read_count_file = str(args.read_count)
dp_file = str(args.diagnostic_positions)
ID = str(args.ID)
out_file = str(args.output)



#####################################################
# Lineages matching
#####################################################
dp = open(dp_file)

lineage_dict = {}
for line in dp:
        line_field=line.split('\t')
        value = (line_field[2].replace('\n', ''))
        key = (line_field[0], line_field[1])
        lineage_dict[key] = value


dp.close()





#####################################################
# Define DP and Frequency dictionaries 
#####################################################

DP_dict= {
None : 0
}

for lineage in (Counter(lineage_dict.values())).keys(): 
	key=lineage
	value= int(0)
	DP_dict[key]=value

freq_dict= {
None : 0
}

for lineage in (Counter(lineage_dict.values())).keys(): 
	key=lineage
	value= int(0)
	freq_dict[key]=value



#####################################################
# Read bam count and provide a summary by lineages 
#####################################################
read_count = open(read_count_file)

for line in read_count:
	line_field=line.split('\t')
	if (line_field[5].startswith('A') and line_field[6].startswith('C') and line_field[7].startswith('G') and line_field[8].startswith('T')and line_field[9].startswith('N')):
		nb_A=float(line_field[5].split(':')[1])
		nb_C=float(line_field[6].split(':')[1])
		nb_G=float(line_field[7].split(':')[1])
		nb_T=float(line_field[8].split(':')[1])
		nb_N=float(line_field[9].split(':')[1])
		nb_tot=float(line_field[3])
		pos=line_field[1]

		if nb_A > 2 :
			freq_A=nb_A/nb_tot
			lignee=lineage_dict.get((line_field[1], 'A'))
			DP_dict[lignee] += 1

			value =  freq_dict[lignee] +freq_A
			freq_dict[lignee] = value

		if nb_C > 2:
			freq_C=nb_C/nb_tot
			lignee=lineage_dict.get((line_field[1],'C'))
			DP_dict[lignee]+=1

			value=freq_dict[lignee]+ freq_C
			freq_dict[lignee]=value

		if nb_G > 2:
			freq_G=nb_G/nb_tot
			lignee=lineage_dict.get((line_field[1],'G'))
			DP_dict[lignee]+=1

			value=freq_dict[lignee]+ freq_G
			freq_dict[lignee]=value

		if nb_T > 2:
			freq_T=nb_T/nb_tot
			lignee=lineage_dict.get((line_field[1],'T'))
			DP_dict[lignee]+=1

			value=freq_dict[lignee]+ freq_T
			freq_dict[lignee]=value




	else :
		print("Read count file have a bad nucleotide order or a wrong format")
		break

read_count.close()


#####################################################
# Output the final support by lineage 
#####################################################
output=open(out_file, "a")
if os.path.getsize(out_file) == 0:
	print ("ID", "lineage", "rate_DP", "freq_read", "total_DP", file = output)
 
for lineage, total_DP  in (Counter(lineage_dict.values())).items(): 
	rate_DP=round(float(DP_dict[lineage])/float(total_DP) , 4)
	if rate_DP > 1: 
		print("There is duplicate line in your read_count_file, please remove them.")

	if float(DP_dict[lineage])  == 0:
		freq_reads='NA'
	else :
		freq_reads=round(float(freq_dict[lineage])/float(DP_dict[lineage]), 4)

	print( ID, lineage, rate_DP, freq_reads, total_DP, file = output)







