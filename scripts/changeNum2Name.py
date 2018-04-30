import sys

interlist2 = {
1:'nivei',
2:'albom_Ishigaki',
3:'taxonF',
4:'hypo_Luzon',
5:'immigrans',
6:'kep_Sarawak',
7:'kep_Brunei',
8:'koh_Sarawak',
9:'koh_Phillipines',
10:'taxonG',
11:'nas_Mysore',
12:'nas_Mombasa',
13:'neon_Mysore',
14:'taxonJ',
15:'siam_Cambodia',
16:'albost_Luzon',
17:'albostrigata_SriLanka',
18:'bilim_Guam',
19:'sulf_NIreland',
20:'sulf_NGuinea',
21: 'hypo_Guam',
22: 'neohypo_NGuinea',
23: 'pula_Sarawak',
24: 'pallidifrons',
25: 'bilim_Oahu',
26: 'albost_Cambodia',
27: 'albost_Borneo',
28: 'albost_Indonesia',
29: 'Subobscura',
30: 'Yakuba',
31: 'Teissieri',
32: 'Miranda',
33: 'Erecta',
34: 'Orena',
35: 'Persimilis',
36: 'Pseudoobscura',
37: 'Mauritiana',
38: 'Melanogaster'
             }

interlist={
101:'nivei',
102:'albom_Ishigaki',
103:'taxonF',
104:'hypo_Luzon',
105:'immigrans',
106:'kep_Sarawak',
107:'kep_Brunei',
108:'koh_Sarawak',
109:'koh_Phillipines',
110:'taxonG',
111:'nas_Mysore',
112:'nas_Mombasa',
113:'neon_Mysore',
114:'taxonJ',
115:'siam_Cambodia',
116:'albost_Luzon',
117:'albostrigata_SriLanka',
118:'bilim_Oahu',
119:'bilim_Guam',
120:'sulf_NIreland',
121:'sulf_NGuinea',
206: 'hypo_Guam',
215: 'neohypo_NGuinea',
218: 'pula_Sarawak',
219: 'pallidifrons',
225: 'bilim_Oahu',
229: 'albost_Cambodia',
230: 'albost_Borneo',
231: 'albost_Indonesia',
301:"Subobscura",
302: "Simulans",
303:"Yakuba",
304:"Teissieri",
305:"Miranda",
306:"Erecta",
307:"Orena",
308:"yakuba",
309:"Persimilis",
310:"Pseudoobscura",
311:"Mauritiana",
312:"Mauritiana2",
313:"Melanogaster",
314:"sechellia",
315:"Simulans",
316:"yakuba",
317:"yakuba"
}

filename = sys.argv[1]
# read in dist table file


file = open(filename, "r")
number = file.readline().strip()
print(number)
num = int(number)
data = str(num) + "\n"
for i in range(num):
    line = file.readline().split(" ")
    index = int(line[0])
    data += interlist[index] + " "
    for num in line[1:]:
        data += num + " "
    data += "\n"
file.close()
file = open(filename, "w")
file.write(data)
file.close()
