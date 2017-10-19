for name in orangutan human gorilla chimp mmu gibbons green marmoset bonobo baboon; do
  if [ $name == "orangutan" ]; then
    file=GCF_000001545.4_P_pygmaeus_2.0.2_genomic.fna
  fi
  if [ $name == "human" ]; then
    file=GCF_000001405.37_GRCh38.p11_genomic.fna
  fi
  if [ $name == "gorilla" ]; then
    file=GCF_000151905.2_gorGor4_genomic.fna
  fi
  if [ $name == "chimp" ]; then
    file=GCF_000001515.7_Pan_tro_3.0_genomic.fna
  fi
  if [ $name == "mmu" ]; then
    file=GCF_000772875.2_Mmul_8.0.1_genomic.fna
  fi
  if [ $name == "bonobo" ]; then
    file=GCF_000258655.2_panpan1.1_genomic.fna
  fi
  if [ $name == "baboon" ]; then
    file=GCF_000264685.3_Panu_3.0_genomic.fna
  fi
  if [ $name == "green" ]; then
    file=GCF_000409795.2_Chlorocebus_sabeus_1.1_genomic.fna
  fi
  if [ $name == "marmoset" ]; then
    file=GCF_000004665.1_Callithrix_jacchus-3.2_genomic.fna
  fi
  if [ $name == "gibbons" ]; then
    file=GCF_000146795.2_Nleu_3.0_genomic.fna
  fi
  move file $name.fa

  coverage=10
  for error in 0.01 0.02 0.03 0.04 0.05 0.06 0.07 0.08 0.09 0.10; do
    echo "Runing simulation on $name ar error of $error"
    # bsub -M16 -J de.$error "python primate_simulate.py 100 $coverage $error ${name}.fa"
  done

  error=0.01
  for coverage in 1 2 3 4 5 6 7 8 9 10 12 15 20; do
    echo "Runing simulation on $name ar coverage of $coverage"
    # bsub -M16 -J dc.$coverage "python primate_simulate.py 100 $coverage $error ${name}.fa"
  done
done
