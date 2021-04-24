"""
Uses the PYPHEN module to convert from given string into syllables
Utilizes the HUNSPELL dictionaries
https://pyphen.org/
https://github.com/Kozea/Pyphen

October 2020
"""

import pyphen

# use czech language dictionary
pyphen.language_fallback("cs_CZ")
dic = pyphen.Pyphen(lang='cs_CZ')

# string to be hyphenated
word = "demotivace"

# hyphenate
syllables = dic.inserted(word)

print(syllables)
