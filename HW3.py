import sys
import copy

class State:
    def __init__(self):
        self.num = None
        self.final = None
        self.transitions = []

class PDA:
    def __init__(self, states):
        self.states = states
        self.found = False
        self.acceptedPath = []

    def validateString(self, string):
        stack = ['*']
        valid = self.generateTree(self.states[0], string, stack)
        self.found = False
        return valid
    
    def generateTree(self, state, string, stack):
        if self.found:
            return 0
        if self.foundPath(state, string, stack):
            self.found = True
            return 1

        total = 0
        
        moves = self.findMoves(state, string, stack)

        # No more moves
        if len(moves) == 0:
            return 0
        
        # Make a new tree
        for move in moves:
            total = total + self.generateTree(move[0], move[1], move[2])

        return total
    
    def foundPath(self, state, string, stack):
        if len(string) > 0:
            return 0
        elif state.final:
            return 1
        return 0

    def findMoves(self, state, string, stack):
        moves = []
        for transition in state.transitions:
            tempStack = copy.deepcopy(stack)
            tempString = string if len(string) == 0 else string[1:]
            # Inputchar matches 
            if len(string) > 0 and string[0] == transition[1]:
                if transition[2] == stack[len(stack) - 1]:
                    tempStack.pop()
                    if transition[3] != 'e':
                        tempStack.append(transition[3])
                    moves.append([self.getState(transition[0]), tempString, tempStack])
                elif transition[2] == 'e':
                    if transition[3] != 'e':
                        tempStack.append(transition[3])
                    moves.append([self.getState(transition[0]), tempString, tempStack])
            # Free transition
            elif transition[1] == 'e':
                if transition[2] == stack[len(stack) - 1]:
                    tempStack.pop()
                    if transition[3] != 'e':
                        tempStack.append(transition[3])
                    moves.append([self.getState(transition[0]), tempString, tempStack])
                elif transition[2] == 'e':
                    if transition[3] != 'e':
                        tempStack.append(transition[3])
                    moves.append([self.getState(transition[0]), tempString, tempStack])

        return moves
    def getState(self, num):
        for state in self.states:
            if state.num == num:
                return state
        return None


if __name__ == '__main__':
    data = []
    with open(sys.argv[1], 'r') as inputFile:
        for line in inputFile.readlines():
            data.append(line.replace('\n',''))
    
    numStates, numTransitions, startState, finalStates = [int(i) for i in data[0].split(' ')]

    states = []
    for i in range(len(data) - 1):
        # Initial Data of state
        stateData = data[i + 1].split(' ')
        stateNum = int(stateData[0])
        stateFinal = (stateNum == finalStates)

        tempState = None
        # Checking if state already exists
        for state in states:
            if state.num == stateNum:
                tempState = state

        # Not found create a new state
        if tempState is None:
            tempState = State()
            tempState.num = stateNum
            tempState.final = stateFinal
            states.append(tempState)
        # For transitions
        
        # Adding transition
        tempState.transitions.append([int(stateData[1]), stateData[2], stateData[3], stateData[4]])


        # Creating the nextState state
        found = False
        for state in states:
            if int(stateData[1]) == state.num:
                found = True

        if not found:
            newState = State()
            newState.num = int(stateData[1])
            newState.final = (newState.num == finalStates)
            states.append(newState)

    pda = PDA(states)
    inputs = []
    with open(sys.argv[2], 'r') as inputFile:
        for line in inputFile.readlines():
            inputs.append(line.replace('\n', ''))
    for i in range(1, len(inputs)):
        print(inputs[i] + " " + str(pda.validateString(inputs[i])))
    