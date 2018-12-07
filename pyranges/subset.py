from pyranges.ncls import find_overlaps

def get_slice(self, val):

    # 100:999


    d = {}

    for k, df in self.items():

        start = val.start or 0
        stop = val.stop or max(df.End.max(), start)
        idxes = find_overlaps(df, start, stop)
        d[k] = df.reindex(idxes)

    return d





def get_string(self, val):

    if val in self.chromosomes:
        if self.stranded:
            return {k: self.dfs[k] for k in self.keys() if k[0] == val}
        else:
            return self.dfs[val]

    elif val in "+ -".split():
        return {k: v for k, v in self.items() if k[1] == val}
    else:
        return {}



def get_tuple(self, val):

    if len(val) == 2:
        df = get_double(self, val)
    elif len(val) == 3:
        df = get_triple(self, val)

    return df


def get_double(self, val):

    # "chr1", 5:10
    if len(val) == 2 and val[0] in self.chromosomes and isinstance(val[1], slice):
        chromosome, loc = val
        start = loc.start or 0
        if self.stranded:
            dfs = {k: df for k, df in self.items() if k[0] == chromosome}
            max_end = max([df.End.max() for df in dfs.values()])
        else:
            dfs = self.dfs[val]
            max_end = df.End.max()

        # in case 1:None
        stop = loc.stop or max(max_end, start)

        dfs2 = {}
        for k, df in dfs.items():
            idxes = find_overlaps(df, start, stop)
            if idxes:
                dfs2[k] = df.loc[idxes]

        return dfs2

    # "+", 5:10
    if len(val) == 2 and val[0] in "+ -".split() and isinstance(val[1], slice):
        strand, loc = val
        start = loc.start or 0

        dfs = {k: df for k, df in self.items() if k[1] == strand}
        max_end = max([df.End.max() for df in dfs.values()])

        stop = loc.stop or max(max_end, start)

        dfs2 = {}
        for k, df in dfs.items():
            idxes = find_overlaps(df, start, stop)
            if idxes:
                dfs2[k] = df.loc[idxes]

        return dfs2


    # "chr1", "+"
    if len(val) == 2 and val[1] in "+ -".split():

        chromosome, strand = val

        if (chromosome, strand) in self.dfs:
            return {(chromosome, strand): self.dfs[chromosome, strand]}
        else:
            return {}


def get_triple(self, val):

    # "chr1", "+", 5:10
    chromosome, strand, loc = val
    start = loc.start or 0

    if strand not in "+ -".split():
        raise Exception("Strand '{}' invalid.".format(val))

    df = self[chromosome, strand].values[0]

    max_end = df.End.max()

    stop = loc.stop or max(max_end, start)

    idxes = find_overlaps(df, start, stop)
    return df.reindex(idxes)