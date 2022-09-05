from queue import PriorityQueue
import numpy as np

def edit(word,weights):
    founded = {word}
    edited = []
    letters = 'aąbcćdeęfghijklmnńoópqrstuvwxyzźż'

    # Insertion
    for letter in letters:
        for i in range(len(word)+1):
            new_word = word[:i]+letter+word[i:]
            if new_word not in founded:
                edited.append((weights['insertion'],new_word))
                founded.add(new_word)

    # Deletion
    for i in range(1,len(word)+1):
        new_word = word[:i-1]+word[i:]
        if new_word not in founded:
            founded.add(new_word)
            edited.append((weights['deletion'], new_word))

    # Substitution
    for letter in letters:
        for i in range(1,len(word)+1):
            new_word = word[:i-1]+letter+word[i:]
            if new_word not in founded:
                founded.add(new_word)
                edited.append((weights['substitution'], new_word))
    return edited


def edit_distance(init_word,dest_word,weights,verbose=False):
    founded = {}
    queue = PriorityQueue()
    queue.put((0,init_word))
    if verbose:
        max_depth = 0
    while not queue.empty():
        priority, current_word = queue.get()
        if verbose:
            if int(priority) > max_depth:
                print(priority)
                max_depth = int(priority)
        if founded.get(current_word,np.inf) > priority:
            if current_word == dest_word:
                return priority
            founded[current_word] = priority
            edited = edit(current_word,weights)
            for p, word in edited:
                if founded.get(word,np.inf) > priority+p:
                    queue.put((priority+p, word))

if __name__ == '__main__':
    weights = {'insertion':0.1,
               'deletion':0.2,
               'substitution':0.3}
    init_word = 'abdc'
    dest_word = 'abcde'

    # for p, word in edit(init_word,weights):
    #     print(p,word)

    print(edit_distance(init_word,dest_word,weights))