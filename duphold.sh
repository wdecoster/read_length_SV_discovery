ls *.vcf | parallel 'duphold --bam bam_done/{.}.bam --fasta ~/GRCh38_recommended/GCA_000001405.15_GRCh38_no_alt_analysis_set.fna.gz --vcf variants_reheader/{} -o duphold/{.}_dh.vcf'

