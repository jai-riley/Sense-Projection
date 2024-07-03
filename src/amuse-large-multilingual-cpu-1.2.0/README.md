# AMuSE-WSD: All-in-one Multilingual System for Easy Word Sense Disambiguation

[AMuSE-WSD](http://nlp.uniroma1.it/amuse-wsd) is an All-in-one Multilingual System for Easy Word Sense
Disambiguation (WSD).

## Requirements

In order to run AMuSE-WSD offline, you need to install Docker. Please refer to its
[official documentation](https://docs.docker.com) to install it on your system.

## How to launch your local instance of AMuSE-WSD

To run a local instance of AMuSE-WSD, you are required to perform a one-time setup to load one of the
available images. Let’s say that we want to load `amuse-large-multilingual-cpu`:

```bash
#!/bin/bash
docker load -i amuse-medium-multilingual-cpu-1.2.0.tar
```

After that, AMuSE-WSD can be started by running the following commands:

```bash
#!/bin/bash
PORT=12346
LANGUAGES="AF"


docker run \
  --name amuse-large-multilinguall \
  -p $PORT:80 \
  -e LANGUAGES="FA" \
  amuse-large-multilingual-cpu:1.2.0
```

This will run an `amuse-large-multilingual` instance on CPU on port number `12345` loading the preprocessing
models for English, French, Italian and Chinese.

### Running AMu-SE-WSD on your GPU

If you need GPU support, you can load the `cuda` version of an image, for example `amuse-large-multilingual-cuda`.
Before using a `cuda` image, you have to load it, just like the CPU image:

```bash
#!/bin/bash
docker load -i amuse-large-multilingual-cpu-1.2.0.tar
```

Then you can launch AMuSE-WSD through the `docker run` command, with an [additional flag](https://docs.docker.com/config/containers/resource_constraints/),
`--gpus`, for example:

```bash
#!/bin/bash
PORT=12345
LANGUAGES=""

docker run \
  --name amuse-large-multilingual-cpu \
  --gpus all \
  -p $PORT:80 \
  -e LANGUAGES="EN ES" \
  amuse-large-multilingual-cpu:1.2.0
```

For more info about how to enable GPU support in Docker you can refer to the [official documentation](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html).

## Usage

AMuSE-WSD exposes an end-point named `/api/model`. The endpoint accepts `POST` requests with a `JSON` body,
containing a list of documents. For each document, two parameters must be specified:

- `text`: the text of the document
- `lang`: the language of the document

Each request returns a `JSON` response containing a list of objects, one for each input document. Each object
in the response provides the tokenization, lemmatization, PoS-tagging and sense information of the
corresponding input document.

Let's try with a simple example. We want to disambiguate the words in the following sentence
"The quick brown fox jumps over the lazy dog.":

```bash
curl -X 'POST' \
  'http://127.0.0.1/api/model' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {"text":"The quick brown fox jumps over the lazy dog.", "lang":"EN"}
]'
```

If everything went right, the output should be similar to:

```json
[
  {
    "tokens": [
      {
        "index": 0,
        "text": "The",
        "pos": "DET",
        "lemma": "the",
        "bnSynsetId": "O",
        "wnSynsetOffset": "O",
        "nltkSynset": "O"
      },
      {
        "index": 1,
        "text": "quick",
        "pos": "ADJ",
        "lemma": "quick",
        "bnSynsetId": "bn:00096664a",
        "wnSynsetOffset": "32733a",
        "nltkSynset": "agile.s.01"
      },
      {
        "index": 2,
        "text": "brown",
        "pos": "ADJ",
        "lemma": "brown",
        "bnSynsetId": "bn:00098942a",
        "wnSynsetOffset": "372111a",
        "nltkSynset": "brown.s.01"
      },
      {
        "index": 3,
        "text": "fox",
        "pos": "NOUN",
        "lemma": "fox",
        "bnSynsetId": "bn:00036129n",
        "wnSynsetOffset": "2118333n",
        "nltkSynset": "fox.n.01"
      },
      {
        "index": 4,
        "text": "jumps",
        "pos": "VERB",
        "lemma": "jump",
        "bnSynsetId": "bn:00083833v",
        "wnSynsetOffset": "1963942v",
        "nltkSynset": "jump.v.01"
      },
      {
        "index": 5,
        "text": "over",
        "pos": "ADP",
        "lemma": "over",
        "bnSynsetId": "O",
        "wnSynsetOffset": "O",
        "nltkSynset": "O"
      },
      {
        "index": 6,
        "text": "the",
        "pos": "DET",
        "lemma": "the",
        "bnSynsetId": "O",
        "wnSynsetOffset": "O",
        "nltkSynset": "O"
      },
      {
        "index": 7,
        "text": "lazy",
        "pos": "ADJ",
        "lemma": "lazy",
        "bnSynsetId": "bn:00105799a",
        "wnSynsetOffset": "981304a",
        "nltkSynset": "lazy.s.01"
      },
      {
        "index": 8,
        "text": "dog",
        "pos": "NOUN",
        "lemma": "dog",
        "bnSynsetId": "bn:00015267n",
        "wnSynsetOffset": "2084071n",
        "nltkSynset": "dog.n.01"
      },
      {
        "index": 9,
        "text": ".",
        "pos": "PUNCT",
        "lemma": ".",
        "bnSynsetId": "O",
        "wnSynsetOffset": "O",
        "nltkSynset": "O"
      }
    ]
  }
]
```

### If you already have pos-tagged and lemmatized text

If you already have pos-tagged and lemmatized text, you can use the `/api/model/from-preprocessed` endpoint. 
The endpoint accepts `POST` requests with a `JSON` body, containing a list of documents. For each document,
four parameters must be specified:
- `doc_id`: the id of the document
- `sid`: the sentence id
- `tokens`: a list of tokens, each token is a list of 4 elements: the token text, the index of the token 
 inside the sentence, the token lemma and the token pos tag
- `lang`: the language of the document

An example of a request to the `/api/model/from-preprocessed` endpoint is:

```bash
curl -X 'POST' \
  'http://127.0.0.1/api/model/from-preprocessed' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
    { 
        "doc_id": 0,
        "sid": 0,
        "tokens":[
            {
                "text":"The",
                "index":0,
                "pos":"DET",
                "lemma":"the"
            },
            {
                "text":"quick",
                "index":1,
                "pos":"ADJ",
                "lemma":"quick"
            },
            {
                "text":"brown",
                "index":2,
                "pos":"ADJ",
                "lemma":"brown"
            },
            {
                "text":"fox",
                "index":3,
                "pos":"NOUN",
                "lemma":"fox"
            },
            {
                "text":"jumps",
                "index":4,
                "pos":"VERB",
                "lemma":"jump"
            },
            {
                "text":"over",
                "index":5,
                "pos":"ADP",
                "lemma":"over"
            },
            {
                "text":"the",
                "index":6,
                "pos":"DET",
                "lemma":"the"
            },
            {
                "text":"lazy",
                "index":7,
                "pos":"ADJ",
                "lemma":"lazy"
            },
            {
                "text":"dog",
                "index":8,
                "pos":"NOUN",
                "lemma":"dog"
            },
            {
                "text":".",
                "index":9,
                "pos":"PUNCT",
                "lemma":"."
            }
        ],
        "lang":"EN"
    }
]'
```

## Environment Variables

There are a few environment variables that can be passed to the docker container to customize the behaviour of your AMuSe-WSD instance:

### `STANZA_DEVICE`

This variable can be used to specify the device to be used by Stanza. The default value is `cpu`, but you can
set it to `cuda` if you want to use the GPU.

Default value: `STANZA_DEVICE="cpu"`

Example:
Launch AMuSE-WSD with GPU support for Stanza:

```bash
docker run --name {$CONTAINER_NAME} -e STANZA_DEVICE="cuda" {$IMAGE_NAME}
````

### `LANGUAGES`

A list of languages, separated by whitespaces. This list indicates the preprocessing models to load with
AMuSE-WSD. The WSD model of AMuSE-WSD supports up to 40 languages (see the
[list of supported languages](http://nlp.uniroma1.it/amuse-wsd/api-documentation)), but each language
requires loading its own preprocessing model. We suggest loading only those languages you need so as to reduce
the memory footprint of AMuSE-WSD.

Default value: `LANGUAGES="EN"`

Example:
Launching AMuSE-WSD to disambiguate text in English, French and Italian.

```bash
docker run --name {$CONTAINER_NAME} -e LANGUAGES="EN FR IT" {$IMAGE_NAME}
```

### `TIMEOUT`

When loading many languages, AMuSE-WSD has to download multiple preprocessing models which may require a long
time. If your container crashes, try to increase this value.

Default value: `TIMEOUT="500"`

Example:
Setting the TIMEOUT value to 1200.

```bash
docker run --name {$CONTAINER_NAME} -e TIMEOUT="1200" {$IMAGE_NAME}
```

### `MAX_WORKERS`

Can be used to limit the number of simultaneously running processes (instances of AMuSE-WSD).

Default value: `MAX_WORKERS=1`

Example:
Setting the number of AMuSE-WSD instances to 4.

```bash
docker run --name {$CONTAINER_NAME} -e MAX_WORKERS="4" {$IMAGE_NAME}
```

### `WORKERS_PER_CORE`

AMuSE-WSD checks how many CPU cores are available in the current server running your container.

It will set the number of workers to the number of CPU cores multiplied by this value.

Default value: `WORKERS_PER_CORE=1`

Example:

```bash
docker run --name {$CONTAINER_NAME} -e WORKERS_PER_CORE="3" {$IMAGE_NAME}
```

If you set the value to `3` in a server with 2 CPU cores, it will run 6 worker processes.

```bash
docker run --name {$CONTAINER_NAME} -e WORKERS_PER_CORE="0.5" {$IMAGE_NAME}
```

### `LOG_LEVEL`

The log level for Gunicorn.

One of:

- `debug`
- `info`
- `warning`
- `error`
- `critical`

Default value: `LOG_LEVEL=”info”`

Example:

```bash
docker run --name {$CONTAINER_NAME} -e LOG_LEVEL="info" {$IMAGE_NAME}
```

## FastAPI docs

Auto-generated interactive documentation for the API (thanks to [FastAPI](https://fastapi.tiangolo.com/)).

```text
http://127.0.0.1:PORT/docs
```

where `PORT` is the port number you specify when starting up AMuSE-WSD.

## Supported Languages

- AF (Afrikaans)
- AR (Arabic)
- BG (Bulgarian)
- CA (Catalan)
- CS (Czech)
- DA (Danish)
- DE (German)
- EL (Greek)
- EN (English)
- ES (Spanish)
- ET (Estonian)
- EU (Basque)
- FA (Persian)
- FI (Finnish)
- FR (French)
- GA (Irish)
- HE (Hebrew)
- HI (Hindi)
- HR (Croatian)
- HU (Hungarian)
- ID (Indonesian)
- IT (Italian)
- JA (Japanese)
- KO (Korean)
- LT (Lithuanian)
- LV (Latvian)
- NL (Dutch)
- NB (Norwegian)
- PL (Polish)
- PT (Portuguese)
- RO (Romanian)
- RU (Russian)
- SK (Slovak)
- SL (Slovenian)
- SR (Serbian)
- SV (Swedish)
- TR (Turkish)
- UK (Ukrainian)
- VI (Vietnamese)
- ZH (Chinese)

## Citation

If you use AMuSE-WSD please cite
[AMuSE-WSD: An All-in-one Multilingual System for Easy Word Sense Disambiguation](https://aclanthology.org/2021.emnlp-demo.34):

```bibtex
@inproceedings{orlando-etal-2021-amuse-wsd,
  title     = {{AMuSE-WSD}: {A}n All-in-one Multilingual System for Easy {W}ord {S}ense {D}isambiguation},
  author    = {Orlando, Riccardo and Conia, Simone and Brignone, Fabrizio and Cecconi, Francesco and Navigli, Roberto},
  booktitle = {Proceedings of EMNLP},
  year      = {2021},
  month     = {nov},
  address   = {Punta Cana, Dominican Republic},
  url       = {https://aclanthology.org/2021.emnlp-demo.34},
}
```

## License

AMuSE-WSD is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
