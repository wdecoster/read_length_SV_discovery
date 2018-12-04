ls *.bam | parallel --bar -j 10 'sniffles -m {} -v {.}.vcf -t 4 --genotype && mv {} bam_done/ && mv {}.bai bam_done/'
