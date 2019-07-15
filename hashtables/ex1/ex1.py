#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(length*2) # twice as fat, etc., etc.
    one = None
    two = None
    if length == 1:
        return None
    for package, weight in enumerate(weights):
        attempt_retrieval = hash_table_retrieve(ht, weight)
        if attempt_retrieval == None:
            hash_table_insert(ht, weight, package)
        else:
            return package, attempt_retrieval
        if weight <= limit:
            if one == None:
                one = weight
            elif two == None:
                two = weight

    if one == None and two == None:
        return None
    weights = sorted(weights)
    for i in range(length):
        starter_weight = weights[i]
        starter = hash_table_retrieve(ht, starter_weight)
        attempt_weight = limit-starter_weight
        attempt = hash_table_retrieve(ht, attempt_weight)
        if attempt != None:
            if attempt > starter:
                return attempt, starter
            else:
                return starter, attempt
        else:
            pass

    return None


def print_answer(answer):
    if answer is None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
