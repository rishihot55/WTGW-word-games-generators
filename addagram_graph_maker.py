"""Addagrams."""
import marisa_trie
import pickle

def load_trie(filename):
    with open(filename) as dict_trie:
        trie = marisa_trie.Trie()
        trie.read(dict_trie)
        return trie

def load_text_file(filename):
    with open(filename) as text_file:
        words = [word.strip() for word in text_file]
        trie = marisa_trie.Trie(words)
        return trie

def load_dictionary(filename):
    extension = filename.split('.')[-1]
    if extension == 'marisa':
        return load_trie(filename)
    elif extension == 'txt':
        return load_text_file(filename)

dictionary = load_dictionary('dictionary.marisa')


class Graph():
    def __init__(self):
        self.adjList = dict()

    def add_vertex(self, v):
        self.adjList[v] = []

    def add_edge(self, v1, v2):
        self.adjList[v1].append(v2)

    def contains_vertex(self, v):
        return v in self.adjList

    def vertices(self):
        return self.adjList.keys()

    def __dfs(self, current_vertex, vertex_list, max_depth):
        if len(vertex_list) == max_depth:
            print([word_list_map[vertex] for vertex in vertex_list])
            return

        for vertex in self.adjList[current_vertex]:
            vertex_list.append(vertex)
            self.__dfs(vertex, vertex_list, max_depth)
            vertex_list.pop()

    def dfs(self, word_multiset, max_depth):
        self.__dfs(word_multiset, [word_multiset], max_depth)


def add_letter(multiset, letter):
    multiset += 10**(ord(letter) - 97)
    return multiset


def word_to_multiset(word):
    multiset = 0
    for letter in word:
        multiset += 10**(ord(letter) - 97)
    return multiset

dict_by_length = {}
for word in dictionary:
    l = len(word)
    entry = (word, word_to_multiset(word))
    if l in dict_by_length:
        dict_by_length[l].append(entry)
    else:
        dict_by_length[l] = [entry]
alphabet = 'abcdefghijklmnopqrstwxyz'

def letter_count(multiset):
    letter_count = 0
    while multiset > 0:
        letter_count += (multiset%10)
        multiset //= 10
    return letter_count

# two letter words containing a or i will appear anyway, so we ignore those
single_letter_word_data = [(word, word_set) for (word, word_set) in dict_by_length[1]]
single_letter_word_sets = [word_set for (_, word_set) in single_letter_word_data]
two_letter_word_data = [(word, word_set) for (word, word_set) in dict_by_length[2] if 'a' not in word and 'i' not in word]
two_letter_word_sets = [word_set for (_, word_set) in two_letter_word_data]

seed_word_data = single_letter_word_data + two_letter_word_data
seed_word_sets = single_letter_word_sets + two_letter_word_sets

g = Graph()
for word_set in seed_word_sets:
    g.add_vertex(word_set)

seen_multisets = set()
seen_multisets.update(seed_word_sets)

active_vertices = []
active_vertices.extend(seed_word_sets)

word_list_map = {}

for (word, word_set) in seed_word_data:
    if word_set in word_list_map:
        word_list_map[word_set].append(word)
    else:
        word_list_map[word_set] = [word]

while active_vertices:
    current_set = active_vertices.pop(0)
    for letter in alphabet:
        candidate_multiset = add_letter(current_set, letter)
        num_letters = letter_count(candidate_multiset)
        if num_letters > 8:
            break
        if g.contains_vertex(candidate_multiset):
            g.add_edge(current_set, candidate_multiset)
        elif candidate_multiset in seen_multisets:
            continue
        else:
            word_list = [word for (word, word_set) in dict_by_length[num_letters] if candidate_multiset == word_set]
            if len(word_list) > 0:
                g.add_vertex(candidate_multiset)
                g.add_edge(current_set, candidate_multiset)
                active_vertices.append(candidate_multiset)
                word_list_map[candidate_multiset] = word_list
        seen_multisets.add(candidate_multiset)

data = {
    'graph': g,
    'word_list_map': word_list_map
}

with open('addagram_graph.pkl', 'wb') as pkl_file:
    pickle.dump(data, pkl_file)