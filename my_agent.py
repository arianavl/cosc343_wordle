__author__ = "<Ariana van Lith>"
__organization__ = "COSC343/AIML402, University of Otago"
__email__ = "<vanar987@student.otago.ac.nz>"

import helper
from collections import Counter


def sort_func(e):
	"""
	Function that sorts 1's before 0's and any other value first
	:param e: The value
	:return: The sorted value
	"""
	if e[1] == 1:
		return 1
	if e[1] == -1:
		return 0
	return 2

def determine_heuristic(diction, word_length):
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

	last_word = helper.letter_indices_to_word(letter_indices, letters)

	# Create a dictionary holding the states and indexes for each letter
	# {'S': [[index, state][index, state]], 'O':[[index, state]...
	states = {}
	for i in range(len(last_word)):
		if last_word[i] not in states:
			states[last_word[i]] = list()
		one_letter = [i, letter_states[i]]
		states[last_word[i]].append(one_letter)

	# Sort so -1 first then 1 then zero for each letter.
	for i in states:
		states.get(i).sort(key=sort_func)

	wrong_word_list = set()

	# if its a -1 add one to amount of 1's
	# so do -1 case first then 1 then zero
	# if -1 add one to 1 count and remove words with less than that amount of letters
	# if one, add to 1 count and remove words without letter there and less than count amount
	# if zero remove all in the position and any letter that has more than count

	for word in diction:
		for letter in states:
			allowed_count = 0  # count how many letters it is allowed
			count = 0  # count how many of the letter word has
			for char in word:  # count amount of times letter is in word
				if char == letter:
					count += 1
			for state in states.get(letter):  # for each state that that letter has

				if state[1] == -1:  # if state is -1
					allowed_count += 1  # increase allowed amount
					if letter == word[state[0]]:  # remove words with that letter in that index
						wrong_word_list.add(word)

				if state[1] == 1:  # if state is 1
					allowed_count += 1  # increase allowed amount
					if letter != word[state[0]]:  # remove all words with letter not in that index
						wrong_word_list.add(word)

				if count < allowed_count: # remove words with not enough recurences of the letter
					wrong_word_list.add(word)

				if state[1] == 0:  # if state is 0
					if letter == word[state[0]]:  # remove any word with that letter in that index
						wrong_word_list.add(word)
					if count != allowed_count:
						i = 0
						wrong_word_list.add(word)
	# End of for each word loop

	for word in wrong_word_list: # remove words from dictionary
		diction.remove(word)

	return diction

def choose_word(diction, heuristic):
	"""
	Function that determines the value of a word and returns the highest valued word based off letter frequencies
	:param diction: A list of all possible words
	:param heuristic: A dictionray: The values corrosponding to each letter in each index
	:return: String: The word with the highest value
	"""
	best_word = ""
	best_value = 0

	# Find word with the largest heuristic
	for word in diction:
		value = 0
		for i in range(len(word)):
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
       letters : list
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
		self.heuristic = determine_heuristic(self.dictionary, self.word_length)
		self.revised_dict = self.dictionary.copy()
		# self.best_word = choose_word(self.dictionary, self.heuristic)


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
			self.revised_dict = self.dictionary.copy()  # reset dictionary
		else:
			self.revised_dict = revise_dict(self.revised_dict, letter_indexes, letter_states, self.heuristic,
											self.letters)

		self.heuristic = determine_heuristic(self.revised_dict, self.word_length)
		best_word = choose_word(self.revised_dict, self.heuristic)
		return best_word

