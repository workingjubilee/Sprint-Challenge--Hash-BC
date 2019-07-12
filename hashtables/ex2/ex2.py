#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length*2) # initialize it to twice as fat to make access faster
    route = [None] * length
    for ticket in tickets:
        hash_table_insert(hashtable, ticket.source, ticket.destination)

    destination = "NONE"

    for i in range(length):
        destination = hash_table_retrieve(hashtable, destination)
        route[i] = destination

    return route
