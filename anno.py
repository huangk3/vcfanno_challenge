#!/usr/bin/env python
import sys, json, urllib.request
#test if the script is launched correctly.
if len(sys.argv) !=2 or not sys.argv[1].endswith('txt'):
	print("Usage: python3 anno.py <snpEff_annotated.txt>")
	sys.exit(1)

#the function querys the variant's allele frequency and somatic flag through ExAC project API.
def exac_query (variants):
	chr_pos_ref=variants[0]+'-'+variants[1]+'-'+variants[3]
#save the alt alleles in a list for there are multi-allelic sites in the vcf file. The alleles in the alt column will be processed individually.
	alts=variants[4].split(',')
#use lists to save the allele frequencies and somatic flags fetched from ExAC database.
	af=[]
	somatics=[]
	for alt in alts:
	#construct the variant query ID by combing chromosome, position, ref allele and alt allele(s) using "-"
		ids=chr_pos_ref+'-'+alt
		query=urllib.request.urlopen("http://exac.hms.harvard.edu/rest/variant/variant/"+ids)
		data=json.loads(query.read().decode('utf8'))
		#read the allele frequency and save it in a list.
		if 'allele_freq' in data:
			af.append("%.5f" % float(data['allele_freq']))
		#read the somatic flag and if it's not empty, then save it in a list.
		if 'vep_annotations' in data:
			for vep in data['vep_annotations']:
				if vep['SOMATIC'] != '':
					somatics.append(vep['SOMATIC'])
	return {'AF':af, 'SFlag':somatics}

#the function reads in the total read depth of the variant loci and calculate the ratio of alt depth to ref depth.
def alt_ref_ratio (tot_reads, alt_reads):
	try:
		alt_count_list=[int(i) for i in alt_reads.split(',')]
		ref_reads=int(tot_reads)-sum(alt_count_list)
		ratio_decimal=[ac/ref_reads for ac in alt_count_list]
		#round the decimal ratio;
		ratio=["%.5f" % j for j in ratio_decimal]
#handle the exceptions in case that the read depth of ref allele is 0 in case all reads support the alternative allele(s).
	except ZeroDivisionError:
		ratio=['NA']
	return ratio

#the output of the script.
Output=open('ExAC.annotated.result.txt', 'w')
#save the headers of the output table in a list.
header=['Chr', 'Pos', 'ID', 'Ref', 'Alt', 'VarType', 'GeneSymbol', 'Impact', 'Effect', 'FunctionClass',
'ExAC_AF', 'ExAC_SOMATIC', 'GT_normal', 'DP_normal', 'AltCountNormal', 'Alt2RefNormal',
'GT_tumor', 'DP_tumor', 'AltCountTumor','Alt2RefTumor']
#construct the header and write it into the output file.
print('\t'.join(header), file=Output)
with open(sys.argv[1], 'r') as InFile:
	for i in InFile:
		record=i.strip().split('\t')
		var_info=record[0:5]
		#ExAC project API query.
		exac_anno=exac_query(var_info)
		#obtain the Alt/Ref ratio for normal (NARR) and tumor (TARR) samples, respectively.
		NARR=alt_ref_ratio(record[11], record[12])
		TARR=alt_ref_ratio(record[14], record[15])
		#save the result in output file.
		print('\t'.join(record[0:10])+'\t'+','.join(exac_anno['AF'])+'\t'+','.join(exac_anno['SFlag'])+'\t'+
			'\t'.join(record[10:13])+'\t'+','.join(NARR)+'\t'+'\t'.join(record[13:])+'\t'+','.join(TARR), file=Output)

Output.close()
