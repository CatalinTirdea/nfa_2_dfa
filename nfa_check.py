
def transitionCheck(DFA,type,transition):
  
  for element in DFA[type]:
   
    if transition  == element:
      return True
  return False


def check(NFA):
  valid = True
  nrS = 0
  transitions = 0 
  transition = 0 
  for state in NFA["states"]:
      if state == 'S':
        nrS += 1 
      if nrS > 1:
        return False
  
  for transitions in range(0,int(len(NFA['transitions'])/3)):
   
    
   
    valid = transitionCheck(NFA,"states",NFA["transitions"][transition])
    
    if valid == False:
       return valid
    transition += 1
   
    
   
    valid = transitionCheck(NFA,"sigma",NFA["transitions"][transition])
    
    if valid == False:
       return valid
    transition += 1
   
    
   
    valid = transitionCheck(NFA,"states",NFA["transitions"][transition])
    
    if valid == False:
       return valid
    
    transition += 1
    
  return valid
  

   
def putInDictionary(lines,words,line,NFA,type):
  while words[0] != "End":
            line += 1
            words = [ele for x in lines[line].split(',') for ele in x.split()]
            if(words[0] != "End"):
                for word in words:   
                  NFA[type].append(word)
    

def readFile(NFA,directory):
  file = open(directory,"r") #citim fisierul
  
  lines = file.readlines() #citim fiecare linie
  
  

  
  for line in range(0,len(lines)-1): #parcurgem fiecare linie

      words = [ele for x in lines[line].split(',') for ele in x.split()] #separam fiecare cuvant din linia respectiva si grupam intr-o lista
     
      if len(words) != 0 and (words[0] == "Sigma" or words[0] == "Sigma:"): #incepem cautarea de la sigma pana la end si punem intr-o lista fiecare sigma 
        
        putInDictionary(lines,words,line,NFA,"sigma")

      if len(words) != 0 and (words[0] == "States" or words[0] == "States:"): #incepem cautarea de la states pana la end si punem in lista fiecare state
        putInDictionary(lines,words,line,NFA,"states")
    
      
      if len(words) != 0 and (words[0] == "Transitions" or words[0] == "Transitions:"): #incepem cautarea de la transitions pana la end cream o lista cu tranzitiile si punem totul intr-o lista 
        putInDictionary(lines,words,line,NFA,"transitions")
          


def validate(directory):
  
  NFA = {
    "sigma" : [],
    "states": [],
    "transitions" : [] 
  }
  
  readFile(NFA,directory) #citim fisierul si punem in liste detaliile esentiale din fisier precum sigma, state-urile si transition-urile
  
  return check(NFA) #afisam True daca fisierul respecta toate regulile impuse sau False in caz contrar


# print(validate("D:/Facultate/LFA/fisier.txt"))