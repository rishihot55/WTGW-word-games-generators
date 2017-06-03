import marisa_trie
import argparse

def find_doll_words(dictionary, reverse, min_word_length):
    for word in dictionary:
        for sub_word_start_index in range(1, len(word) - 1):
            for sub_word_end_index in range(sub_word_start_index + min_word_length, len(word) - 1):
                candidate_sub_word = word[sub_word_start_index:sub_word_end_index] if not reverse else word[sub_word_start_index:sub_word_end_index][::-1]
                if candidate_sub_word in dictionary:
                    outer_word = word[:sub_word_start_index] + word[sub_word_end_index:]
                    if outer_word in dictionary:
                        print(candidate_sub_word, "->", outer_word, "=", word)

def find_triple_doll_words(dictionary, min_word_length):
    for word in dictionary:
        wlen = len(word)
        for sub_word_start_index in range(1, wlen - 1):
            for sub_word_end_index in range(sub_word_start_index + min_word_length, wlen - 1):
                candidate_sub_word = word[sub_word_start_index:sub_word_end_index]
                for sub_sub_word_start_index in range(sub_word_start_index + 1, sub_word_end_index - 1):
                    for sub_sub_word_end_index in range(sub_sub_word_start_index + min_word_length, sub_word_end_index - 1):
                        sub_sub_word = word[sub_sub_word_start_index: sub_sub_word_end_index]
                        if sub_sub_word in dictionary:
                            middle_word = word[sub_word_start_index:sub_sub_word_start_index] + word[sub_sub_word_end_index:sub_word_end_index]
                            if middle_word in dictionary:
                                outer_word = word[:sub_word_start_index] + word[sub_word_end_index:]
                                if outer_word in dictionary:
                                    print(sub_sub_word, middle_word, outer_word, "= ", word)


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


def main():
    parser = argparse.ArgumentParser(description='Russian Dolls generator')
    parser.add_argument('--reverse', help='Finds reverse Russian Dolls', action='store_true')
    parser.add_argument('--triple', help='Finds triple doll words', action='store_true')
    parser.add_argument('--dictionary', default='dictionary.marisa')
    parser.add_argument('--length', help='Minimum word length', type=int, default=2)
    args = parser.parse_args()

    dictionary = load_dictionary(args.dictionary)

    if args.triple:
        find_triple_doll_words(dictionary, min_word_length=args.length)
    else:
        find_doll_words(dictionary, reverse=args.reverse, min_word_length=args.length)

if __name__ == "__main__":
    main()
