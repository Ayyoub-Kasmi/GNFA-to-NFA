# we used the character '#' as 'epsilon', since the empty string causes some programmatical issues 
class FA: # Finite Automata
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions

class GNFA(FA): # Generalized Non-deterministic Finite Automata
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        super().__init__(alphabet, states, initial_state, final_states, transitions)
        self.cpt = len(states) # number of states, counter used for naming

    def toPGNFA(self): # Partially-Generalized Non-deterministic Finite Automata
        # Split the words & add intermediary states
        newStates = self.states.copy()
        newTransitions = dict()

        for start_state, trs in self.transitions.items():
            # iterate over starting states of transitions and their transitions, and for each transition:
            for next_state, words in trs.items():
                # words = set of words
                for word in words:
                    # if the transition word is a character, keep the transition
                    if(len(word) < 2):
                        if not start_state in newTransitions:
                            newTransitions[start_state] = dict()
                            newTransitions[start_state][next_state] = set(word)
                        elif not next_state in newTransitions[start_state]:
                            newTransitions[start_state][next_state] = set(word)
                        else:
                            newTransitions[start_state][next_state].add(word)
                    else:
                        # split the transition's word
                        prevState = start_state
                        if not prevState in newTransitions: newTransitions[prevState] = dict()
                        for char in word[0:-1]:
                            intermediate_state = f'S{self.cpt}'
                            newStates.add(intermediate_state)
                            newTransitions[intermediate_state] = dict()
                            if intermediate_state in newTransitions[prevState]:
                                newTransitions[prevState][intermediate_state].add(char)
                            else:
                                newTransitions[prevState][intermediate_state] = set(char)
                            prevState = intermediate_state
                            self.cpt=self.cpt+1
                        newTransitions[prevState][next_state] = word[-1]

        return PGNFA(
            alphabet=self.alphabet,
            states=newStates,
            transitions=newTransitions,
            initial_state=self.initial_state,
            final_states=self.final_states
        )


class PGNFA(FA):
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        super().__init__(alphabet, states, initial_state, final_states, transitions)
        self.cpt = len(states)
    
    def toNFA(self):
        newFinalStates = self.final_states
        newTransitions = dict()

        for start_state, trs in self.transitions.items():
            # iterate over starting states of transitions and their transitions, and for each transition:
            for next_state, chars in trs.items():
                # words = set of words
                for char in chars:
                    # if the transition word is a character, keep the transition
                    if char == '#':
                        # get the transitions (successors) of 'next_state'
                        for other_state, other_char in self.transitions[next_state].items():
                            if not start_state in newTransitions:
                                newTransitions[start_state] = dict()
                                newTransitions[start_state][other_state] = set(other_char)
                            elif not other_state in newTransitions[start_state]:
                                newTransitions[start_state][other_state] = set(other_char)
                            else:
                                newTransitions[start_state][other_state] = other_char
                        if next_state in self.final_states: newFinalStates.add(start_state)
                    else:
                        if not start_state in newTransitions:
                            newTransitions[start_state] = dict()
                            newTransitions[start_state][next_state] = set(char)
                        elif not next_state in newTransitions[start_state]:
                            newTransitions[start_state][next_state] = set(char)
                        else: 
                            newTransitions[start_state][next_state].add(char)

        return NFA(
            alphabet=self.alphabet,
            states=self.states,
            transitions=newTransitions,
            initial_state=self.initial_state,
            final_states=newFinalStates
        )

class NFA(FA):
    def __init__(self, alphabet, states, initial_state, final_states, transitions):
        super().__init__(alphabet, states, initial_state, final_states, transitions)
        self.cpt = len(states)

gnfa = GNFA(
    alphabet={'0', '1'},
    states={'S0', 'S1', 'S2'},
    transitions={
        'S0': {'S1': {'0'}, 'S0': {'01'}},
        'S1': {'S2': {'#', '00'},},
        'S2': {'S1': {'1'},},
    },
    initial_state='S0',
    final_states={'S2'}
)

print(gnfa.transitions)
print("\n\n========================\n\n")
pgnfa = gnfa.toPGNFA()
print(pgnfa.transitions)
print("\n\n========================\n\n")
nfa = pgnfa.toNFA()
print(nfa.final_states)
print(nfa.transitions)
