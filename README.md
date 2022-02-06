# Wordle helper

## Motivation
Wordle is fun! But let's face it, it kind of sucks for us non-native English speakers, so I figured I'd write my own helper.

## User guide
To start the helper simply run:

```
❯ ./helper.sh


--------------------------------------------------------------------
Round 1

Try "arise"
what word did you enter? arise
what was the feedback? Enter 'g' for green, 'b' for black and 'y' for yellow. bbyyy


--------------------------------------------------------------------
Round 2

Try "vines"
 > here are other options that may also work:
   vines -                              19.126315789473683
   lines ----                           19.568421052631578
   liens -------                        19.94736842105263
   kines --------                       20.157894736842106
   tines -----------                    20.51578947368421
   mines ------------                   20.66315789473684
   dines -------------                  20.726315789473684
   lives -------------                  20.74736842105263
   sinew -------------                  20.810526315789474
   sited --------------                 20.852631578947367
   skein ----------------               21.105263157894736
   stein ----------------               21.189473684210526
   miens -----------------              21.273684210526316
   inset -------------------            21.54736842105263
   vised -------------------            21.568421052631578
   dives --------------------           21.71578947368421
   likes ----------------------         21.905263157894737
   idles -------------------------      22.305263157894736
   tiles -------------------------      22.305263157894736
   dikes ------------------------------ 23.042105263157893
what word did you enter? 
```

The helper will suggest a word to try. You can be a good fella and try that word, but you may be feeling a bit adventurous and try something different! The helper will ask you what word did you actually enter and what feedback you got back from Wordle.
Based on the feedback it will calculate the best next word to try.

## Installation
```
./install.sh
```

## But how does it work?

Using a list of curated 5 letter words, the helper tries to constantly narrow down the list of possible answers. Do this for a couple of rounds and hopefully the list will be narrowed down to just one word, the right answer!