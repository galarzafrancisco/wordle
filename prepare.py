import enchant
us_dictionary = enchant.Dict('en_US')
gb_dictionary = enchant.Dict('en_GB')

file_name = 'words-raw'

with open(f'data/{file_name}.txt', 'r') as f:
    raw_words = f.read().split('\n')

# print(raw_words)
# Keep words with 5 leters made of letters only
filtered = [word.lower() for word in raw_words if len(word) == 5 and word.isalpha() and (us_dictionary.check(word) or gb_dictionary.check(word))]

print(filtered)
with open(f'data/clean-{file_name}.txt', 'w') as f:
    f.write('\n'.join(filtered))
