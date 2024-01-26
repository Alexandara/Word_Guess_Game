"""
Code by Alexis Tudor
Created for CS 6320: Natural Language processing
Homework 1: Word Guess Game
"""
import sys
import nltk
from nltk.corpus import stopwords
from random import seed
from random import randint

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

class Word_Guess_Game:
    """
    Word_Guess_Game has functionality to perform various text processing as well
    as a guessing game.
    """
    def __init__(self, filename):
        """
        Initialization for the Word Guess Game class
        :param filename: the name of the file containing the text to use
        """
        self.filename = filename
        file = open(self.filename, "r")
        raw_text = file.read()
        self.tokens = nltk.word_tokenize(raw_text.lower())
        self.filetext = nltk.text.Text(self.tokens)
        seed(9999)

    def calculate_lexical_diversity(self):
        """
        This function calculates the lexical diversity of the body of text,
        defined as the number of unique words divided by total words.
        """
        # Convert the tokens list to a set of unique words
        unique_words = set(self.tokens)
        # Count all tokens
        count = len(self.tokens)
        # Calculate the lexical_diversity
        lex_div = len(unique_words) / count
        rounded = round(lex_div, 2)
        print("Lexical Diversity: " + str(rounded))

    def preprocess_text(self):
        """
        This function normalizes the text, removing non-alphabetical words, stop words, and words
        shorter than 6 letters long and returns the filtered words and a list of all nouns.
        :return: a list of processed words and a list of nouns
        """
        # tokenize the lower-case raw text, reduce the tokens to only those that are alpha, not in
        # the NLTK stopword list, and have length > 5
        filtered_tokens = []
        for token in self.tokens:
            if token.isalpha() and token not in stopwords.words('english') and len(token) > 5:
                filtered_tokens.append(token)
        # lemmatize the tokens and use set() to make a list of unique lemmas
        lemmatizer = nltk.WordNetLemmatizer()
        lemmed = [lemmatizer.lemmatize(token) for token in filtered_tokens]
        lemmed_set = set(lemmed)
        # do pos tagging on the unique lemmas and print the first 20 words and their tag
        tagged = nltk.pos_tag(lemmed_set)
        print("First 20 tagged unique lemmas: ")
        for i in range(20):
            word, tag = tagged[i]
            print(str(i+1) + ") " + word + ", " + tag)
        # create a list of only those lemmas that are nouns
        nouns = []
        for token in tagged:
            word, tag = token
            if "NN" in tag:
                nouns.append(word)
        # print the number of tokens (from step a) and the number of nouns (step d)
        print("\nNumber of tokens: " + str(len(filtered_tokens)))
        print("Number of nouns: " + str(len(nouns)))
        # return (1) tokens (not unique tokens) from step a, and (2) nouns from the function
        return filtered_tokens, nouns

    def get_nouns(self, tokens, nouns):
        """
        Takes in a list of words and a list of nouns and calculates how common
        each noun is in the list of words, then returns a list of the 50 most
        common nouns.
        :param tokens: list of words
        :param nouns: list of nouns
        :return: list of 50 most common nouns
        """
        # Make a dictionary of {noun:count of noun in tokens} items from the nouns and tokens lists; sort
        # the dict by count and print the 50 most common words and their counts. Save these words to a
        # list because they will be used in the guessing game.

        # Create the dictionary
        noun_dict = {}
        for noun in nouns:
            noun_dict[noun] = tokens.count(noun)
        # Sort the dictionary
        # This code snippet taken directly from https://realpython.com/sort-python-dictionary/
        sorted_noun_dict = dict(sorted(noun_dict.items(), key=lambda item: item[1]))
        # Print the 50 most common nouns and save to a dictionary
        i = 0
        print("The 50 Most Common Nouns: ")
        common_noun_list = []
        for token, count in reversed(sorted_noun_dict.items()):
            if i >= 50:
                break
            common_noun_list.append(token)
            print(str(i+1) + ") " + token + ", " + str(count))
            i += 1
        return common_noun_list

    def print_list(self, word):
        """
        Prints a list of characters as a string with spaces between
        the characters.
        :param word: a list of characters
        """
        new_word = ""
        for character in word:
            new_word += character
            new_word += " "
        print(new_word)

    def word_guess(self, words):
        """
        Plays a word guessing game with the user based on the words
        passed into the function.
        :param words: list of words to use in the guessing game
        """
        print("Let's play a word guessing game! (enter ! to stop)")
        # a. give the user 5 points to start with; the game ends when their total score is negative, or
        # they guess ‘!’ as a letter
        score = 5
        answer = ""
        curr_word = []
        underscore_word = []
        words_guessed = 0
        while score > -1 and answer != '!':
            # b. randomly choose one of the 50 words in the top 50 list (See the random numbers
            # notebook in the Xtras folder of the GitHub)
            if len(curr_word) == 0:
                num = randint(0, 49)
                for character in words[num]:
                    curr_word.append(character)
                for _ in curr_word:
                    underscore_word.append("_")
            # c. output to console an “underscore space” for each letter in the word
            self.print_list(underscore_word)
            # d. ask the user for a letter
            answer = input("Guess a letter: ")
            answer = answer.lower()
            # e. if the letter is in the word, print ‘Right!’, fill in all matching letter _ with the letter and
            # add 1 point to their score
            if answer in curr_word and answer not in underscore_word:
                score += 1
                print("Right! Score is " + str(score) + ".\n")
                for i in range(len(curr_word)):
                    if curr_word[i] == answer:
                        underscore_word[i] = answer
            # g. guessing for a word ends if the user guesses the word or has a negative score
            elif answer == "!":
                print("Thanks for playing! Final score is " + str(score) + " and you guessed " + str(words_guessed) + ".")
                break
            # f. if the letter is not in the word, subtract 1 from their score, print ‘Sorry, guess again’
            else:
                score -= 1
                if score > -1:
                    print("Sorry, guess again. Score is " + str(score) + ".\n")
                else:
                    print("Your score is -1. Try again sometime!")
            # h. keep a cumulative total score and end the game if it is negative (or the user entered ‘!’)
            # for a guess
            if curr_word == underscore_word:
                words_guessed += 1
                self.print_list(underscore_word)
                print("You solved it!")
                print("\nCurrent score: " + str(score))
                print("Words guessed: " + str(words_guessed))
                answer = input("\nGuess another word? (Y/N): ")
                answer = answer.lower()
                if answer == 'n' or answer == '!':
                    print("Thanks for playing!")
                    break
                curr_word = []
                underscore_word = []
                answer = ""

if __name__ == '__main__':
    # Instruction 1
    # Opens the file passed in as a system argument or else terminates
    try:
        file = open(str(sys.argv[1]), "r")
    except:
        print("Please provide the filename as a system argument.")
        exit(1)
    file.close()
    # Creates a word guess game object
    wgg = Word_Guess_Game(str(sys.argv[1]))
    # Code is called by instruction corresponding
    print("Instruction 2: ")
    wgg.calculate_lexical_diversity()
    print("\nInstruction 3: ")
    filtered_tokens, nouns = wgg.preprocess_text()
    print("\nInstruction 4: ")
    common_noun_list = wgg.get_nouns(filtered_tokens, nouns)
    print("\nInstruction 5: ")
    answer = input("Would you like to play the word guessing game? Y/N: ")
    answer = answer.lower()
    if answer == 'y':
        wgg.word_guess(common_noun_list)