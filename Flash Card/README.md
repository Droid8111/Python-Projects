This Python project is a flash card app built using the Tkinter library for the graphical user interface (GUI) and pandas for data management. The app helps users learn and memorize French vocabulary by displaying flash cards with French words and their English translations.

Features:
Flash Cards: The app displays French words on one side of a card, and after a few seconds, flips to show the English translation on the back.
Learning Progress: Users can mark words they’ve learned by pressing a "right" button, which removes the word from the list and saves the progress.
Word Data Management: The app reads and stores words from a CSV file. If the user finishes all the words, the app uses a different set of words to continue the learning process.
CSV Storage: The words are stored in a CSV file, ensuring that the user's progress is saved, and unlearned words are tracked for future sessions.
Workflow:
The app starts by displaying a random French word.
After a few seconds, the English translation is shown.
Users can mark whether they’ve learned the word or not by clicking the appropriate button.
Words that are marked as learned are removed from the list, and the progress is saved.
Tested for functionality, ensuring smooth flash card transitions and accurate word tracking.