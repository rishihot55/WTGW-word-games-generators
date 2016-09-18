import marisa_trie

import itertools

with open('dictionary.marisa', 'r') as dictionary_file:
	trie = marisa_trie.Trie()
	trie.read(dictionary_file)

# A prefix trie of all words. Gives a lookup time of O(word_length).
# Considering that the dictionary does not contain words longer than 10 letters
# we can reasonably assume the time complexity to be O(1) for lookup


# Dictionary ordered by length to speed up retrieval of words of a specific length
dictionary_by_length = dict()

for i in range(1, 10):
	dictionary_by_length[i] = []

for word in trie.keys():
	dictionary_by_length[len(word)].append(word)

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def get_word_hash(word):
	word_hash = [0]*26

	for letter in word:
		word_hash[ord(letter) - 97] += 1

	return word_hash

def check_anagram_hash(word_hash, word2):
	test_hash = word_hash[:]

	for letter in word2:
		test_hash[ord(letter) - 97] -= 1

	unmatched_letters = [i for i in test_hash if i != 0]
	# If there are no non-zero entries in the test hash, return true
	return len(unmatched_letters) == 0

# A depth-first lookup for valid word sequences
def add_and_anagram(word, current_word_sequence, word_length):
	if word_length > 9:
		return

	if len(current_word_sequence) > 5:
		print(current_word_sequence)
		return
	
	anagrams = []

	# Hash of the letters of the given word
	
	word_hash = get_word_hash(word)

	# Testing if two words are anagrams by letter counting
	for test_word in dictionary_by_length[word_length]:
		if check_anagram_hash(word_hash, test_word):
			anagrams.append(test_word)

	for test_anagram in anagrams:
		for letter in alphabet:
			for i in range(0, word_length + 1):
				test_word = test_anagram[:i] + letter + test_anagram[i:]
				if test_word in trie:
					add_and_anagram(
						test_word, current_word_sequence + [test_word],
						word_length + 1)

def main():
	print("Enter a word: ")
	word = input()
	add_and_anagram(word=word, current_word_sequence=[word], word_length=len(word))

if __name__ == '__main__':
	main()