"""
Sentence Evaluation and Analysis

This script performs evaluation and analysis of sentences based on gold and predicted senses.

Dependencies:
    - csv: for reading CSV files
    - f1_score, precision_score, recall_score: from sklearn.metrics for evaluating the model performance

Functions:
    - read_csv_file(filename): Reads data from a CSV file and constructs sentences based on the tokens in the file.
    - evaluate(gold_sentences, pred_sentences): Evaluates the performance of the model based on gold and predicted senses.

"""

import csv
from sklearn.metrics import f1_score, precision_score, recall_score


def read_csv_file(filename):
    """
    Reads data from a CSV file and constructs sentences based on the tokens in the file.
    Args:
    - filename (str): The path to the CSV file to be read.
    Returns:
    - dict: A dictionary where keys are sentence IDs and values are sentences constructed from tokens.
    """
    # Dictionary to store sentences
    sentences = {}
    # List to hold tokens of the current sentence being constructed
    current_sentence = {}

    # Open the CSV file for reading
    with open(filename, 'r', newline='',encoding="utf-8-sig") as file:
        # Create a CSV reader object
        reader = csv.DictReader(file)
        # Variable to track the current sentence ID
        id = ""
        # Iterate over each row in the CSV file
        count = 1
        for row in reader:
            # Extract the first 9 characters of the Token ID
            token_id_prefix = row["Token ID"]
            # If the current Token ID prefix is different from the previous one,
            # it means we are starting a new sentence
            if token_id_prefix != id:
                # If there are tokens in the current sentence, join them to form a sentence
                if current_sentence:
                    sentences[id] = current_sentence
                # Reset the current sentence
                current_sentence = {}
                # Update the current sentence ID
                id = token_id_prefix
                count = 1

            # Extract the token from the row
            token = row['Token']
            # If the token is not None, append it to the current sentence
            if token is not None:
                if count % 10 == count:
                    tokenID = f"t00{count}"
                elif count % 100 == count:
                    tokenID = f"t0{count}"
                else:
                    tokenID = f"t{count}"
                count += 1
                current_sentence[tokenID] = [row['Token'], row['Sense']]

        # After reading all rows, if there are tokens in the current sentence, join them to form a sentence
        if current_sentence:
            sentences[id] = current_sentence
    # Return the constructed sentences
    return sentences


def evaluate(gold_sentences, pred_sentences):
    """
    Evaluates the performance of the model based on gold and predicted senses.
    Args:
        gold_sentences (dict): Dictionary containing gold standard sentences.
        pred_sentences (dict): Dictionary containing predicted sentences.
    """
    p = 0
    r = 0
    f1 = 0
    for x in range(len(gold_sentences.keys())):
        gold_sentence = gold_sentences[list(gold_sentences.keys())[x]]
        pred_sentence = pred_sentences[list(pred_sentences.keys())[x]]
        # print(len(gold_sentence.keys()),len(pred_sentence.keys()))
        if len(gold_sentence.keys()) == len(pred_sentence.keys()):
            f1 += f1_score([y[1] for x, y in gold_sentence.items()], [y[1] for x, y in pred_sentence.items()],
                           average='micro')
            p += precision_score([y[1] for x, y in gold_sentence.items()], [y[1] for x, y in pred_sentence.items()],
                                 average='micro')
            r += recall_score([y[1] for x, y in gold_sentence.items()], [y[1] for x, y in pred_sentence.items()],
                              average='micro')
        else:
            g = [y for x, y in gold_sentence.items()]
            pred = [y for x, y in pred_sentence.items()]
            # Adjust lists if lengths are not equal
            if len(g) < len(pred):
                x = 0
                a = 0
                while (x < len(pred)):
                    count = 0
                    if g[x][0].lower() != pred[x][0]:
                        a = x
                        x += 1
                        while (g[x][0].lower() != pred[a][0] and a < len(pred)):
                            count += 1
                            a += 1
                        for a in range(count - 1):
                            g.insert(x + a, ["", 'n/a'])
                        x += count

                    else:
                        x += 1

            f1 += f1_score([y[1] for y in g], [y[1] for y in pred], average='micro')
            p += precision_score([y[1] for y in g], [y[1] for y in pred], average='micro')
            r += recall_score([y[1] for y in g], [y[1] for y in pred], average='micro')

    print(
        f"F1 Score: {f1 / len(gold_sentences.keys()):.2f}\nPrecision: {p / len(gold_sentences.keys()):.2f} \nRecall: {r / len(gold_sentences.keys()):.2f}")

def get_column(csv_file,row_val, second =None):
    listt = []
    with open(csv_file, 'r', newline='', encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:

            if row[row_val]:
                if second:
                    if row[second]:
                        listt.append(int(row[row_val]))
                else:
                    listt.append(int(row[row_val]))
    return listt

def evaluate_manual(silver,gold):
    l1 = get_column(silver,"Correct?")
    l2 = get_column(gold, "Add Annotation","BN Synset")
    print(sum(l1)/len(l1))
    print(sum(l1)/(len(l1)+len(l2)))
    return


evaluate_manual("../data/farsi_silver.csv","../data/farsi_gold.csv")

#
# gold_sentences = read_csv_file("out_senses.csv")
# pred_sentences = read_csv_file("out_senses_farsi_GOLD.csv")
# evaluate(gold_sentences, pred_sentences)
