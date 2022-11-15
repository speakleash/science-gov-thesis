import requests
from tqdm import tqdm
import os
from lm_dataformat import Archive
import shutil
import spacy
import json
import glob

def download_file(url):

    ok = True
    parts = url.split('/')
    file_name = parts[-1]

    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open(file_name, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        ok = False

    return ok, file_name

def get_word_stats(txt):
    if not txt:
        return 0, 0, 0, 0

    sentences = 0
    words = 0
    verbs = 0
    nouns = 0

    doc = nlp(txt)

    sentences = len(list(doc.sents))
    words = len([token.text for token in doc if not token.is_punct])
    nouns = len([token.text for token in doc if (not token.is_stop and not token.is_punct and token.pos_ == "NOUN")])
    verbs = len([token.text for token in doc if (not token.is_stop and not token.is_punct and token.pos_ == "VERB")])

    return sentences, words, verbs, nouns




ar = Archive('./cache')
file_name_zst = 'thesis.jsonl.zst'
file_name_manifest = 'thesis.manifest'
nlp = spacy.load("pl_core_news_md")

total_len = 0
total_docs = 0
total_sentences = 0
total_words = 0
total_verbs = 0
total_nouns = 0

# TODO
# 1. Odczytać data/json
# 2. Plik po pliku downolad, sprawdzić, czy ju lokalnie istnieje
# 3. Plik po pliku rozbicie do txt + sprawdzenie, czy istnieje
# 4. Sprawdzenie, czy wiekszosc jest po polsku (lang detect?)
# 5. Obliczenie statystyki dla kadego, polskiego tekstru (analogicznie do wikipedii)
# 6. uzupelnienie add_data

ar.add_data("aaa")
ar.commit()

data_files= glob.glob('./cache/*')
file_size = 0

for f in data_files:
    print(f)
    if f.endswith('.zst'):
        shutil.copy(f, file_name_zst)
        file_size = os.path.getsize(file_name_zst)

    os.remove(f)

manifest = {"project" : "SpeakLeash", "name": "thesis", "description": "Large document examples", "language": "pl", "file_size" : file_size, "sources": [{"name": "TO DO", "url": "TO DO", "license": "TO DO"}], "stats": {"documents": total_docs, "sentences": total_sentences, "words" : total_words, "nouns" : total_nouns, "verbs" : total_verbs, "characters": total_len}}
json_manifest = json.dumps(manifest, indent = 4) 

with open(file_name_manifest, 'w') as mf:
    mf.write(json_manifest)


