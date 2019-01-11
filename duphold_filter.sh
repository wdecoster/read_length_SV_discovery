function filter {
  bcftools sort $1 | bgzip > ${1}.gz && tabix -p vcf ${1}.gz && bcftools view -i '(SVTYPE = "DEL" & DHFFC < 0.7) | (SVTYPE = "DUP" & DHFFC > 1.3) | (SVTYPE = "INS")' ${1}.gz -o ${1%.*}_filtered.vcf
}

export -f filter

ls *.vcf | parallel 'filter {}'

