def find_doll_words(dictionary):
    matroska_set = []
    for inner in dictionary:
        if len(inner) < 4:
            continue
        for outer in dictionary:
            if outer.find(inner) > 0:
                subtracted_word = outer.replace(inner,'')
                if len(subtracted_word) > 2 and subtracted_word in dictionary and (subtracted_word + inner) != outer:
                    matroska_set.append((inner, subtracted_word, outer))
                    print (inner, subtracted_word, outer)


def main():
    dictionary = set()

    with open('ospd.txt','r') as file_reader:
        for line in file_reader:
            dictionary.add(line.strip())

    assert 'apple' in dictionary
    find_doll_words(dictionary)

if __name__ == "__main__":
    main()
