import marisa_trie

with open('dictionary.marisa', 'r') as dictionary_file:
    trie = marisa_trie.Trie()
    trie.read(dictionary_file)

def find_doll_words():
    non_short_words = []
    non_short_words = filter(
        lambda w: len(w) > 2,
        trie.keys())

    medium_length_words = []

    medium_length_words = filter(
        lambda w: len(w) < 5,
        non_short_words)

    long_words = []

    '''
        The letter s creates a lot of 'lazy' entries such as 
        call > miss = mis(call)s.
        call > cats = cat(call)s
        This is because of the fact that s is the suffix for pluralizing words
        Similarly 'ed' creates a verb form of the word such as : 
        space > red = respaced
        slime > bed = beslimed
    '''
    long_words = filter(
        lambda w: len(w) > 5 and w[-1] != 's',
        non_short_words)

    # Better word combinations can be found using words that aren't short and words that are long
    # This also makes the program more efficient since the word space is smaller
    for inner in medium_length_words:
        for outer in long_words:
            if outer.find(inner) > 0:
                subtracted_word = outer.replace(inner,'')
                if subtracted_word in trie and (subtracted_word + inner) != outer:
                    print (inner, subtracted_word, outer)

def main():
    find_doll_words()

if __name__ == "__main__":
    main()
