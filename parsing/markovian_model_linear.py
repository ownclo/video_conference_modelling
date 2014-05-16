import sys
import numpy

import parse_trace
import quantizers
import markovian_fsm

def gen_seq(orig, len_seq, num_quants, quantizer=quantizers.linear_quantizer):
    quantize = quantizer(orig, num_quants)
    qseq = map(quantize, orig)

    pmatrix = markovian_fsm.estimate_pmatrix(qseq)
    machine = markovian_fsm.FSM(pmatrix)

    _ = machine.gen_seq(10000)
    seq = numpy.array(machine.gen_seq(len_seq))
    return seq

if __name__ == "__main__":
    tracefile = sys.argv[1]
    with open(tracefile) as f:
        # NOTE: first frame must be skipped
        sizes = numpy.array(parse_trace.get_sizes(f)[1:])

    num_quants = 20
    for q in [quantizers.linear_quantizer, quantizers.kmeans_quantizer]:
        seq = gen_seq(sizes, 10000, num_quants, quantizer=q)

        print seq.mean(), sizes.mean()
        print seq.var(), sizes.var()
        model_corr = parse_trace.acf(seq)
        sizes_corr = parse_trace.acf(sizes)

        print model_corr[1], sizes_corr[1]
        print model_corr[2], sizes_corr[2]
        print model_corr[3], sizes_corr[3]
        print model_corr[4], sizes_corr[4]
        print model_corr[5], sizes_corr[5]
        print '\n'
