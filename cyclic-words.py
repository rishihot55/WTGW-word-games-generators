def running_letters(needle, eight_letter_words):
	valid_words = []
	alphabet = 'abcdefghijklmnopqrstuvwxyz'

	for fodder in eight_letter_words:
		haystack = fodder + fodder
		if needle in haystack:
			valid_words.append(fodder)
			
	categories = dict()
	for i in range(0,8):
		categories[i] = []

	for word in valid_words:
		index = (word + word).find(needle)
		print index
		categories[index].append(word)

	for index in categories.keys():
		print index, ":", sorted(categories[index])

def main():
	dictionary = set()
	print "Enter running letters:"
	needle = raw_input()

	with open('ospd.txt') as file_reader:
		for line in file_reader:
			dictionary.add(line.strip())

	eight_letter_words = filter(lambda x: len(x) == 8, dictionary)

	running_letters(needle, eight_letter_words)


if __name__ == "__main__":
	main()
