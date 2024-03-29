import mmh3  # murmer hash used by bloom filter
import numpy as np
import csv


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


class BloomFilter(UST):
    def __init__(self, prob, n_to_insert):
        # need a guesstimation of how many things will be inserted.
        self.prob = prob  # probability of a FALSE positive.
        self.n = n_to_insert
        self.num_cells = int(-(self.n * np.log(prob)) / (np.log(2)**2))
        self.hash_count = int(np.ceil(-np.log2(prob)))
        self.cells = np.zeros(self.num_cells, dtype=np.uint8)
        self.num_entries = 0

    def view(self):
        # Bloomfilter does not store urls. Only bits
        return list(self.cells)

    def add(self, item):
        indices = [
            mmh3.hash(item, i) % self.num_cells
            for i in np.arange(self.hash_count)
        ]
        self.cells[indices] = 1
        self.num_entries += 1

    def __contains__(self, item):
        # checks if item is probably contained.
        # if the retrieved cells contain a zero, then item is definitely not
        # contained. Otherwise, item probably is contained
        indices = [
            mmh3.hash(item, i) % self.num_cells
            for i in np.arange(self.hash_count)
        ]
        return not 0 in self.cells[indices]

    def contains(self, item):
        return self.__contains__(item)


#
# A VERY simple and inefficient disk-based ust.
#
class SimpleDiskUST(UST):
    def __init__(self, path, name='simple_disk_ust'):
        self.path = path
        self.name = name
        f = open(self.path + self.name, 'w+')
        f.close()

    def add(self, item):
        assert isinstance(item, str), 'SimpleDiskUST.add item must be str'
        f = open(self.path + self.name, 'w+')
        f.write(item + ',')
        f.close()

    def __contains__(self, item):
        with open(self.path + self.name, 'r+') as f:
            reader = csv.reader(f, delimiter=',')
            for s in reader:
                if item == s:
                    return True
            return False

    def contains(self, item):
        return self.__contains__(item)


#
# Disk-based Bloom Filter.
#
class DiskBloomFilter(UST):
    def __init__(self, prob, n_to_insert, path, name):
        self.path = path
        self.name = name
        self.prob = prob  # probability of a FALSE positive.
        self.n = n_to_insert
        self.num_cells = int(-(self.n * np.log(prob)) / (np.log(2)**2))
        self.hash_count = int(np.ceil(-np.log2(prob)))
        self.num_entries = 0

        # fill file with n_to_insert 0's
        with open(path + name, 'wb+') as f:
            for i in range(self.num_cells + 1):
                f.write('0'.encode())

    def add(self, item):
        indices = [
            mmh3.hash(item, i) % self.num_cells
            for i in np.arange(self.hash_count)
        ]
        with open(self.path + self.name, 'rb+') as f:
            for idx in indices:
                f.seek(idx)
                f.write('1'.encode())
            self.num_entries += 1

    def __contains__(self, item):
        indices = [
            mmh3.hash(item, i) % self.num_cells
            for i in np.arange(self.hash_count)
        ]
        with open(self.path + self.name, 'rb') as f:
            for idx in indices:
                f.seek(idx)
                x = f.read(1)
                if x == '0'.encode():
                    return False
            return True

    def contains(self, item):
        return self.__contains__(item)
