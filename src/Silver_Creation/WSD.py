import requests
import csv
import pandas as pd
def get_wsd(sentence,id,d):
    try:
        response = requests.post(api_url, headers=headers, json=sentence)

        if response.status_code == 200:
            json_response = response.json()

            for sentence in json_response:
                for token in sentence['tokens']:
                    # print(token)
                    if token['index'] % 10 == token['index']:
                        token_id = f't00{token["index"]}'
                    elif token['index'] % 100 == token['index']:
                        token_id = f't0{token["index"]}'
                    else:
                        token_id = f't{token["index"]}'
                    print(token['text'] )
                    if len(token['bnSynsetId']) > 1:
                        d.append({"Token ID":f'{id}.{token_id}',
                                  "Token":token['text'],
                                  'POS':token['pos'],
                                  "Lemma":token['lemma'],
                                  "BN Synset":token['bnSynsetId']
                                  })
                    else:
                        d.append({"Token ID":f'{id}.{token_id}',
                                  "Token":token['text'],
                                  'POS':token['pos'],
                                  "Lemma":token['lemma'],
                                  "BN Synset":""
                                  })

    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")

def read_csv_file(file_path):
    count = 0
    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile,delimiter="\t")
        sentences = []
        for row in reader:
            sentences.append({'ID': row['Sentence ID'], "Sentence": {'text': row['Sentence'].lower(), 'lang': lang}})
            count += 1
            # print(f"Done row {count}")
    return sentences

api_url = "http://127.0.0.1:12346/api/model"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}
lang = "ZH"
language = "Chinese"
sentences = read_csv_file(f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/gold-sentences-{language}.tsv")
# print(sentences)
# df = pd.DataFrame(d)

d = []
# print(sentences[0]["Sentence"])
for x in range(len(sentences)):
    print(f'{x} of {len(sentences)}')
    # print(sentences)
    get_wsd([sentences[x]["Sentence"]],sentences[x]['ID'],d)

df = pd.DataFrame(d)
print(df)

df.to_csv(f"/Users/jairiley/Desktop/Research/Sense-Projection/data/{language}/{language}-WSD.tsv", sep='\t', index=False)
