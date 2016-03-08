import marisa_trie

with open('dictionary.marisa', 'r') as dictionary_file:
    trie = marisa_trie.Trie()
    trie.read(dictionary_file)

def find_doll_words():
    non_short_words = []
    for word in trie.keys():
        if len(word) > 2:
            non_short_words.append(word)

    medium_length_words = []
    for word in non_short_words:
        if len(word) < 5:
            medium_length_words.append(word)

    long_words = []
    for word in non_short_words:
        '''
        The letter s creates a lot of 'lazy' entries such as 
        call > miss = mis(call)s.
        call > cats = cat(call)s
        This is because of the fact that s is the suffix for pluralizing words
        Similarly 'ed' creates a verb form of the word such as : 
        space > red = respaced
        slime > bed = beslimed
        '''
        if len(word) > 5 and word[-1] != 's':
            long_words.append(word)

    # Better word combinations can be found using words that aren't short and words that are long
    # This also makes the program more efficient since the word space is smaller
    for inner in medium_length_words:
        for outer in long_words:
            if outer.find(inner) > 0:
                subtracted_word = outer.replace(inner,'')
                if subtracted_word in trie and (subtracted_word + inner) != outer:
                    print (inner, subtracted_word, outer)

# The subset of words is smaller, hence the program runs a lot faster than the brute force one
def find_doll_words_given_inner_word(inner_word):
    for outer_word in trie.keys():
        if len(outer_word) > 5:
            if outer_word.find(inner_word) > 0:
                subtracted_word = outer_word.replace(inner_word, '')
                if subtracted_word in trie and (subtracted_word + inner_word) != outer_word:
                    print (inner_word, subtracted_word, outer_word)

def main():
    ch = 1
    if ch == 1:
        find_doll_words()
    if ch == 2:
        print "Enter word:"
        word = unicode(raw_input())
        find_doll_words_given_inner_word(word)

if __name__ == "__main__":
    main()
