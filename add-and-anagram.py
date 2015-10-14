import marisa_trie

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

# Used for evaluating whether anagram checking by using a set or using a hash is faster
# As expected, using the hash is faster
def check_anagram_set(word_set, word2):
	if word_set == set(word2):
		return True
	return False

def check_anagram_hash(word_hash, word2):
	test_hash = word_hash[:]

	for letter in word2:
		test_hash[ord(letter) - 97] -= 1

	# If there are no non-zero entries in the test hash, return true
	return len(filter(lambda a: a != 0, test_hash)) == 0

# A depth-first lookup for valid word sequences
def add_and_anagram(word, current_word_sequence, word_length):
	if word_length > 9:
		return

	if len(current_word_sequence) > 5:
		print current_word_sequence
		return
	
	anagrams = []

	# Hash of the letters of the given word
	word_hash = [0]*26

	for letter in word:
		word_hash[ord(letter) - 97] += 1

	# Testing if two words are anagrams by letter counting
	for test_word in dictionary_by_length[word_length]:
		test_hash = word_hash[:]

		for letter in test_word:
			test_hash[ord(letter) - 97] -= 1

		# If there are no non-zero entries in the test hash, then append to dictionady
		if len(filter(lambda a: a != 0, test_hash)) == 0:
			anagrams.append(test_word)

	for test_anagram in anagrams:
		for letter in alphabet:
			test_word = letter + test_anagram
			if test_word in trie:
				add_and_anagram(test_word, current_word_sequence + [test_word], word_length + 1)

			for i in range(1, word_length):
				test_word = test_anagram[:i] + letter + test_anagram[i:]
				if test_word in trie:
					add_and_anagram(test_word, current_word_sequence + [test_word], word_length + 1)

			test_word = test_anagram + letter
			if test_word in trie:
				add_and_anagram(test_word, current_word_sequence + [test_word], word_length + 1)

def main():
	print "Enter a word: "
	word = unicode(raw_input())
	add_and_anagram(word=word, current_word_sequence=[word], word_length=len(word))

if __name__ == '__main__':
	main()