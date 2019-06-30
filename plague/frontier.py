from heapq import *
import queue
import plague.url_util as uu
import time


class Frontier(object):
    def __init__(self):
        pass

    def view_frontier():
        raise NotImplementedError('Frontier.view_frontier not implemented')

    def empty(self):
        raise NotImplementedError('Frontier.empty not implemented')

    def add(self, url, **kwargs):
        raise NotImplementedError('Fronter.add not implemented')

    def add_many(self, urls, **kwargs):
        for url in urls:
            self.add(url)

    def get(self):
        raise NotImplementedError('Fronter.get not implemented')


#
# Simple FIFO Queue. Very impolite. :(
# Essentially just a wrapper for that implements view_frontier()
#
class FIFOFrontier(Frontier):
    def __init__(self):
        self.q = queue.Queue()

    def view_frontier(self):
        return list(self.q.queue)

    def empty(self):
        return self.q.empty()

    def add(self, url, **kwargs):
        self.q.put(url)

    def get(self):
        # returns and removes the first item from q
        return self.q.get()


#
# Priority Queue based Frontier. A bit more polite than fifo.
# Keeps limit domains. Prioritizes new domains, domains not seen in a while,
# then recently seen domains
#
class DomainPriorityFrontier(Frontier):
    def __init__(self, limit=None):
        self.q = []

        # domain -> time
        # keeps track of the last time the domain was popped.
        self.last_pulled = {}

        # max number of things stored in last_pulled.
        # If it is None, there is no limit.
        self.limit = limit

    def view_frontier(self):
        return self.q

    def empty(self):
        return len(self.q) == 0

    def k_oldest(self, k):
        # the oldest keys will have the earliest time pulled. So
        # sort and get the first k elements.
        oldest = sorted(self.last_pulled.items(),
                        key=lambda kv: (kv[1], kv[0]))[:k]
        x, _ = zip(*oldest)
        return list(x)

    def add(self, url):

        domain = uu.domain_name(url)

        if self.limit and len(self.last_pulled) >= self.limit:
            oldest_keys = self.k_oldest(int(self.limit / 2) + 1)
            for key in oldest_keys:
                del self.last_pulled[key]

        time_pulled = time.time()

        if domain in self.last_pulled:
            # large negative if it has not been seen in a while.
            # small negative if it has been seen recently :)
            priority = self.last_pulled[domain] - time_pulled

        else:
            # if the domain is totally new, give it great priority.
            priority = -time_pulled

        # update the last time pulled to now
        self.last_pulled[domain] = time_pulled

        # push the url on the heap, not the domain
        heappush(self.q, (priority, url))

    def get(self):
        # return the url on the top of the heap, ignoring the priority
        return heappop(self.q)[1]
