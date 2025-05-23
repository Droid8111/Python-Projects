import pandas

data = pandas.read_csv("nato_phonetic_alphabet.csv")

phonetic_dict = {row.letter: row.code for (index, row) in data.iterrows()}


loop = True
while loop:

    try:

        word = input("Enter a word: ").upper()
        output_list = [phonetic_dict[letter] for letter in word]
        print(output_list)
        loop = False

    except KeyError:
        print("Sorry, only letters in the alphabet please.")