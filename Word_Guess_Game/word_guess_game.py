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
    def __init__(self, filename):
        self.filename = filename
        file = open(self.filename, "r")
        raw_text = file.read()
        self.tokens = nltk.word_tokenize(raw_text.lower())
        self.filetext = nltk.text.Text(self.tokens)
        seed(9999)

    def calculate_lexical_diversity(self):
        # Convert the tokens list to a set of unique words
        unique_words = set(self.tokens)
        # Count all tokens
        count = len(self.tokens)
        # Calculate the lexical_diversity
        lex_div = len(unique_words) / count
        rounded = round(lex_div, 2)
        print("Lexical Diversity: " + str(rounded))

    def preprocess_text(self):
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


    def word_guess(self, words):
        print("Let's play a word guessing game! (enter ! to stop)")
        # a. give the user 5 points to start with; the game ends when their total score is negative, or
        # they guess ‘!’ as a letter
        score = 5
        answer = ""
        curr_word = ""
        underscore_word = ""
        while score > -1 and answer != '!':
            # b. randomly choose one of the 50 words in the top 50 list (See the random numbers
            # notebook in the Xtras folder of the GitHub)
            if curr_word == "":
                num = randint(0, 49)
                curr_word = words[num]
                for _ in curr_word:
                    underscore_word += "_"
            # c. output to console an “underscore space” for each letter in the word
            print(underscore_word)
            # d. ask the user for a letter
            answer = input("Guess a letter: ")
            answer = answer.lower()
            # e. if the letter is in the word, print ‘Right!’, fill in all matching letter _ with the letter and
            # add 1 point to their score
            if answer in curr_word and answer not in underscore_word:
                score += 1
                print("Right! Score is " + str(score))
            # HEREX
            # f. if the letter is not in the word, subtract 1 from their score, print ‘Sorry, guess again’
            # g. guessing for a word ends if the user guesses the word or has a negative score
            # Natural Language Processing Dr. Karen Mazidi
            # Caution: All course work is run through plagiarism detection software comparing
            # students’ work as well as work from previous semesters and other sources.
            # h. keep a cumulative total score and end the game if it is negative (or the user entered ‘!’)
            # for a guess
            # i. right or wrong, give user feedback on their score for this word after each guess

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