from heapq import *
import queue


class Frontier(object):
    def __init__(self):
        pass

    def view_frontier():
        raise NotImplementedError('Frontier.view_frontier not implemented')

    def empty(self):
        raise NotImplementedError('Frontier.empty not implemented')

    def add(self, url):
        raise NotImplementedError('Fronter.add not implemented')

    def add_many(self, urls):
        for url in urls:
            self.add(url)

    def get(self):
        raise NotImplementedError('Fronter.get not implemented')


#
# Simple FIFO Queue. Very impolite.
#
class FIFOFrontier(Frontier):
    def __init__(self):
        self.q = queue.Queue()

    def view_frontier(self):
        return list(self.q.queue)

    def empty(self):
        return self.q.empty()

    def add(self, url):
        self.q.put(url)

    def get(self):
        # returns and removes the first item from q
        return self.q.get()
