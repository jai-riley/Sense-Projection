Semi-Automated Construction of Sense-Annotated Datasets for Practically Any Language

Jai Riley, Bradley Hauer, Nafisa Sadaf Hriti, Guoqing Luo, Amirreza Mirzaei, Ali Rafiei
Hadi Sheikhi, Mahvash Siavashpour, Mohammad Tavakoli, Ning Shi, Grzegorz Kondrak

COLING 2025


Paper Link:
https://aclanthology.org/2025.coling-main.419/

Paper Citation:
@inproceedings{riley-etal-2025-semi,
    title = "Semi-Automated Construction of Sense-Annotated Datasets for Practically Any Language",
    author = "Riley, Jai  and
      Hauer, Bradley M.  and
      Hriti, Nafisa Sadaf  and
      Luo, Guoqing  and
      Mirzaei, Amir Reza  and
      Rafiei, Ali  and
      Sheikhi, Hadi  and
      Siavashpour, Mahvash  and
      Tavakoli, Mohammad  and
      Shi, Ning  and
      Kondrak, Grzegorz",
    editor = "Rambow, Owen  and
      Wanner, Leo  and
      Apidianaki, Marianna  and
      Al-Khalifa, Hend  and
      Eugenio, Barbara Di  and
      Schockaert, Steven",
    booktitle = "Proceedings of the 31st International Conference on Computational Linguistics",
    month = jan,
    year = "2025",
    address = "Abu Dhabi, UAE",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.coling-main.419/",
    pages = "6270--6284",
}


The pipeline consists of a set of steps:

(1) Translate the source sentences into the target language. The file translations.ipynb shows how to do this using google translate. This script with require a .json file with a key to the google cloud API. If you are trying to reproduce our work you can skip this step and just to step 3.

(2) Tokenize the translated text. We have an of how we do this with SpaCy in the file tokenize.ipynb. You could additionally perform POS tagging during this step as well, or during alignment transfer over the POS tag of the source to the target token. NOTE: It is reccommended that you verify translations, tokenization, and pos tags in this step before moving on to step 3 as to save you time during the gold annotation stage. 

(3) Align the tokens in the target to the source. This is done through the align.ipynb file. This will create the base version of our method with all the sense transfered over from the aligned source tokens. 

(4) Filter out improperly projected senses. 

(5) Create key files from the file get_key.py in order to compare to the gold.

(6) You can get a score for your two key files, gold versus the created, using the main.py function. 