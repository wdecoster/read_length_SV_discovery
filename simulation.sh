parallel --bar 'simlord -c 20 --without-ns -fl {} -rr HG00733_diploid_phased_scaffolds.fasta --no-sam simlord-{}' ::: 100 200 300 500 750 1500 3000 4000 25000
