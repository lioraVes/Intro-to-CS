############################################################################
# FILE : hangman.py
# WRITER : Liora Vesnovaty
# EXERCISE : intro2cse ex4 2021
# DESCRIPTION: This is the hangman game. There is a secret word and the user
#              has to guess letters until the he guess the full word.
############################################################################
import hangman_helper

ABC = "abcdefghijklmnopqrstuvwxyz"  # setting a constant variable- the ABC


def not_in_wrong_lst(word, wrong_guess_lst):
    """ This function checks and returns True if the letters that are in the
        wrong_guess_lst are not in the given word, and returns False if there
        is a letter from this list in the word. """
    for letter in wrong_guess_lst:
        if letter in word:
            return False
    return True


def filter_by_places(word, pattern):
    """ This function checks if the letters that are shown in the
        pattern can be found in the word at the exact same place and only
        there. The function returns True if the word passed the checks and
        False if not. """
    for l in range(len(pattern)):
        if pattern[l] != "_":
            if word[l] != pattern[l]:
                return False
            else:
                if word.count(word[l]) != pattern.count(word[l]):
                    return False
    return True


def filter_words_list(words, pattern, wrong_guess_lst):
    """ This function returns an hints list. The function filters the big
        words list (words variable) and adds the words that can help to
        the hints_list only if all of this conditions are correct:
        - If the word is in the same length as the pattern.
        - If the letters that are shown in the pattern is in the same places
          in the word (and only there)- by calling the function
          filter_by_places.
        - if the letters in the wrong_guess_lst are not in the word - by
          calling the function not_in_wrong_lst."""
    hints_lst = []
    for word in words:
        if len(word) == len(pattern):
            if filter_by_places(word, pattern):
                if not_in_wrong_lst(word, wrong_guess_lst):
                    hints_lst.append(word)
    return hints_lst


def hints(score, words_list, pattern, wrong_guess_lst):
    """ This function shows the user a hints list. By using the
        filter_words_list this function gets the list. If the list is longer
        then the HINT_LENGTH variable from hangman_helper,the function returns
        a new shorter list- according to the HINT_LENGTH variable by using
        the show_suggestion function from hangman_helper."""
    score -= 1
    hints_list = filter_words_list(words_list, pattern, wrong_guess_lst)

    if len(hints_list) > hangman_helper.HINT_LENGTH:
        new_hints = []
        for i in range(hangman_helper.HINT_LENGTH):
            new_item = hints_list[(i * len(hints_list)) //
                                  hangman_helper.HINT_LENGTH]
            new_hints.append(new_item)

        hangman_helper.show_suggestions(new_hints)

    else:
        hangman_helper.show_suggestions(hints_list)
    return score


def initialize_game(words_list):
    """" This function initializes the game. It is called at the start of a
        new game. It gets a words list and chooses a random word by using the
        get_random_word function from hangman_helper, initializes a
        wrong_guess_lst to be empty and a pattern which is a string the
        same length as the secret word and all the strings are "_" ."""
    word = hangman_helper.get_random_word(words_list)
    wrong_guess_lst = []
    pattern = "_" * len(word)
    return word, wrong_guess_lst, pattern


def update_word_pattern(word, pattern, letter):
    """ This function gets a word, a pattern and a letter. The function
        updates the pattern so the letter that was guessed will be in it in
        the right place according to the word. The function converts the
        pattern to a list (temporary) and adds the letter in the right
        places according to the word, then converts the list to a string and
        returns the updated pattern."""
    updated_pattern_lst = list(pattern)
    for i in range(len(word)):
        if word[i] == letter:
            updated_pattern_lst[i] = letter

    pattern = ""
    for char in updated_pattern_lst:
        pattern += str(char)
    return pattern


def calc_score(score, num):
    """ This function calculates and returns the score of the user. It gets
        a number of letters that the user found and a initialized score and
        returns the updated score."""
    score -= 1
    score += (num * (num + 1)) // 2
    return score


def end_game(pattern, word, wrong_guess_lst, score):
    """ This function displays the result of the game to the user - if he
        won or lost """
    if pattern == word:
        msg = "Good job, you Won! :)"
    else:
        msg = "Sorry, you lost :( the word was " + word

    hangman_helper.display_state(pattern, wrong_guess_lst, score, msg)


def return_msg(msg_mode):
    """ This function returns the msg that should be shown to the user in the
        display_state when running the game. """
    if msg_mode == "Not Valid":
        msg = "This input is not valid"
    elif msg_mode == "Already":
        msg = "This letter was already guessed"
    elif msg_mode == "Hint":
        msg = "hint not supported yet"
    else:
        msg = ""
    return msg


def word_hidden(word, pattern, score, msg_mode, wrong_guess_lst, words_list):
    """ This function runs until the word is no longer hidden or the user
        loses. Each iteration the function shows the player his progress by
        using the display_state function from hangman helper. By calling the
        return_msg function, this function knows which msg it should print
        to the user. With the get_input function from hangman helper this
        function gets the input that the user inserts. The function checks:
        -If the user inserts a letter- if its valid or if its already been
        used and returns the right msg. If the input is fine and a part of
        the word the function calls the update_word_pattern function to
        update the pattern, counts the number of letters that the user found
        and calculates his score by calling the calc_score function. If the
        letter is not in the word the function subtracts one point from the
        score and adds the letter to the wrong_lst_guess.
        - If the user inserts a word and it's correct the function counts the
        number of letters the user found and by using the calc_score
        function calculates the score. If it isn't correct - subtracts a
        point from the score.
        - If the user wants a hint. the function calls the hints function. """
    while pattern != word and score > 0:
        msg = return_msg(msg_mode)
        hangman_helper.display_state(pattern, wrong_guess_lst, score, msg)
        msg_mode = "None"
        input_type, user_input = hangman_helper.get_input()

        if input_type == hangman_helper.LETTER:
            if len(user_input) > 1 or user_input not in ABC:
                msg_mode = "Not Valid"
            elif user_input in wrong_guess_lst or user_input in pattern:
                msg_mode = "Already"
            else:
                if user_input in word:
                    pattern = update_word_pattern(word, pattern, user_input)
                    num = word.count(user_input)
                    score = calc_score(score, num)
                else:
                    score -= 1
                    wrong_guess_lst.append(user_input)

        elif input_type == hangman_helper.WORD:
            if user_input == word:
                num = pattern.count("_")
                pattern = user_input
                score = calc_score(score, num)
            else:
                score -= 1
        else:
            score = hints(score, words_list, pattern, wrong_guess_lst)

    return score, pattern, wrong_guess_lst


def run_single_game(words_list, score):
    """ This function runs a single game. At the start- this function calls
        the initialize_game function and it gets the initialized game
        information. At first there is no need to a special message to be
        shown to the user so msg_mode variable is "None". This function
        calls the word_hidden function which will work until the word is
        found or the user lost. When the word_hidden function finishes its
        job it returns a final score,pattern, and updated wrong_guess_lst
        and this function calls the end_game function. Finally the function
        returns the users score. """
    word, wrong_guess_lst, pattern = initialize_game(words_list)
    msg_mode = "None"

    score, pattern, wrong_guess_lst = word_hidden(word, pattern, score,
                                                  msg_mode, wrong_guess_lst,
                                                  words_list)
    end_game(pattern, word, wrong_guess_lst, score)
    return score


def play_game(score, words_list):
    """ This function contains a while loop that allows the game to run on
        and on until the user loses or doesn't want to play anymore. This
        function counts the number of games the user played. If the player
        lost and want to play again (from the start) the function returns
        True."""
    num_of_games = 0
    while score > 0:
        num_of_games += 1
        score = run_single_game(words_list, score)
        if score > 0:
            msg = "Number of games played: " + str(num_of_games) + " Your " \
                  "score: " + str(score) + ". Want to play another game?"
            another_game = hangman_helper.play_again(msg)
            if another_game:
                continue
            else:
                break
    else:
        msg = "Number of games played: " + str(num_of_games) + ". Want to " \
              "play another game?"
        another_game = hangman_helper.play_again(msg)
        if another_game:
            return True


def main():
    """ This function is the main function and calls the play_game function
        in order to start playing this game. The words_list contains all the
        words that are in the words.txt file and the score is initialize to
        POINTS_INITIAL variable. want_new is a boolean variable that enable
        the program to understand if the player want to play another game
        from the start (after he lost) -it starts as True."""
    words_list = hangman_helper.load_words("words.txt")
    score = hangman_helper.POINTS_INITIAL
    want_new = True
    while want_new:
        want_new = play_game(score, words_list)


if __name__ == "__main__":
    """ This calls the function main() """
    main()
