from scipy.stats import rv_discrete
import random

class FSM:
    def __init__(self, states):
        self.states = states
        self.distributions = FSM.__make_dists(states)

        self.state = random.choice(states.keys())

    def tick(self):
        curr = self.state
        next_dist = self.distributions[self.state]

        next_state = next_dist.rvs()

        self.state = next_state
        return next_state

    def gen_seq(self, num):
        seq = []
        for i in xrange(num):
            seq.append(self.tick())
        return seq

    @staticmethod
    def __make_dists(states):
        return {k: rv_discrete(name='foo', values=v)
                for k, v in states.items()}


def estimate_pmatrix(seq):
    """
    given a list of states, estimates the transition matrix
    of the underlying Finite State Machine.
    """
    assert(len(seq) > 1)

    allstates = set(seq)
    numstates = len(allstates)
    count_matrix = {curr: {nxt: 0 for nxt in allstates}
                    for curr in allstates}

    for curr, nxt in zip(seq, seq[1:]): # not lazy :(
        count_matrix[curr][nxt] += 1

    pmatrix = {curr: (nexts.keys(), estimate_prob(nexts.values()))
               for curr, nexts in count_matrix.items()}

    for _curr, nexts in pmatrix.items():
        _states, probs = nexts
        assert(sum(probs) == 1.0)

    return pmatrix

def estimate_prob(counters):
    s = sum(counters)
    # WOW. Such weak. Very duck
    return [c * 1.0 / s for c in counters]

if __name__ == "__main__":
    # NOTE: State (ToState, Probabilities)
    states = {1: ([1, 2, 3], [0.9, 0.1, 0.0])
             ,2: ([1, 2, 3], [0.5, 0.0, 0.5])
             ,3: ([1, 2, 3], [0.0, 0.1, 0.9])}
    machine = FSM(states)

    seq = machine.gen_seq(10000)
    # both pmatrices are largely identical
    print estimate_pmatrix(seq)
