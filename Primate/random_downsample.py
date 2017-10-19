import random
import sys

expected = int(sys.argv[1])  # expected of total amount of nucleotides
file_len = int(sys.argv[2])  # file line by wc -l
f = sys.argv[3]  # input file

filetype = f.split(".")[-1]  # fastq or fasta

output = open("%s_trimmed.%s" % ("".join(f.split(".")[:-1]), f.split(".")[-1]), 'w')  # open the output file

with open(f, "r") as myfile:
    x = myfile.readline()
    r = len(myfile.readline())-1


p = (expected / r) / file_len
print(p)

if p > 1:
    with open(f, "r") as myfile:
        for line in myfile:
            output.write(line)
        output.close()
        sys.exit()

with open(f, "r") as myfile:
    if filetype in ['fq', 'fastq']:

        i = 0
        inOrNot = True

        for line in myfile:
            if i % 4 == 0: inOrNot = random.random() <= p

            if (inOrNot):
                output.write(line)

            i += 1

    elif filetype in ['fa', 'fasta']:
        for line in myfile:
            # p = expected/(len(lines)*len(lines[1]))

            # for line in lines:
            if line[0] == ">":
                if random.random() <= p:
                    output.write(out)
                out = line
            else:
                out += line

output.close()
