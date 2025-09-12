# Sense-Projection
This repository is for the paper Semi-Automated Construction of Sense-Annotated Datasets for Practically Any Language. In *Proceedings of the 31st International Conference on Computational Linguistics*, pages 6270–6284, Abu Dhabi, UAE. Association for Computational Linguistics.

📄 [Paper](https://aclanthology.org/2025.coling-main.419/) | 🖼️ [Poster](assets/poster.pdf)

---

## Dependencies
Ensure you have the following dependencies installed:
+ Python >= 3.8
+ pandas
+ google-cloud-translate
+ simalign
+ spacy
+ nltk
+ tqdm

## Pipeline Overview
The sense projection pipeline consists of the following steps:

1. **Translation** (`src/translations.ipynb`) - Translate source sentences into the target language using Google Cloud Translate. Requires a Google Cloud API key in JSON format.

2. **Tokenization** (`src/tokenize.ipynb`) - Tokenize the translated text using SpaCy with POS tagging. It's recommended to verify translations, tokenization, and POS tags before proceeding.

3. **Alignment** (`src/alignment.ipynb`) - Align target language tokens to source tokens using SimAlign. This creates the base version with all senses transferred from aligned source tokens.

4. **Filtering** (`src/filter.py`) - Filter out improperly projected senses using dictionary validation and POS constraints.

5. **Key Generation** (`src/get_key.py`) - Create key files for evaluation:
   ```bash
   python src/get_key.py input.tsv output.txt --id_column "Token ID" --synset_column "BN Synset"
   ```

6. **Evaluation** (`src/main.py`) - Score the system output against gold standard:
   ```bash
   python src/main.py --gold_file gold.txt --test_file system.txt
   ```

## Data Structure
The repository includes multilingual datasets for Bengali, Chinese, English, Farsi, Italian, and Spanish. English data is provided in two formats:
- **Original format**: All tokens have IDs (compatible with Bengali, Farsi, Chinese)
- **Second-sense format**: Only sense-bearing tokens have IDs (compatible with Spanish, Italian)

## Usage
For reproduction, you can skip the translation step (1) and start from alignment (3) using the provided translated data.

## 👥 Author

- **Jai Riley** — <jai.riley@ualberta.ca>

---

## 📚 BibTeX

```bibtex
@inproceedings{riley-etal-2025-semi,
    title = "Semi-Automated Construction of Sense-Annotated Datasets for Practically Any Language",
    author = "Riley, Jai  and
      Hauer, Bradley  and
      Hriti, Nafisa Sadaf  and
      Luo, Guoqing  and
      Mirzaei, Amirreza  and
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
    abstract = "High-quality sense-annotated datasets are vital for evaluating and comparing WSD systems. We present a novel approach to creating parallel sense-annotated datasets, which can be applied to any language that English can be translated into. The method incorporates machine translation, word alignment, sense projection, and sense filtering to produce silver annotations, which can then be revised manually to obtain gold datasets. By applying our method to Farsi, Chinese, and Bengali, we produce new parallel benchmark datasets, which are vetted by native speakers of each language. Our automatically-generated silver datasets are of higher quality than the annotations obtained with recent multilingual WSD systems, particularly on non-European languages."
}
``` 