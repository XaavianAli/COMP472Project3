import csv
import random
from gensim import downloader

def letter_to_index(index_letter):
    if index_letter == "a":
        return 1
    elif index_letter == "b":
        return 2
    elif index_letter == "c":
        return 3
    elif index_letter == "d":
        return 4

model = "conceptnet-numberbatch-17-06-300"

corpus = downloader.load(model)

with open('synonym_guess.txt') as f:
    lines = f.readlines()

results = []
correct_count = 0
guess_count = 0
for i in range(480):
    if i % 6 != 0:
        continue

    must_guess = False

    line = lines[i].replace("\t", "").replace("\n", "").replace(".", "")
    guess_word = ''.join([i for i in line if not i.isdigit()])

    if (guess_word in corpus.key_to_index) == False:
        must_guess = True

    index_letter = lines[i + 5].replace("\t", "").replace("\n", "").replace(".", "")
    index = letter_to_index(index_letter)
    line = lines[i+index].replace("\t", "").replace("\n", "").replace(".", "")
    best_synonym = line[1:]

    guess = ""
    score = 0
    word_found = False
    for j in range(1, 5):
        if must_guess:
            random_index = random.randint(1,4)
            line = lines[i + random_index].replace("\t", "").replace("\n", "").replace(".", "")
            guess = line[1:]
            break

        line = lines[i + j].replace("\t", "").replace("\n", "").replace(".", "")
        word = line[1:]

        if word in corpus.key_to_index:
            word_found = True
        else:
            continue

        similarity = corpus.similarity(guess_word, word)
        if similarity > score:
            guess = word
            score = similarity

    if word_found == False:
        must_guess = True

    label = ""
    if must_guess:
        label = "guess"
        guess_count += 1
    elif best_synonym == guess:
        label = "correct"
        correct_count += 1
    else:
        label = "wrong"

    results.append([guess_word, best_synonym, guess, label])

header = ["question-word", "correct answer-word", "model's guess-word", "result label"]
with open(model + '-details.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(results)

corpus_length = len(corpus.key_to_index)
without_guess_count = 80 - guess_count
accuracy = correct_count / without_guess_count
analysis = [model, corpus_length, correct_count, without_guess_count, accuracy]
with open('analysis.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(analysis)
