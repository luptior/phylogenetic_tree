# move the original compressed files to the current dir and uncompress
echo "Move the original compressed files to the current dir and uncompress"
cp /proj/cdjones_lab/HTSF/151009_UNC18-D00493_0266_AC7JUYANXX/*.gz /proj/cdjones_lab/ganx/Drosophila/fastq2/ && bsub "gunzip /proj/cdjones_lab/ganx/Drosophila/fastq2/*.gz"

condition=""
# do the kmc part
for name in 06 15 18 19 25 29 30 31; do
  if [ $name == "06" ]; then
    file=WADD06_GCCAAT_
  fi
  if [ $name == "15" ]; then
    file=WADD15_CGATGT_
  fi
  if [ $name == "18" ]; then
    file=WADD18_CAGATC_
  fi
  if [ $name == '19' ]; then
    file=WADD19_CTTGTA_
  fi
  if [ $name == '25' ]; then
    file=WADD25_AGTCAA_
  fi
  if [ $name == '29' ]; then
    file=WADD29_TGACCA_
  fi
  if [ $name == '30' ]; then
    file=WADD30_ACAGTG_
  fi
  if [ $name == '31' ]; then
    file=WADD31_AGTTCC_
  fi
  echo "Running kmc on $name."
    for num in 1 2; do
      mkdir -p /netscr/ganx/${name}.${num}
      bsub -J kmc.$name.$num -M16 "/proj/cdjones_lab/ganx/KMC/bin/kmc -k30 -fq -ci1 -cs65535 ${file}L004_R${num}_001.fastq 2${name}_R${num}_KmerCountsResult_2byte_k30_1thres.res /netscr/ganx/${name}.${num} > KMCrunlog_2${name}_${num}"
      if [ $condition == "" ]; then condition="done(kmc.$name.$num)"; else condition="$condition && done(kmc.$name.$num)"; fi
    done
done

prev_step=$condition
condition=""

# union the 2 seperate parts for the seperate kmc results from kmc
for name in 06 15 18 19 29 30 31; do
  echo "Union the 2 seperate parts for $name"
  bsub -M8 -J union.$name -w "$prev_step" "/proj/cdjones_lab/ganx/KMC/bin/kmc_tools simple 2${name}_R1_KmerCountsResult_2byte_k30_1thres.res 2${name}_R2_KmerCountsResult_2byte_k30_1thres.res union WAD_2${name}_k30_2byte_1thres"
  if [ $condition == "" ]; then condition="done(union.$name)"; else condition="$condition && done(union.$name)"; fi
done

echo "Union the 2 seperate parts for 25"
bsub -M8 -J union.118_225 -w "$prev_step" "/proj/cdjones_lab/ganx/KMC/bin/kmc_tools simple 225_R1_KmerCountsResult_2byte_k30_1thres.res 225_R2_KmerCountsResult_2byte_k30_1thres.res union WAD_225_unionpart_k30_2byte_1thres"
# union the 18 in the first batch and 25 in second batch
echo "Union the 18 in the first batch and 25 in second batch"
name = 25
bsub -M8 -J union.$name -w "done(union.118_225)" "/proj/cdjones_lab/ganx/KMC/bin/kmc_tools simple WAD_118_k30_2byte_1thres WAD_225_unionpart_k30_2byte_1thres union WAD_225_k30_2byte_1thres"
if [ $condition == "" ]; then condition="done(union.$name)"; else condition="$condition && done(union.$name)"; fi



prev_step=$condition
condition=""
# begin the subtract part

for name in 06 15 18 19 25 29 30 31; do
  echo "Running histogram on $name."
  bsub -M8 -w "$prev_step"  "/proj/cdjones_lab/ganx/KMC/bin/kmc_tools transform WAD_2${name}_k30_2byte_1thres histogram /histogram/WAD_2${name}_k30_2byte_1thres_histgram.txt"
done

for name1 in 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 119 120 121 206 215 218 219 225 229 230 231; do
  for name2 in 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 119 120 121 206 215 218 219 225 229 230 231; do
    if [ "$name1" != "$name2" ]; then
      name = ${name1}_${name2}
      echo "Running subtraction on $name"
      bsub -M8 -J subtract.$name -w "$prev_step" "/proj/cdjones_lab/ganx/KMC/bin/kmc_tools simple /proj/cdjones_lab/ganx/Drosophila/fastq2/WAD_${name1}_k30_2byte_1thres /proj/cdjones_lab/ganx/Drosophila/fastq2/WAD_${name2}_k30_2byte_1thres kmers_subtract subtract_${name1}_${name2}_k30_2byte -cs65535"
      if [ $condition == "" ]; then condition="done(subtract.$name)"; else condition="$condition && done(subtract.$name)"; fi
    fi
  done
done

prev_step=$condition
condition=""
# begin union the A-B and B-A
for name1 in 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 119 120 121 206 215 218 219 225 229 230; do
  for name2 in 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 119 120 121 206 215 218 219 225 229 230 231; do
    if [ "$name1" -lt "$name2" ]; then
      name = ${name1}_${name2}
      echo "union subtraction on $name"
      bsub -M8 -J diff.$name -w "$prev_step" "/proj/cdjones_lab/ganx/KMC/bin/kmc_tools simple subtract_${name1}_${name2}_k30_2byte subtract_${name2}_${name1}_k30_2byte union diff_${name1}_${name2}_k30_2byte -cs65535"
      if [ $condition == "" ]; then condition="done(diff.$name)"; else condition="$condition && done(diff.$name)"; fi
    fi
  done
done


prev_step=$condition
condition=""

for name1 in 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 119 120 121 206 215 218 219 225 229 230; do
  for name2 in 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 119 120 121 206 215 218 219 225 229 230 231; do
    name = ${name1}_${name2}
    echo "dumping the difference of $name"
    bsub -J dump.$name -w "$prev_step" "/proj/cdjones_lab/ganx/KMC_better/bin/kmc_dump -ci5 diff_${name1}_${name2}_k30_2byte diff_${name1}_${name2}_k30_2byte_5thre.txt"
    bsub -J dump.$name -w "$prev_step" "/proj/cdjones_lab/ganx/KMC_better/bin/kmc_dump -ci10 diff_${name1}_${name2}_k30_2byte diff_${name1}_${name2}_k30_2byte_10thre.txt"
    if [ $condition == "" ]; then condition="done(dump.$name)"; else condition="$condition && done(dump.$name)"; fi
  done
done

prev_step=$condition
condition=""

echo "Getting the distance table"
bsub -J 10thre_unique -w "$prev_step" "python Inter_CMP_wc.py -d -unique *_10thre.txt > Drosophila_2batch_10thre_unique.dist"
bsub -J 5thre_unique -w "$prev_step" "python Inter_CMP_wc.py -d -counts *_5thre.txt > Drosophila_2batch_5thre_counts.dist"
bsub -J 10thre_counts -w "$prev_step" "python Inter_CMP_wc.py -d -counts *_10thre.txt > Drosophila_2batch_10thre_counts.dist"
bsub -J 5thre_counts -w "$prev_step" "python Inter_CMP_wc.py -d -counts *_10thre.txt > Drosophila_2batch_5thre_counts.dist"
