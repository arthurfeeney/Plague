#
# Abstact UST URL-Seen-Test.
#
class UST(object):
    def __init__(self):
        pass

    def view(self):
        raise NotImplementedError('UST.view not implemented')

    def add(self, item):
        raise NotImplementedError('UST.add not implemented')

    def __contains__(self, item):
        raise NotImplementedError('UST.__contains__ not implemented')

    def contains(self, item):
        # just be a more explicit version of __contains__
        raise NotImplementedError('UST.contains not implemented')


#
# set has constant insertion and lookup. So it works well for this.
# There are other UST types, such as a bloom filter, that I may use in the
# future. Everything should be somewhat modular, so this is basically a
# wrapper for set.
#
class SetUST(UST):
    def __init__(self):
        super(SetUST, self).__init__()
        self.seen = set()

    def view(self):
        return list(self.seen)

    def add(self, item):
        self.seen.add(item)

    def __contains__(self, item):
        return item in self.seen

    def contains(self, item):
        return item in self.seen