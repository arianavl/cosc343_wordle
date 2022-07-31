__author__ = "<your name>"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<your e-mail>"

# first start with a good word - most used letters in alphabet
# Go a step further and go with most common letters in that row
# if -1 get rid of any word with that letter in that index, get rid of any word where the letter is not present anywhere
# Add 500 to every other hueristic that is not currently 0
# if 0, remove every word with that letter at that index
# if 1, remove any words that do not have that letter at that index and make letter value 1000

import helper
from collections import Counter




def determine_initial_heuristic(diction, word_length):
	"""
	A method that counts the occurrences of letters at an index and
	returns that information
	:param diction: The current list of words/precepts
	:param word_length: the length of the word
	:param count: the previous count
	:return: the next word
	"""
	count = {}

	for i in range(word_length):
		count[i] = {}
		for word in diction:
			if word[i] not in count[i]:
				count[i][word[i]] = 1
			else:
				count[i][word[i]] += 1

	print(count[0])
	return count


def revise_dict(diction, letter_indices, letter_states, heuristic, letters):
	"""
	Method that removes any impossible words from the dictionary
	:param letters:
	:param diction: The current Dictionary
	:param letter_indices:
	:param letter_states:
	:param heuristic:
	:return: The revised dictionary
	"""


	# print(letters)
	# print(last_word)
	# print("letter_states: " + str(letter_states))

	# Can probably take this out - see difference in time

	# Create a dictionary of the letters and their states
	last_word = helper.letter_indices_to_word(letter_indices, letters)

	states = {}
	for i in range(len(last_word)):
		if last_word[i] not in states:
			states[last_word[i]] = []
		states[last_word[i]].append(letter_states[i])
	print("states: " + str(states))
	"""
	if last_word in diction:
		print("last_word: " + last_word)
		diction.remove(last_word)
		"""
	wrong_word_list = set()


 # create dict with letters from last word as keys, then add states to all the letters

    # if any of the states have the same letter associated to them - count that amount and make sure there are that many
	"""
	for word in diction:
		word_count = Counter(word)
		# print(word_count)
		for i in range(len(word)):
			if i in states[0]:
				if letters[letter_indices[i]] == word[i]:
					wrong_word_list.add(word)
			if i in states[1]:
				if letters[letter_indices[i]] != word[i]:
					wrong_word_list.add(word)
			if i in states[-1]:
				if letters[letter_indices[i]] == word[i] or letters[letter_indices[i]] not in word:
					wrong_word_list.add(word)
	"""

	for i in range(len(letter_states)):  # for every letter in word
		if letter_states[i] == 0:  # if letter does not go there
			heuristic[i][letters[letter_indices[i]]] = 0  # Don't think this actually does anything
			for word in diction:  # go through every word and add to wrong_word list if word has letter at index
				if len(states[letters[letter_indices[i]]]) == 1:
					if letters[letter_indices[i]] in word:
						wrong_word_list.add(word)
				elif letters[letter_indices[i]] != word[i]:
					wrong_word_list.add(word)
		elif letter_states[i] == 1:
			# heuristic[i][letters[letter_indices[i]]] = 1000  # dont think this actually does anything
			for word in diction:
				if letters[letter_indices[i]] != word[i]:
					wrong_word_list.add(word)
		else:
			for word in diction:
				heuristic[i][letters[letter_indices[i]]] += 5000  # change heuristic values
				if letters[letter_indices[i]] == word[i] or letters[letter_indices[i]] not in word:
					wrong_word_list.add(word)
	# """
	for word in wrong_word_list:
		# print("word being removed: " + word)
		diction.remove(word)

	# print(diction)
	print(heuristic[0])
	return diction




def choose_word(diction, heuristic):
	best_word = ""
	best_value = 0

	for word in diction:
		value = 0
		for i in range(len(word)):
			# print(word[i])
			# print(heuristic[i][word[i]])
			value += heuristic[i][word[i]]
		if value > best_value:
			best_value = value
			best_word = word

	return best_word


class WordleAgent():

	"""
       A class that encapsulates the code dictating the
       behaviour of the Wordle playing agent

       ...

       Attributes
       ----------
       dictionary : list
           a list of valid words for the game
       letter : list
           a list containing valid characters in the game
       word_length : int
           the number of letters per guess word
       num_guesses : int
           the max. number of guesses per game
       mode: str
           indicates whether the game is played in 'easy' or 'hard' mode

       Methods
       -------
       AgentFunction(percepts)
           Returns the next word guess given state of the game in percepts
       """

	def __init__(self, dictionary, letters, word_length, num_guesses, mode):
		"""
    		:param dictionary: a list of valid words for the game
    		:param letters: a list containing valid characters in the game
    		:param word_length: the number of letters per guess word
    		:param num_guesses: the max. number of guesses per game
    		:param mode: indicates whether the game is played in 'easy' or 'hard' mode
    		:param heuristic: the value of each letter in each index
    	"""

		self.dictionary = dictionary
		self.letters = letters
		self.word_length = word_length
		self.num_guesses = num_guesses
		self.mode = mode
		self.heuristic = {}
		self.revised_dict = self.dictionary.copy()


	def AgentFunction(self, percepts):
		"""
		Returns the next word guess given state of the game in percepts

    	:param percepts: a tuple of three items: guess_counter, letter_indexes, and letter_states;
               guess_counter is an integer indicating which guess this is, starting with 0 for initial guess;
               letter_indexes is a list of indexes of letters from self.letters corresponding to
                           the previous guess, a list of -1's on guess 0;
               letter_states is a list of the same length as letter_indexes, providing feedback about the
                           previous guess (conveyed through letter indexes) with values of 0 (the corresponding
                           letter was not found in the solution), -1 (the correspond letter is found in the
                           solution, but not in that spot), 1 (the corresponding letter is found in the solution
                           in that spot).
		:return: string - a word from self.dictionary that is the next guess
		"""

		# This is how you extract three different parts of percepts.
		guess_counter, letter_indexes, letter_states = percepts

		if guess_counter == 0:

			self.heuristic = determine_initial_heuristic(self.dictionary, self.word_length)
			best_word = choose_word(self.dictionary, self.heuristic)
			self.revised_dict = self.dictionary.copy()  # reset dictionary
		else:
			self.revised_dict = revise_dict(self.revised_dict, letter_indexes, letter_states, self.heuristic, self.letters)
			best_word = choose_word(self.revised_dict, self.heuristic)


		# Currently this agent always returns the first word from the dictionary-probably
        # a good idea to replace this with a better guess based on your code above.
        # return self.dictionary[0]
		return best_word
