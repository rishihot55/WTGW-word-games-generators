import marisa_trie

with open('dictionary.marisa', 'r') as dictionary_file:
    trie = marisa_trie.Trie()
    trie.read(dictionary_file)

def find_doll_words():
    non_short_words = []
    for word in trie.keys():
        if len(word) > 3:
            non_short_words.append(word)

    long_words = []
    for word in non_short_words:
        if len(word) > 5:
            long_words.append(word)

    # Better word combinations can be found using words that aren't short and words that are long
    # This also makes the program more efficient since the word space is smaller
    for inner in non_short_words:
        for outer in long_words:
            if outer.find(inner) > 0:
                subtracted_word = outer.replace(inner,'')
                if subtracted_word in trie and (subtracted_word + inner) != outer:
                    print (inner, subtracted_word, outer)


def main():
    find_doll_words()

if __name__ == "__main__":
    main()
