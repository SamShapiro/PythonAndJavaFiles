import re

s = re.compile("GATATATGCATATACTT")
s1 = re.compile("ATAT")

def myfindall(regex, seq): 
   resultlist=[] 
   pos=0 

   while True: 
      result = regex.search(seq) 
      if result is None: 
         break 
      resultlist.append(seq[result.start():result.end()]) 
      pos = result.start()+1 
   return resultlist 
 
myfindall(s1,s) 
