import copy
import random
import pandas as pd

common_words_file_name = 'clean-3000-most-common.txt'
all_words_file_name = 'clean-words-raw.txt'
# test_set_file_name = 'test-set.txt'
test_set_file_name = '1000.txt'


# load words
with open(f'data/{common_words_file_name}') as f:
    common_words = f.read().split('\n')
with open(f'data/{all_words_file_name}') as f:
    all_words = f.read().split('\n')
with open(f'data/{test_set_file_name}') as f:
    test_set = f.read().split('\n')

class Feedback:
    def __init__(self):
        self.correct = [None, None, None, None, None]
        self.wrong_order = []
        self.incorrect = []
    
    def add_incorrect_char(self, incorrect_char):
        self.incorrect.append(incorrect_char)

    def add_correct_char(self, correct_char, idx):
        self.correct[idx] = correct_char

    def add_wrong_order(self, wrong_order_char, idx):
        self.wrong_order.append([wrong_order_char, idx])

    def print(self):
        print(f'correct: {self.correct}')
        print(f'incorrect: {self.incorrect}')
        print(f'wrong order: {self.wrong_order}')

    def copy(self):
        return copy.deepcopy(self)


def evaluate_guess(guess, right_answer, feedback):
    """
    Knowing the right answer and given a guess and a feedback object
    return the expanded feedback for that guess
    """
    for idx, guess_char in enumerate(guess):
        # Find incorrect characters
        if guess_char not in right_answer:
            feedback.add_incorrect_char(guess_char)
        else:
            # Find if the character is in the right order
            if right_answer[idx] == guess_char:
                feedback.add_correct_char(guess_char, idx)
            else:
                feedback.add_wrong_order(guess_char, idx)
    return feedback


def get_possible_answers(list_of_words, feedback):
    "given the feedback, what are the possible answers?"
    # Filter out incorrect characters
    for incorrect_char in feedback.incorrect:
        list_of_words = [w for w in list_of_words if incorrect_char not in w]

    # Filter out correct characters
    for idx, correct_char in enumerate(feedback.correct):
        if correct_char:
            list_of_words = [w for w in list_of_words if w[idx] == correct_char]

    # Filter out the right characters but wrong order
    for [wrong_order_char, idx] in feedback.wrong_order:
        if wrong_order_char:
            list_of_words = [w for w in list_of_words if wrong_order_char in w and w[idx] != wrong_order_char]

    return list_of_words


def rank_options(list_of_words, feedback):
    """
    Ranks a list of words to find the best guess.
    If I chose this word, how long would the next list of possible words be?
    Takes a list of possible words (list) and a feedback object (correct, wrong order and incorrect characters)
    """
    matrix = [[None for idx in range(len(list_of_words))] for idx in range(len(list_of_words))]

    ranked_words = []
    for idx_guess, guess in enumerate(list_of_words):
        next_list_length = []
        for idx_right_answer, right_answer in enumerate(list_of_words):
            internal_feedback = feedback.copy()
            internal_feedback = evaluate_guess(guess, right_answer, internal_feedback)
            possible_answers = get_possible_answers(list_of_words, internal_feedback)
            # if len(possible_answers) > 500:
            #     possible_answers = get_possible_answers(common_words, internal_feedback)
            matrix[idx_right_answer][idx_guess] = len(possible_answers)
            next_list_length.append(len(possible_answers))
        guess_score = sum(next_list_length) / len(next_list_length)
        ranked_words.append([guess, guess_score])

    ranked_words.sort(key=lambda x: x[1])
    # if len(list_of_words) < 20:
    #     df = pd.DataFrame(matrix, columns=list_of_words, index=list_of_words)
    #     print(df)
    # else:
    #     print('Matrix is too large to print')
    return ranked_words



def print_options(options):
    """
    Prints the options with an asociated bar showing their score
    """
    bar_length = 30
    number_of_options_to_print = 20
    options_to_print = options[0: number_of_options_to_print]
    min_score = options_to_print[0][1]
    max_score = options_to_print[-1][1]
    score_range = (max_score - min_score) or 1
    score_scale = bar_length / score_range
    for [word, score] in options_to_print:
        bar = ''.join(['-' if (score - min_score) * score_scale >= idx else ' ' for idx in range(bar_length)])
        print(f'{word} {bar} {score}')
    


def play(right_answer):
    initial_guess = 'arise'

    # Init game
    feedback = Feedback()
    guess = initial_guess
    words_set = all_words

    # Play until the correct answer is found
    turn = 1
    while None in feedback.correct:
        print('')
        print('')
        print('')
        print('----------------------------------------------------')
        print(f'Round {turn} - Choice: "{guess}"')
        print('----------------------------------------------------')
        print(f'Choice: "{guess}"')
        # Get feedback
        feedback = evaluate_guess(guess, right_answer, feedback)
        feedback.print()
        # Get possible answers
        possible_answers = get_possible_answers(words_set, feedback)
        if len(possible_answers) > 500:
            possible_answers = get_possible_answers(common_words, feedback)
        print(f'possible answers: {len(possible_answers)}')
        # Choose next word
        options = rank_options(possible_answers, feedback)
        print(f'ranked options: {options}')
        # Take the first option
        guess = options[0][0]
        turn += 1


def help():
    feedback = Feedback()
    win = False
    turn = 1
    guess = 'arise'
    while not win:
        print('')
        print('')
        print('--------------------------------------------------------------------')
        print(f'Round {turn}')
        print('')
        
        # Recommend option and ask for feedback from the user
        print(f'Try "{guess}"')
        guess = input("what word did you enter? ")
        colours = ''
        while len(colours) != 5:
            colours = input("what was the feedback? [g/b/y] ")
        if colours == 'ggggg':
            win = True
            print("Congratulations!")
        else:
            for idx, colour in enumerate(colours):
                if colour == 'g':
                    # right guess 
                    feedback.add_correct_char(guess[idx], idx)
                elif colour == 'y':
                    # wrong order
                    feedback.add_wrong_order(guess[idx], idx)
                elif colour == 'b':
                    # wrong character
                    feedback.add_incorrect_char(guess[idx])

            # Evaluate feedback and get new answers
            possible_answers = get_possible_answers(all_words, feedback)
            options = rank_options(possible_answers, feedback)
            print_options(options)
            guess = options[0][0]
            turn += 1

        
if __name__ == '__main__':
    help()
