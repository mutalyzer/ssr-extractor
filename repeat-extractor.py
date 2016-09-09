def LCS(s1, s2):
    m = [[0] * (1 + len(s2)) for i in xrange(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in xrange(1, 1 + len(s1)):
        for y in xrange(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1] and s1[x - 1] != '.':
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]


def mask_string(string, units):
    for unit in units:
        found = string.find(unit)
        if found != -1:
            string = string.replace(unit, '.' * len(unit))
    return string


def extract_repeats(reference, sample):
    lcs = LCS(reference, sample)
    ref_start = reference.find(lcs)
    alt_start = sample.find(lcs)


def main():
    reference = 'TTTGGAAACAGAAATGGCTTGGCCTTGCCTGCCTGCCTGCCTGCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCCTCCTGCAATCCTTTAACTTACTGAATAACTCATGATTATGGGCCACCTGCAGGTACCATGCTAG'
    sample =    'AGCTGTGGGAGGGAGCCAGTGGATTTGGAAACAGAAATGGCTTGGCCTTGCCTGCCTGCCTGCCTGCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCTTCCGTCCTTCCTTCCCTCCTGCAATCCTTTAACTTACTGAATAACTCATGATTATGGGCCACCTGCAGGTACCATGCTAG'
    units = ['TCCT', 'GCCT']

    masked_ref = mask_string(reference, units)
    masked_alt = mask_string(sample, units)

    extract_repeats(masked_ref, masked_alt);


if __name__ == '__main__':
    main()

