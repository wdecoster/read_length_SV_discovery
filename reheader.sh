ls *.vcf | parallel 'echo {} | sed s/.vcf// > {.}.sample && bcftools sort {} | bcftools reheader -s {.}.sample - > variants_reheader/{} && rm {.}.sample'
