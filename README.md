# Word frequencies
### Data and tools to compile word frequencies for use with NLP, spelling correction etc.
***

### Goal

The goal of this project is to facilitate easy to use data and tools regarding word frequencies in various languages. Any and all contribution to add more data to the project is welcome.

### Available tools

The `script` directory contains several scripts that can be used individually as a library or as a CLI tool.

There are scripts to fetch data from Wikipedia articles, Gutenberg books as well as other regional sources.

The scripts in `scripts/processing` can be used to download and compile large text files for a language as well as a frequency map.

The `scripts/ai/test_ai` and `scripts/ai/train_ai` scripts can be used to train a MLE model using NLTK to predict the likelihood of a specific word being in a sentence, as well as generating new sentences.

### Available data

As of now, this repository contains data for the Swedish and English language. No data is available within the repository itself since v1.0.0. Instead, releases are made containing the data.

#### Swedish

1. Word frequencies - roughly 300 000 words and how often they occur.
1. Character frequencies - roughly 600 characters and how often they occur.
2. bigrams - roughly 1 600 000 unique bigrams.
3. trigrams - roughly 2 150 650 unique trigrams.

Note: Due to the nature of the sources from which the data was retrieved, it is likely that the character frequencies contain foreign characters such as `海` and characters from the international phonetic alphabet. To mitigate this, when using the character frequencies, filter out characters that are not used more than `n` times where `n` is low (0-15).

#### English

The word frequencies were compiled by using the compilation script in this repository.

#### Others

Is your language missing from the released compilations? Fear not! This repository holds scripts that are designed to be as multilingual as possible. The available languages are compiled due to my personal interest, but the scripts are purposefully designed to allow fetching any language available on Wikipedia, Project Gutenberg etc. with a modular approach to easily be able to add regional sources such as local media etc.

### Contributing

Any help with the project is more than welcome. If you're unable to add a change yourself, open an issue and let someone else take a look at it.
