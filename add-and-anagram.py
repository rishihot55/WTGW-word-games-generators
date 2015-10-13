with open('ospd.txt') as word_file:
	dictionary = []
	for line in word_file:
		dictionary.append(line.strip())

dictionary_by_length = dict()

for i in range(1, 10):
	dictionary_by_length[i] = []

for word in dictionary:
	dictionary_by_length[len(word)].append(word)

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def add_and_anagram(word, current_word_sequence, word_length):
	if word not in dictionary_by_length[word_length] or word_length > 9:
		return

	if len(current_word_sequence) > 5:
		print current_word_sequence
		return
	letter_set = set(word)

	anagrams = []

	for test_word in dictionary_by_length[word_length]:
		if set(test_word) == letter_set:
			anagrams.append(test_word)

	for test_anagram in anagrams:
		for letter in alphabet:
			test_word = letter + test_anagram
			add_and_anagram(test_word, current_word_sequence + [test_word], word_length + 1)

			for i in range(1, word_length):
				test_word = test_anagram[:i] + letter + test_anagram[i:]
				add_and_anagram(test_word, current_word_sequence + [test_word], word_length + 1)

			test_word = test_anagram + letter

			add_and_anagram(test_word, current_word_sequence + [test_word], word_length + 1)

def main():
	print "Enter a word: "
	word = raw_input()
	add_and_anagram(word=word, current_word_sequence=[word], word_length=len(word))

if __name__ == '__main__':
	main()