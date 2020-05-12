import re

words = re.findall(r'\b\w[^.,;:!?\s]{2,}\b', open('Book.txt').read().lower())
f = open('text.txt', 'w')
uniqWords = sorted(set(words))
for word in uniqWords:
    f.write(word + '\n')
    print(word, '-', words.count(word), 'times',)
f.close()

