from nfa_check import *
from pathlib import Path
import sys


def printTable(table):
    for i in table:
        print('\t'.join(map(str, i)))


def transformDFA(createdNFA, NFA):
    DFA = {
        "sigma": [],
        "states": [],
        "transitions": []
    }

    # add all the letters to the DFA except epsilon
    for letter in NFA["sigma"]:
        if letter != "epsilon":
            DFA['sigma'].append(letter)

    # create the transition table

    transitionTable = createTransitionTable(NFA, createdNFA, DFA)

    # after creating the DFA table we create the transitions in the DFA

    rows = len(transitionTable)
    cols = len(transitionTable[0])

    # we go trough the transition table with 2 fors and add to the transitions

    for row in range(1, rows):
        if transitionTable[row][0] != 0:
            trans = str(transitionTable[row][0])
            for col in range(1, cols):
                if transitionTable[0][col] != "epsilon":
                    trans = str(transitionTable[row][0])
                    trans += "," + transitionTable[0][col]
                    if transitionTable[row][col] == 0 or transitionTable[row][col] == '':
                        trans += "," + "vid"
                    else:
                        trans += "," + str(transitionTable[row][col])
                    DFA['transitions'].append(trans)

    # we if the sigma goes to 0 it means it goes to the void state

    for col in range(1, cols):
        if transitionTable[0][col] == 0:
            trans = "vid" + "," + transitionTable[0][col] + ",vid"
            DFA['transitions'].append(trans)

    # adding the void trap

    for sig in NFA["sigma"]:
        if sig != "epsilon":
            trans = "vid" + "," + sig + "," + "vid"
            DFA['transitions'].append(trans)
    i = 0
    # Adding the Finish states
    while i < len(DFA['states']):

        multipleState = str(DFA["states"][i]).split(".")
        for ms in multipleState:

            if ms in createdNFA['finish']:
                DFA['states'].insert(i+1, 'F')
        i += 1
    return DFA
    # create the Transition Table


def createTransitionTable(NFA, createdNFA, DFA):
    nr = 0
    # counting how many states
    for state in NFA['states']:
        if state != "S" and state != 'F':
            nr += 1

    # making the table with the maximum ammount of state that it can generate
    cols = len(NFA["sigma"])+1
    rows = (2**nr) + 1

    # adding 0's to the table
    transitionTable = [[0 for j in range(cols)]for i in range(rows)]

    transitionTable[0][0] = "S/T"

    i = 1
    # adding the sigma to the table including epsilon
    for sig in NFA['sigma']:
        transitionTable[0][i] = sig
        i += 1
    i = 1
    # adding the first states that the NFA already has
    for state in NFA['states']:
        if state != "S" and state != 'F':
            transitionTable[i][0] = state
            DFA['states'].append(state)
            i += 1

    row = 1
    newRow = len(NFA['states'])-1

    s = 0
    epsilonstate = ''
    epsilonstaterow = 0
    # go trough the transition table until no new state is found or when the max number of states is reached
    while row < rows and newRow < rows:

        for col in range(1, cols):
            ok = 0
            # do the transition
            transitionTable[row][col] = transition(
                transitionTable[row][0], transitionTable[0][col], createdNFA)

            if transitionTable[row][col] == '':
                transitionTable[row][col] = 0
            # check to see if the new state is a new one or is already found
            for state in DFA['states']:
                if state == transitionTable[row][col]:
                    ok = 1

            # particular case when epsilon creates a new state
            if transitionTable[0][col] == 'epsilon':
                if transitionTable[row][col] != 0:
                    epsilonstate = str(transitionTable[row][0])
                    epsilonstaterow = row

            if str(transitionTable[row][col]) == epsilonstate:
                transitionTable[row][col] = transitionTable[epsilonstaterow][len(
                    transitionTable[0])-1]

            # if it's a new state add to the state entry
            if ok == 0 and transitionTable[row][col] != 0:
                transitionTable[newRow][0] = transitionTable[row][col]
                DFA['states'].append(transitionTable[row][col])

                newRow += 1
            # case when we have a epsilon multiple state chef if it's the start and make that one the start state
            if transitionTable[0][col] == "epsilon":
                multipleState = str(transitionTable[row][col]).split(".")
                if createdNFA['start'] in multipleState and s == 0:
                    DFA['states'].append('S')
                    s = 1

        row += 1
    # else make the initial start state the start
    if s == 0:

        for i in range(0, len(DFA["states"])):
            if DFA['states'][i] == createdNFA['start']:
                DFA['states'].insert(i+1, 'S')
    return transitionTable


def transition(state, sigma, createdNFA):

    nr = 0
    newState = ""

    multipleState = str(state).split(".")
    multipleState.sort()
    multipleState = list(dict.fromkeys(multipleState))

    # make all the transitions a one state
    for ms in multipleState:

        isKeyPresent = ms in createdNFA
        if isKeyPresent == True:

            for st in range(0, len(createdNFA[ms])):

                if createdNFA[ms][st] == sigma and nr == 1:

                    newState += "." + createdNFA[ms][st+1]
                if createdNFA[ms][st] == sigma and nr == 0:
                    if sigma == 'epsilon':
                        newState = ms + "." + str(createdNFA[ms][st+1])
                    else:
                        newState += createdNFA[ms][st+1]
                        nr = 1
        nsduplicates = str(newState).split(".")

        # check for duplicates
        nsduplicates = list(dict.fromkeys(nsduplicates))
        newState = nsduplicates[0]
        for i in range(1, len(nsduplicates)):
            newState += "." + nsduplicates[i]

    return newState


def check(DFA):
    valid = True
    nrS = 0
    transitions = 0
    transition = 0
    for state in DFA["states"]:
        if state == 'S':
            nrS += 1
        if nrS > 1:
            return False

    for transitions in range(0, int(len(DFA['transitions'])/3)):

        valid = transitionCheck(DFA, "states", DFA["transitions"][transition])

        if valid == False:
            return valid
        transition += 1

        valid = transitionCheck(DFA, "sigma", DFA["transitions"][transition])

        if valid == False:
            return valid
        transition += 1

        valid = transitionCheck(DFA, "states", DFA["transitions"][transition])

        if valid == False:
            return valid

        transition += 1

    return valid


def createNFA(directory):

    readFile(NFA, directory)

    createdNFA = {}
    createdNFA["finish"] = []
    createdNFA["start"] = []
    # createdNFA
    for j in range(0, int(len(NFA['states']))):

        if NFA['states'][j] == "S":
            createdNFA["start"] = NFA['states'][j-1]

        if NFA['states'][j] == "F":
            if NFA['states'][j-1] == "S" or NFA["states"][j-1] == "F":
                createdNFA["finish"].append(NFA['states'][j-2])
            else:
                createdNFA["finish"].append(NFA['states'][j-1])

    i = 0

    for transition in range(0, int(len(NFA['transitions'])/3)):

        createdNFA[NFA["transitions"][i]] = []

        i += 3

    i = 0
    for transition in range(0, int(len(NFA['transitions'])/3)):
        createdNFA[NFA["transitions"][i]].append(NFA["transitions"][i+1])
        createdNFA[NFA["transitions"][i]].append(NFA["transitions"][i+2])
        i += 3
    return createdNFA


def writeInFile(f, DFA):

    f.write("Sigma:")
    f.write("\n")

    for sig in DFA["sigma"]:
        f.write(sig)
        f.write("\n")

    f.write("\n")
    f.write("States:")
    f.write("\n")

    for i in range(0, len(DFA['states'])):
        f.write(DFA['states'][i])

        if i+1 != len(DFA['states']):
            if DFA['states'][i+1] != 'S' and DFA['states'][i+1] != 'F':
                f.write("\n")
            else:
                f.write(",")
        else:
            f.write("\n")

    f.write("\n")
    f.write("Transitions:")
    f.write("\n")

    for transition in DFA["transitions"]:
        f.write(transition)
        f.write("\n")


nr_arguments = len(sys.argv)

if nr_arguments != 3:
    print("Invalid number of arguments")
else:
    directory = Path(__file__).with_name(sys.argv[1])
    directory = directory.absolute()
    createdDFA = {}

    if validate(directory) == False:
        print("The dfa configuration file is invalid!")
    else:
        NFA = {
            "sigma": [],
            "states": [],
            "transitions": []
        }
        DFA = {
            "sigma": [],
            "states": [],
            "transitions": []
        }
        createdNFA = createNFA(directory)
        DFA = transformDFA(createdNFA, NFA)

        f = open(sys.argv[2], "w")
        writeInFile(f, DFA)
