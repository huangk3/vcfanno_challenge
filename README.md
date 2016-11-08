**Pre-requirements before running 'run.sh' shell script:**
 1. run 'chmod +x run.sh' and put the input Challenge_data.vcf file in the same folder as 'run.sh'.
 2. get latest bcftools, tabix, snpEff, and GATK installed.  
 3. have access to python3
 4. have internet connection
 5. have human_1k_b37.fasta, dbsnp138_b37.vcf.gz and their index files downloaded from GATK ftp server (ftp://ftp.broadinstitute.org/bundle/2.8/b37/)
 6. modify the work directory and the path of the software tools and resources in the beginning of 'run.sh' to make them accessible.

**Run './run.sh Challenge_data.vcf', and get the final result in tab separated annotation file 'ExAC.annotated.result.txt'**

**The content of each column in 'ExAC.annotated.result.txt':**
- Chr: chromosome;
- Pos: position of the variant on reference genome build 37;
- ID: dbSNP id in dbsnp138, build 37;
- Ref: reference allele;
- Alt: single alternative allele for bi-allelic loci and alternative alleles separated by ',' for multi-allelic loci;
- VarType: variant type, SNP/INDEL/MNP/OTHER;
- GeneSymbol: the name of the gene that the variant locates;
- Impact: the highest-impact of the variant as annotated by snpEff;
- Effect: the highest-effect of the variant as annotated by snpEff;
- FunctionClass: the function class as annotated by snpEff;
- ExAC_AF: allele frequency(s) in ExAC project;
- ExAC_SOMATIC: somatic flag(s) in ExAC project;
- GT_normal: genotype in normal sample;
- DP_normal: total read depth of the loci in normal sample;
- AltCountNormal: read depth(s) of the alt allele(s) in normal sample;. 
- Alt2RefNormal: the ratio(s) between read depth of alt allele(s) and reference allele in normal sample;
- GT_tumor: genotype in normal sample;
- DP_tumor: total read depth of the loci in normal sample;
- AltCountTumor: read depth(s) of the alt allele(s) in normal sample;. 
- Alt2RefTumor: the ratio(s) between read depth of alt allele(s) and reference allele in normal sample;
