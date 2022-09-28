# cosc343_wordle
## AI agent that plays a version of the popular online game Wordle.

Wordle is a game that challenges the user to discover a randomly chosen target word in as few guesses as possible. They are given information as to how close they are to the target word, usually via the colour of the letter or in the case of our environment, by three number states:
* ’0’ or grey, represents that the letter does not exist in the target word. (Excluding already correctly placed or identified letters)
* ’-1’ or yellow, represents the state that the corresponding letter is present some- where in the target word but not at its current index.
* ’1’ or green, represents that the letter and its placement match that of the target word.

Using this information, the user picks their next best guess as to what the target word could be. The number of guesses allowed is usually limited to a specified amount. In the case of my examples, I have limited the guesses to 6.
Therefore, the task was to create an agent that uses the letter states returned from its former guesses to pick its next best guess in order to discover the target word.
