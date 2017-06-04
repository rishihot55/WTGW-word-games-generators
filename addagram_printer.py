import pickle
import argparse


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

def word_to_multiset(word):
    multiset = 0
    for letter in word:
        multiset += 10**(ord(letter) - 97)
    return multiset

with open('addagram_graph.pkl', 'rb') as pkl_file:
    data = pickle.load(pkl_file)
g = data['graph']
word_list_map = data['word_list_map']

def generate_addagrams(word, sequence_length):
    word_set = word_to_multiset(word)
    g.dfs(word_set, sequence_length)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Addagrams generator')
    parser.add_argument('starting_word', help='Word from which to generate addagrams')
    parser.add_argument('-l', help='Maximum length of generated words', type=int, default=7)
    args = parser.parse_args()
    if args.starting_word:
        generate_addagrams(args.starting_word, args.l - 2 + len(args.starting_word))
    else:
        parser.print_help()