import random


# load words
with open('data/5-letters.txt') as f:
    words = f.read().split('\n')

def play():
    # choose word
    idx = int( round( len(words) * random.random() ) )
    word = words[idx]
    print(word)
    win = False
    while not win:
        guess = input()
        if len(guess) != 5:
            print('Enter a 5 letters word')
        else:
            if guess == word:
                win = True
                print('Congrats! You have won!')
            # else:
                

if __name__ == '__main__':
    play()