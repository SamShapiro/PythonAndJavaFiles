import re
import sys
from itertools import izip
import os
import arvados

try:
        os.remove('personaltileset.fa')
except OSError:
        pass
try:
        os.remove('converterstats.txt')
except OSError:
        pass
try:
        os.remove('tagchangecheck.txt')
except OSError:
        pass


refnum = 0
snpnum = 0
subnum = 0
indelnum = 0
totrefed = 0
tagchanges = 0

this_task = arvados.current_task()
if this_task['sequence'] == 0:
        job_input = arvados.current_job()['script_parameters']['input']
        cr = arvados.CollectionReader(job_input)
        for s in cr.all_streams():
                for f in s.all_files():
                        task_input = f.as_manifest()
                        new_task_attrs = {
                                'job_uuid': arvados.current_job()['uuid'],
                                'created_by_job_task_uuid': arvados.current_task()['uuid'],
                                'sequence': 1,
                                'parameters': {
                                        'input':task_input
                                        }
                                }
                        arvados.api().job_tasks().create(body=new_task_attrs).execute()
        this_task.set_output(None)

else:
        this_task_input = this_task['parameters']['input']
        collection = arvados.CollectionReader(this_task_input)
        input_file = list(collection.all_files())[0]
        e = filter(lambda x: x.isdigit(), input_file.name())
        nme = 'personaltile%s.fa' % e
        out = arvados.CollectionWriter()
        out.set_current_file_name(nme)

        ftile = input_file
        fgff = open('CGI_sample_GS01670-DNA_E02_from_PGP_sample_.ns.gff', 'r')
        changeset = []
        fstts = open('tagchangecheck.txt', 'w')

        for line in fgff:
                splt = re.split(r'[\t\n]', line)
                del splt[-1]
                if splt[0] == 'chr1':
                        if int(splt[4]) > 0:
                                totrefed += int(splt[4]) - int(splt[3]) + 1
                                maxrefs = int(splt[4])
                        z = -1
                        if splt[2] == 'SNP' and splt[0]:
                                snpnum += 1
                                allnum = int(splt[3])
                                alldiff = re.split("[\s;]", splt[-1])

                                allcheck = re.split('/', alldiff[1])
                                allnew = allcheck[-1]
                                allorig = alldiff[z]
                                while allorig not in ['A', 'G', 'C', 'T']:
                                        z -= 1
                                        allorig = alldiff[z]
                                z = - 1
                                doubler=False
                                if len(allcheck) == 2:
                                        if allcheck[0] != allcheck[1]:
                                                doubler = True
                                snphere = ['SNP', 0, allnum, allorig, allnew, doubler]
                                changeset.append(snphere)
                        if splt[2] == 'SUB':
                                subnum += 1
                                doubler = False
                                allnum = int(splt[3])
                                sublen = int(splt[4]) - int(splt[3])
                                alldiff = re.split("[\s;]", splt[-1])
                                allcheck = re.split('/', alldiff[1])
                                allnew = allcheck[-1]
                                allorig = alldiff[z]
                                while re.search('[^ACGT]', allorig):
                                        z -= 1
                                        allorig = alldiff[z]
                                doubler=False
                                if len(allcheck) == 2:
                                        if allcheck[0] != allcheck[1]:
                                                doubler = True
                                subhere = ['SUB', sublen, allnum, allorig, allnew, doubler]
                                changeset.append(subhere)
                        if splt[2] == 'INDEL':
                                indelnum += 1
                                '''
                                allnum = int(splt[3])
                                indellen = int(splt[4]) - int(splt[3])
                                alldiff = re.split("[\s;]", splt[-1])
                                allcheck = re.split('/', alldiff[1])
                                allnew = allcheck[-1]
                                allorig = alldiff[z]
                                while re.search('[^ACGT-]', allorig):
                                        z -= 1
                                        allorig = alldiff[z]
                                doubler=False
                                if len(allcheck) == 2:
                                        if allcheck[0] != allcheck[1]:
                                                doubler = True
                                indelhere = ['INDEL', indellen, allnum, allorig, allnew, doubler]
                                changeset.append(indelhere)
                                '''
                        if splt[2] == 'REF':
                                refnum += 1
        #print(changeset)
        snpleft = snpnum
        subleft = subnum
        indelleft = indelnum
#       ptsf = open('personaltileset.fa', 'w')
        tset = ftile.read()
        tiles = tset.split('>')
        del tiles[0]
        #totrefed = 0
        for t in range(0, len(tiles)):
                d = 0
                retile = re.split('[\:\-\n]', tiles[t])
                retile[3] = ''.join(retile[3:])
                alleles = list(retile[3])
                origall = list(retile[3])
                isDouble = False
                tileCombine = False
        #       print("%d-%d" %(int(retile[1]), int(retile[2])))
        #       maxrefs = int(retile[2])
        #       totrefed += (int(retile[2]) - int(retile[1])) -24
                for j in changeset:
                        if j[2] <= int(retile[2]) and j[2] >= int(retile[1]):
                                if j[1] + j[2] > int(retile[2]):
                                        nexttile = re.split('[\:\-\n]', tiles[t+1])
                                        tagsep = list(nexttile[3])
                                        tilenew = []
                                        for i in retile[3:]:
                                                tilenew.append(i)
                                        for i in tagsep[25:]:
                                                tilenew.append(i)
                                        for i in nexttile[4:]:
                                                tilenew.append(i)
                                        newtile = ''.join(tilenew[:])
                                        stile = '%s:%s-%s\n%s' % (retile[0], retile[1], nexttile[2]$
                                        print('merged %s-%s and %s-%s into %s-%s' % (retile[1], ret$
                                        tileCombine = True
                                        del tiles[t+1]
                                        tiles.insert(t+1, stile)
                                        break
                                if (j[2]-1) <= int(retile[1]) + 24 or (j[2]-1) >= int(retile[2])-24:
                                        tagchanges += 1
                                        print >>fstts, j[2]
                                if j[-1] == True:
                                        isDouble=True
                                if j[0] == 'SNP':
                                        snpleft -= 1
                                        curr = j[2]-int(retile[1]) - 1 - d
        #                               curr = j[2] + 1
                                        if int(retile[1]) == j[2]:
                                                continue
        #                               if j[2] != curr+int(retile[1]):
        #                                       print(j[2])
        #                                       print(curr+int(retile[1]))
        #                                       sys.exit()
                                        if alleles[curr].lower() == j[3].lower():
                                                alleles[curr] = j[4]
                                                snpleft -= 1
                                        elif alleles[curr].lower() == j[4].lower():
                                                continue
                                                snpleft -= 1
                                        else:
                                                print('GFF does not match REF at %s' % j[2])
        #                                       print(retile[1])
                                                print("%d-%d" %(int(retile[1]), int(retile[2])))
                                                print(curr+int(retile[1]))
                                                print("%s > %s with %s" % (j[3], j[4],alleles[curr]$
                                                if j[2] != curr+int(retile[1]):
                                                        sys.exit()
        #                                       d += 1
        #                                       changeset.insert(changeset.index(j)+1, j)
                                elif j[0] == 'SUB':
                                        subleft -= 1
                                        curr = j[2]-int(retile[1]) - 1 - d
        #                                curr = j[2] + 1
                                        end = curr+j[1]
                                        if int(retile[1]) == j[2]:
                                                j[4] = list(j[4])
                                                del j[4][0]
                                                ''.join(j[4])
                                                subleft -= 1
                                        try:
                                                if ''.join(y.lower() for y in alleles[curr:end+1]) $
                                                        alleles[curr:end+1] = j[4]
                                                        k = list(alleles[curr])
                                                        k.reverse()
                                                        for l in k:
                                                                alleles.insert(curr+1, l)
                                                        del alleles[curr]
                                                        subleft -= 1
                                                elif ''.join(y.lower() for y in alleles[curr:end+1]$
                                                        continue
                                                else:
                                                        print('GFF does not match REF at %s' %j[2])
        #                                               sys.exit()
                                                        continue
                                        except AttributeError:
                                                print j[4]
                                                print alleles[curr:end+1]
                                elif j[0] == 'INDEL':
                                        indelleft -= 1
                                        curr = j[2]-int(retile[1]) - 1 - d
        #                               curr = j[2] + 1
                                        if re.match('-', j[3]):
                                                k = list(j[4])
                                                k.reverse()
                                                for l in k:
                                                        alleles.insert(curr, l)
                                                d -= len(j[4])
        #                                       alleles = filter(lambda name: name.strip(), alleles)
                                                indelleft -= 1
                                        elif re.match('-', j[4]):
        #                                       alleles = filter(lambda name: name.strip(), alleles)
                                                end = curr+j[1]
                                                del alleles[curr:end+1]
        #                                       alleles.insert(curr, '')
                                                d += 1
                                                indelleft -= 1
                                        elif re.match('[ACGT]+', j[3]) and re.match('[ACGT]+', j[4]$
                                                end = curr+j[1]
                                                del alleles[curr:end+1]
                                                k = list(j[4])
                                                k.reverse()
                                                for l in k:
                                                        alleles.insert(curr,l)
        #                                       d -= j[1]
                                                d += len(j[3]) - len(j[4])
                                                indelleft -= 1
                                        else:
                                                print('bad INDEL at %s' %j[2])
                                                sys.exit()
                        elif j[2] >= int(retile[2]):
                                break
                if isDouble == False and tileCombine == False:
                        out.write(">%s:%s-%s" % (retile[0], retile[1], retile[2]))
                        for all50 in izip(*[iter(alleles)]*50):
                                out.write(''.join(all50))
                        out.write(''.join(alleles[len(alleles)-(len(alleles) % 50):]))
                elif isDouble == True and tileCombine == False:
                        out.write(">%s:%s-%s A" % (retile[0], retile[1], retile[2]))
                        for all50 in izip(*[iter(alleles)]*50):
                                out.write(''.join(all50))
                        out.write(''.join(alleles[len(alleles)-(len(alleles) % 50):]))
                        out.write(">%s:%s-%s B" % (retile[0], retile[1], retile[2]))
                        for orig50 in izip(*[iter(origall)]*50):
                                out.write(''.join(orig50)
                        out.write(''.join(origall[len(origall)-(len(origall) % 50):]))
#ptsf.close()
        ftile.close()
        fgff.close()
fstts.close()
#print("Successfully generated personal tile set")
#print(maxrefs)
#print(maxrefs-totrefed)
#print(tagchanges)
#with open('converterstats.txt', 'w') as fstats:
#       print>>fstats, "Number of REFs: %d \nNumber of SNPs: %d \nNumber of SNPs Left: %d \nNumber $

