for error in 01 02 03 04 05 06 07 08 09 10; do
  for name in orangutan human gorilla chimp mmu gibbons green marmoset bonobo baboon; do
    file=$name._simulation_l100_x10_0.${error}0000er.fa
    echo "Running kmc on ${name}.${error}"
    mkdir -p /netscr/ganx/${name}.e${error}
    bsub -J kmc.$name.e${error} -M16 "/proj/cdjones_lab/ganx/KMC/bin/kmc -k30 -ci5 -fa -cs65535 ${file} ./temp/${name}_kmc_e${error}_k30_2byte_1thres /netscr/ganx/${name}.e${error}"
  done

  condition=""

  for name1 in orangutan human gorilla chimp mmu gibbons green marmoset bonobo baboon; do
    for name2 in orangutan human gorilla chimp mmu gibbons green marmoset bonobo baboon; do
      if [ $name1 == "orangutan" ]; then
          num1=1
      fi
      if [ $name1 == "human" ]; then
          num1=2
      fi
      if [ $name1 == "gorilla" ]; then
        num1=3
      fi
      if [ $name1 == "chimp" ]; then
        num1=4
      fi
      if [ $name1 == "mmu" ]; then
        num1=5
      fi
      if [ $name1 == "bonobo" ]; then
        num1=6
      fi
      if [ $name1 == "baboon" ]; then
        num1=7
      fi
      if [ $name1 == "green" ]; then
        num1=8
      fi
      if [ $name1 == "marmoset" ]; then
        num1=9
      fi
      if [ $name1 == "gibbons" ]; then
        num1=10
      fi
      if [ $name2 == "orangutan" ]; then
        num2=1
      fi
      if [ $name2 == "human" ]; then
        num2=2
      fi
      if [ $name2 == "gorilla" ]; then
        num2=3
      fi
      if [ $name2 == "chimp" ]; then
        num2=4
      fi
      if [ $name2 == "mmu" ]; then
        num2=5
      fi
      if [ $name2 == "bonobo" ]; then
        num2=6
      fi
      if [ $name2 == "baboon" ]; then
        num2=7
      fi
      if [ $name2 == "green" ]; then
        num2=8
      fi
      if [ $name2 == "marmoset" ]; then
        num2=9
      fi
      if [ $name2 == "gibbons" ]; then
        num2=10
      fi
      if [ $num1 -lt $num2 ]; then
        echo "Running unionning & dumping on ${name1}_${name2}.e${error}"
        bsub -M16 -J subtract.${name1}_${name2}.e${error} -w "done(kmc.$name1.e${error}) && done(kmc.$name2.e${error})" "/proj/cdjones_lab/ganx/KMC/bin/kmc_tools simple ./temp/${name1}_kmc_x${coverage}_k30_2byte_1thres ./temp/${name2}_kmc_x${coverage}_k30_2byte_1thres kmers_subtract ./temp/subtract_${name1}_${name2}_x${coverage}_k30_2byte -cs65535"
        bsub -M16 -J subtract.${name2}_${name1}.e${error} -w "done(kmc.$name1.e${error}) && done(kmc.$name2.e${error})" "/proj/cdjones_lab/ganx/KMC/bin/kmc_tools simple ./temp/${name2}_kmc_x${coverage}_k30_2byte_1thres ./temp/${name1}_kmc_x${coverage}_k30_2byte_1thres kmers_subtract ./temp/subtract_${name2}_${name1}_x${coverage}_k30_2byte -cs65535"
        bsub -M8 -J diff.${name1}_${name2}.$coverage -w "done(subtract.${name1}_${name2}.$coverage) && done(subtract.${name2}_${name1}.$coverage)" "/proj/cdjones_lab/ganx/KMC/bin/kmc_tools simple ./temp/subtract_${name1}_${name2}_x${coverage}_k30_2byte ./temp/subtract_${name2}_${name1}_x${coverage}_k30_2byte union ./temp/diff_${name1}_${name2}_x${coverage}_k30_2byte -cs65535"
        bsub -J dump.${name1}_${name2}.$coverage  -w "done(diff.${name1}_${name2}.$coverage)"  "/proj/cdjones_lab/ganx/KMC_better/bin/kmc_dump -ci5 ./temp/diff_${name1}_${name2}_x${coverage}_k30_2byte ./temp/diff_${name1}_${name2}_x${coverage}_k30_2byte_5thre.txt"
        if [ -z "$condition" ]; then condition="done(dump.${name1}_${name2}.$coverage)"; else condition="$condition && done(dump.${name1}_${name2}.$coverage)"; fi
      fi
    done
  done

  prev_step=$condition

  echo "Getting the distance table for $coverage"
  bsub -J dist.dc.$coverage -w "$prev_step" "python /proj/cdjones_lab/ganx/primate_chr1/fasta_files/Inter_CMP_wc.py -d -unique ./temp/diff_*_x${coverage}_k30_2byte_5thre.txt > primate_simulation_x${coverage}_k30_2byte_5thre_unique_whole.dist"
  bsub -J fastme.dc.$coverage -w "done(dist.dc.$coverage)" "/proj/cdjones_lab/ganx/tree_builder/fastme-2.1.5/src/fastme -i primate_simulation_x${coverage}_k30_2byte_5thre_unique_whole.dist -o primate_simulation_x${coverage}_k30_2byte_5thre_unique_whole.newick"
  bsub -w "done(fastme.dc.$coverage)" "python /proj/cdjones_lab/ganx/tree_builder/draw_newick.py  primate_simulation_x${coverage}_k30_2byte_5thre_unique_whole.newick primate_simulation_x${coverage}_k30_2byte_5thre_unique_whole.png marmoset primate_whole_simulation_5thres_unique_coverage${coverage}"
done
