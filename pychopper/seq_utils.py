# -*- coding: utf-8 -*-

from six.moves import reduce
import sys
from pychopper.common_structures import Seq

""" Utilities manipulating biological sequences and formats. Extensions to biopython functionality.
"""

# Reverse complements of bases, taken from dragonet:
comp = {
    'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C', 'X': 'X', 'N': 'N',
    'a': 't', 't': 'a', 'c': 'g', 'g': 'c', 'x': 'x', 'n': 'n',
    '-': '-'
}


def base_complement(k):
    """ Return complement of base.

    Performs the subsitutions: A<=>T, C<=>G, X=>X for both upper and lower
    case. The return value is identical to the argument for all other values.

    :param k: A base.
    :returns: Complement of base.
    :rtype: str

    """
    try:
        return comp[k]
    except KeyError:
        sys.stderr.write(
            "WARNING: No reverse complement for {} found, returning argument.".format(k))
        return k


def reverse_complement(seq):
    """ Return reverse complement of a string (base) sequence.

    :param seq: Input sequence.
    :returns: Reverse complement of input sequence.
    :rtype: str

    """
    if len(seq) == 0:
        return seq
    return reduce(lambda x, y: x + y, map(base_complement, seq[::-1]))


def readfq(fp):  # this is a generator function
    """
    Below function taken from https://github.com/lh3/readfq/blob/master/readfq.py
    Much faster parsing of large files compared to Biopyhton.
    """

    last = None  # this is a buffer keeping the last unprocessed line
    while True:  # mimic closure; is it a bad idea?
        if not last:  # the first record or a record following a fastq
            for l in fp:  # search for the start of the next record
                if l[0] in '>@':  # fasta/q header line
                    last = l[:-1]  # save this line
                    break
        if not last:
            break
        name, seqs, last = last[1:], [], None
        for l in fp:  # read the sequence
            if l[0] in '@+>':
                last = l[:-1]
                break
            seqs.append(l[:-1])
        if not last or last[0] != '+':  # this is a fasta record
            yield Seq(name, ''.join(seqs), None)  # yield a fasta record
            if not last:
                break
        else:  # this is a fastq record
            seq, leng, seqs = ''.join(seqs), 0, []
            for l in fp:  # read the quality
                seqs.append(l[:-1])
                leng += len(l) - 1
                if leng >= len(seq):  # have read enough quality
                    last = None
                    yield Seq(Name=name, Seq=seq, Qual="".join(seqs))  # yield a fastq record
                    break
            if last:  # reach EOF before reading enough quality
                yield Seq(name, seq, None)  # yield a fasta record instead
                break

def writefq(r, fh):
    q = r.Qual
    if q is None:
        q = "!" * len(r.Seq)
    fh.write("@{}\n{}\n+\n{}\n".format(r.Name, r.Seq, q))



def revcomp_seq(seq):
    """ Reverse complement sequence record """
    qual = seq.Qual
    if qual is not None:
        qual = qual[::-1]
    return Seq(seq.Name, reverse_complement(seq.Seq), qual)


def _filter_and_annotate(read, match):
    """ Filter sequences by match and annotate with direction. """
    if match is not None:
        direction = '+' if match == 'fwd_match' else '-'
        read.description = read.description + " strand=" + direction
        if match == 'rev_match':
            read = _revcomp_seq(read)
        return read, True
    else:
        return read, False


def get_runid(desc):
    """ Parse out runid from sequence description. """
    tmp = [t for t in desc.split(" ") if t.startswith("runid")]
    if len(tmp) != 1:
        return "NA"
    return tmp[0].rsplit("=", 1)[1]


def record_size(read, in_format='fastq'):
    """ Calculate record size. """
    if read.Qual is None:
        in_format = 'fasta'
    dl = len(read.Name)
    sl = len(read.Seq)
    if in_format == 'fastq':
        bl = dl + 2 * sl + 6
    elif in_format == 'fasta':
        bl = dl + sl + 3
    else:
        raise Exception("Unkonwn format!")
    return bl

def get_primers(primers):
    all_primers = {}
    for acc, (seq, _) in readfq(open(args.primers, 'r')):
        all_primers[acc] = seq
        all_primers[ '-' + acc ] = seu.reverse_complement(seq)
    return all_primers, len(seq)
