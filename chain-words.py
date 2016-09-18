from functools import partial

def find_chain_words(base_word, dictionary, chain_length):
    # Ideally for chain words, it's better to use six letter words
    word_pool = [word for word in dictionary if len(word) == 6 or len(word) == 7]

    prefix = base_word[:chain_length] # get the first 3 letters of the word

    front_words = []
    
    for word in word_pool:
        if word[-chain_length:] == prefix:
            front_words.append(word)
    
    print(chain_length,"-chain front words for the given word are: ", front_words)

    suffix = base_word[-chain_length:]
    back_words = []
    for word in word_pool:
        if word[:chain_length] == suffix:
            back_words.append(word)

    print(chain_length,"-chain back words for the given word are: ", back_words)

if __name__ == "__main__":
    word = input("Please enter the word to find chains for: ")
    dictionary = []
    with open('ospd.txt') as file_reader:
        for line in file_reader:
            dictionary.append(line.strip())
    find_chain_words(word, dictionary,3)
    find_chain_words(word, dictionary,4)
