from heapq import *
import queue
import queuelib
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


class PriorityFunctor:
    def __init__(self):
        # domain -> information required for functor
        # keeps track of the last time the domain was popped.
        self.last_pulled = {}

    def priority(self, domain):
        raise NotImplementedError('Frontier.priority not implemented')

    def __call__(self, domain):
        raise NotImplementedError('Frontier.__call__ not implemented')


#
# Priority Queue based Frontier. A bit more polite than fifo.
# Keeps limit domains. Prioritizes new domains, domains not crawled in a
# while
# should be used as a functor for priority queue class.
#
class DomainPriorityFunctor(PriorityFunctor):
    def __init__(self):
        super(DomainPriorityFunctor, self).__init__()
        pass

    def priority(self, domain):
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

        return priority

    def __call__(self, domain):
        return self.priority(domain)


#
# Prioritezes domains not SEEN in a while. One site may link many other
# sites that are in a different domain. This spaces them out a bit.
# should be used as a functor for priority queue class.
#
class SeenPriorityFunctor(PriorityFunctor):
    def __init__(self, scale_jump=20):
        super(SeenPriorityFunctor, self).__init__()
        self.scale_jump = scale_jump

    def priority(self, domain):
        time_pulled = time.time()

        if domain in self.last_pulled:
            last_time_pulled, scale = self.last_pulled[domain]
            priority = last_time_pulled - time_pulled + scale
            scale += self.scale_jump  # artifically add seconds
        else:
            # if the domain is totally new, give it great priority.
            priority = -time_pulled
            scale = self.scale_jump

        # update the domain's last time pulled to now
        self.last_pulled[domain] = (time_pulled, scale)

        return priority

    def __call__(self, domain):
        return self.priority(domain)

    def lower_scale(self, domain):
        time, scale = self.last_pulled[domain]
        self.last_pulled[domain] = (time, scale - self.scale_jump)


#
# In-memory version of priority queue.
#
class Memory_PriorityFrontier(Frontier):
    def __init__(self, priority_functor, limit=None):
        # functor used to compute priority.
        self.priority_functor = priority_functor

        # option to store a finite number of elements since this structure
        # is in memory.
        # max number of things stored in last_pulled.
        # If it is None, there is no limit.
        self.limit = limit

        # use list and heapq functions for priority queue.
        self.q = []

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

        priority = self.priority_functor(domain)

        # push the url on the heap, not the domain
        heappush(self.q, (priority, url))

    def get(self):
        # return the url on the top of the heap, ignoring the priority
        return heappop(self.q)[1]


#
# convenient functions so you can make one call instead of the two that
# are requried to construct the priority_functors and the frontier
#
def memory_domain_priority_frontier(limit=None):
    return Memory_PriorityFrontier(DomainPriorityFunctor(), limit)


def memory_seen_priority_frontier(limit=None):
    return Memory_PriorityFrontier(SeenPriorityFunctor(), limit)
