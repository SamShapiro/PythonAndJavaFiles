def converter(j):
    if j == "UUU" or j == "UUC":
         return "F"
    if j == "UUA" or j == "UUG" or j == "CUU" or j == "CUC" or j == "CUA" or j == "CUG":
         return "L"
    if j == "UCU" or j == "UCC" or j == "UCA" or j == "UCG" or j == "AGU" or j == "AGC":
         return "S"
    if j == "UAU" or j == "UCG" or j == "UAC":
         return "Y"
    if j == "UAA" or j == "UAG" or j == "UGA":
        return "STOP"
    if j == "UGU" or j == "UGC":
         return "C"
    if j == "UGG":
         return "W"
    if j == "CCU" or j == "CCC" or j == "CCA" or j == "CCG":
         return "P"
    if j == "CAU" or j == "CAC":
         return "H"
    if j == "CAA" or j == "CAG":
         return "Q"
    if j == "CGU" or j == "CGC" or j == "CGA" or j == "CGG" or j =="AGA" or j == "AGG":
         return "R"
    if j == "AUU" or j == "AUC" or j == "AUA":
         return "I"
    if j == "AUG":
        return "M"
    if j == "ACU" or j == "ACC" or j == "ACA" or j == "ACG":
         return "T"
    if j == "AAU" or j == "AAC":
         return "N"
    if j == "AAA" or j == "AAG":
         return "K"
    if j == "GUU" or j == "GUC" or j == "GUA" or j == "GUG":
         return "V"
    if j == "GCU" or j == "GCC" or j == "GCA" or j == "GCG":
         return "A"
    if j == "GAU" or j == "GAC":
         return "D"
    if j == "GAA" or j == "GAG":
         return "E"
    if j == "GGU" or j == "GGC" or j == "GGA" or j == "GGG":
         return "G"

s0 = []
with open("rosalind_prot.txt", "r") as f:
    for line in f.readlines():
        s0.append(line.replace('\n', ''))

s = ''.join(s0)
#print(s)

li = []
li1 = []

for i in range(0, len(s), 3):
    li.append(s[i:i+3])

z = 0
for j in li:
    k = converter(j)
    if k == None:
        print(k)
        print(j)
    if k == "STOP":
        z = 1
    if z == 0:
        li1.append(k)

#print(li1)
    
s1 = "".join(li1)
print(s1)

