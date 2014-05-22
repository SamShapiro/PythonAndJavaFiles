s = []
n = 0
nli = []
with open("rosalind_common.txt", "r") as f:
    for line in f.readlines():
        if line.startswith(">") == False:
            nli.append(line.replace('\n', ''))
        else:
            s.append(''.join(nli))
            nli = []
    s.append(''.join(nli))


m = 0

s1 = []
ACGT1 = ["A", "C", "G", "T"]
liA = []
liC = []
liG = []
liT = []

while m < len(s[0]):
    ACGT = [0,0,0,0]
    for c in s:
        if c[m] == "A":
            ACGT[0]= ACGT[0] + 1
        elif c[m] == "C":
            ACGT[1] = ACGT[1] + 1
        elif c[m] == "G":
            ACGT[2] = ACGT[2] + 1
        elif c[m] == "T":
            ACGT[3] = ACGT[3] + 1
    s1.append(ACGT1[ACGT.index(max(ACGT))])
    liA.append(str(ACGT[0]))
    liC.append(str(ACGT[1]))
    liG.append(str(ACGT[2]))
    liT.append(str(ACGT[3]))
    m = m + 1

print(''.join(s1))
print("A: " + ' '.join(liA))
print("C: " + ' '.join(liC))
print("G: " + ' '.join(liG))
print("T: " + ' '.join(liT))
