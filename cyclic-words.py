def running_letters(needle, eight_letter_words):
	valid_words = []
	alphabet = 'abcdefghijklmnopqrstuvwxyz'

	# Get all words which contain the needle in their rotation
	valid_words = [fodder for fodder in eight_letter_words 
		if needle in fodder + fodder]

	categories = dict()
	for i in range(0,8):
		categories[i] = []

	for word in valid_words:
		index = (word + word).find(needle)
		categories[index].append(word)

	for index in categories.keys():
		print('{0}: {1}'.format(index, sorted(categories[index])))

def main():
	dictionary = set()
	print("Enter running letters:")
	needle = input()

	with open('ospd.txt') as file_reader:
		for line in file_reader:
			dictionary.add(line.strip())

	eight_letter_words = [word for word in dictionary if len(word) == 8]

	running_letters(needle, eight_letter_words)


if __name__ == "__main__":
	main()
