"""Addagrams."""
import argparse
import pickle

alphabet = 'abcdefghijklmnopqrstuvwxyz'


def load_dictionary(filename):
    with open(filename) as file:
        words = [word.strip().lower() for word in file]
        return words

def w2c(word):
    counter = 0
    for letter in word:
        counter += 10**(ord(letter) - 97)
    return counter


def add_letter(counter, letter):
    counter += 10**(ord(letter) - 97)
    return counter


def letter_count(counter):
    letter_count = 0
    while counter > 0:
        letter_count += (counter%10)
        counter //= 10
    return letter_count


def get_counter_anagram_map(dictionary):
    counter_anagram_map = dict()
    for word in dictionary:
        counter = w2c(word)
        if counter in counter_anagram_map:
            counter_anagram_map[counter].append(word)
        else:
            counter_anagram_map[counter] = [word]
    return counter_anagram_map


def find_addagrams_util(counter, addagram_list, max_length, counter_anagram_map):
    if letter_count(counter + 1) > max_length:
        print(addagram_list)
        return

    for letter in alphabet:
        candidate_counter = add_letter(counter, letter)
        if candidate_counter in counter_anagram_map:
            addagram_list.append(counter_anagram_map[candidate_counter])
            find_addagrams_util(candidate_counter, addagram_list, max_length, counter_anagram_map)
            addagram_list.pop()


def find_addagrams(word, max_length, counter_anagram_map):
    find_addagrams_util(w2c(word), [[word]], max_length, counter_anagram_map)


class Graph:
    def __init__(self):
        self.adjList = dict()

    def add_vertex(self, v):
        self.adjList[v] = []

    def add_edge(self, v1, v2):
        self.adjList[v1].append(v2)

    def contains_vertex(self, v):
        return v in self.adjList

    def __dfs(self, v, vertex_list, current_length, max_length, counter_anagram_map):
        if current_length > max_length:
            print([counter_anagram_map[vertex] for vertex in vertex_list])
            return

        for vertex in self.adjList[v]:
            vertex_list.append(vertex)
            self.__dfs(vertex, vertex_list, current_length + 1, max_length, counter_anagram_map)
            vertex_list.pop()

    def dfs(self, v, max_length, counter_anagram_map):
        self.__dfs(v, [v], letter_count(v) + 1, max_length, counter_anagram_map)


def generate_addagram_graph(word_list):
    print("Building addagram graph, this may take a while!")
    g = Graph()
    counter_anagram_map = get_counter_anagram_map(word_list)
    seed_word_counters = counter_anagram_map.keys()
    for counter in seed_word_counters:
        g.add_vertex(counter)
    active_vertices = list(seed_word_counters)
    while active_vertices:
        counter = active_vertices.pop()
        for letter in alphabet:
            candidate_counter = add_letter(counter, letter)
            if g.contains_vertex(candidate_counter):
                g.add_edge(counter, candidate_counter)

    print("Graph built! Writing to disk.")
    with open('addagram_graph.pkl', 'wb') as pkl_file:
        pickle.dump(g, pkl_file)
    with open('counter_anagram_map.pkl', 'wb') as pkl_file:
        pickle.dump(counter_anagram_map, pkl_file)
    print("Saved to disk!")


def load_graph():
    with open('addagram_graph.pkl', 'rb') as pkl_file:
        g = pickle.load(pkl_file)
        return g


def load_counter_anagram_map():
    with open('counter_anagram_map.pkl', 'rb') as pkl_file:
        counter_anagram_map = pickle.load(pkl_file)
        return counter_anagram_map

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Addagrams generator')
    parser.add_argument('--word', help='Word from which to generate addagrams')
    parser.add_argument('-l', help='Maximum length of generated words (default: 7)', type=int, default=7)
    parser.add_argument('--dictionary', help='Word list to generate addagrams from', default='/usr/share/dict/words')
    parser.add_argument('--build', help='Build addagram graph from word list', action='store_true')
    parser.add_argument('--trial', help='Find all addagrams by trial and error', action='store_true')
    args = parser.parse_args()
    if args.word:
        if args.trial:
            counter_anagram_map = load_counter_anagram_map()
            find_addagrams(args.word, args.l, counter_anagram_map)
        else:
            counter_anagram_map = load_counter_anagram_map()
            g = load_graph()
            g.dfs(w2c(args.word), args.l, counter_anagram_map)
    elif args.build:
        word_list = load_dictionary(args.dictionary)
        generate_addagram_graph(word_list)

    else:
        parser.print_help()