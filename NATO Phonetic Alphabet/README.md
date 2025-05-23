This Python project converts input words into their corresponding NATO phonetic alphabet codes. It utilizes the pandas library to read data from a CSV file containing the phonetic alphabet and then maps each letter of a word to its corresponding phonetic code.

Features:
Phonetic Alphabet Mapping: The app takes any word input from the user and converts each letter into its corresponding NATO phonetic code (e.g., A → Alpha, B → Bravo).
Error Handling: If the user enters a non-alphabet character, the program will prompt them to enter a valid word containing only letters.
CSV Data: The NATO phonetic alphabet is stored in a CSV file, which is read and processed to create a dictionary for efficient lookups.
Workflow:
The user is prompted to enter a word.
The word is converted to uppercase, and each letter is mapped to its NATO phonetic code.
The phonetic codes are printed as a list.
If the user enters a character that's not a letter, the program will request a valid input.
Tested to ensure proper handling of user input and accurate phonetic conversions