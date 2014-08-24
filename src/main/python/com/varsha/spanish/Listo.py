
def L(data):

    return Listo(data)

class Listo():

    def n(self):

        return len(self.data)


    def where(self, predicate):

        return Listo(filter(predicate, self.data))


    def but_not(self, predicate):

        return self.where(lambda x: not predicate(x))


    def agg(self, aggregate, initial=None):

        if initial is not None:
            return reduce(aggregate, self.data, initial)
        else:
            return reduce(aggregate, self.data[1:], self.data[0])


    def map(self, mapping):

        return Listo(map(mapping, self.data))


    def imap(self, mapping):

        mapped = [None] * len(self.data)

        for i, d in enumerate(self.data):
            mapped[i] = mapping(i, d)

        return Listo(mapped)


    def list(self):

        return self.data


    def chunk(self, n):

        return Listo(list(Listo(self.data[i:i + n]) for i in xrange(0, len(self.data), n)))


    def __init__(self, data):

        self.data = data


    def __len__(self):

        return len(self.data)


    def __getitem__(self, index):

        return self.data[index]


    def __contains__(self, element):

        return element in self.data


    def __iter__(self):

        return iter(self.data)


    def __str__(self):

        return str(self.data)


    def __repr__(self):

        return str(self.data)


    def __unicode__(self):

        return unicode(str(self.data))
