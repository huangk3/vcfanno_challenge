#!/bin/bash

input_vcf=$1
#change directory to the folder where "Challenge_data.vcf" is saved.
cd ~/Documents/Tempus
#set the path of the software tools and resources used in the script.
ref="${HOME}/Softwares/resources/b37/human_g1k_v37.fasta"
GATK="${HOME}/Softwares/GenomeAnalysisTK-3.6/GenomeAnalysisTK.jar"
snpeff="${HOME}/Softwares/snpEff/snpEff.jar"
dbsnp="${HOME}/Softwares/resources/b37/dbsnp_138.b37.vcf.gz"

#90% of machine memory which will be used as maximum java heap size when running snpEff and GATK
#megs=$(head -n1 /proc/meminfo |awk '{print int(0.9*($2/1024))}')

#Annotate the vcf file using snpEff and GRCh37.75 database, the annototion is attached in the INFO column.
java -jar ${snpeff} GRCh37.75 -o gatk ${input_vcf} > Challenge_data.ann.vcf 

#Annotate each variant with its rs id and highest-impact effect using the VariantAnnotator module of GATK, dbsnp138 build 37 and snpEff annotated vcf file.
java -jar ${GATK} -T VariantAnnotator -A SnpEff --variant ${input_vcf} --snpEffFile Challenge_data.ann.vcf --dbsnp ${dbsnp} -R $ref -o Challenge_data.high.impact.vcf

#query the requested information, such as coordinates, dbsnp ids, variant type, total read depth, alt allele read depth, gene name, snpEff annotation, and genotypes, from the annotated vcf file.
bcftools query -f '%CHROM\t%POS\t%ID\t%REF\t%ALT\t%TYPE\t%INFO/SNPEFF_GENE_NAME\t%INFO/SNPEFF_IMPACT\t%INFO/SNPEFF_EFFECT\t%INFO/SNPEFF_FUNCTIONAL_CLASS[\t%GT\t%DP\t%AO]\n' Challenge_data.high.impact.vcf > Challenge_data.txt

#run the python script using command "python3 anno.py Challenge_data.txt" to generate the table with information such as ExAC allele frequency, SOMATIC flag, ratio between the depth of alt allele and ref allele in normal sample and tumor sample, respectively. The output will be saved in file named "ExAC.annotated.result.txt".
python3 anno.py Challenge_data.txt
