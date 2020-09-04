import pickle
from argparse import ArgumentParser

# Requires NLTK to be installed:
# python3 -m pip install nltk
# python3 -c 'import nltk;nltk.download("punkt")'
# May be slow at first start due to NLTK preparing its dependencies
from nltk import word_tokenize, sent_tokenize
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk.lm import MLE


def main() -> None:
    """Main entrypoint."""
    # Create an argument parser for parsing CLI arguments
    parser = ArgumentParser(description="A tool to train an AI to predict the probability of a word in a sentence")

    # Add parameters for the server connection
    parser.add_argument("-i", "--input", required=True, type=str, help="The input file to read from")
    parser.add_argument("-o", "--output", required=True, type=str, help="The output file to serialize the model to")
    parser.add_argument("-l", "--language", required=True, type=str, help="The name of the language to use")

    # Parse the arguments
    options = parser.parse_args()

    # Read and extract tokens
    tokens = []
    with open(options.input, "r") as file:
        raw_text = file.read()
        # Tokenize the text.
        tokens = [list(map(str.lower, word_tokenize(sentence))) for sentence in sent_tokenize(raw_text, language=options.language)]

    # n-gram size (trigram)
    n = 3

    # Prepare train data
    train_data, padded_sentences = padded_everygram_pipeline(n, tokens)

    # Train a Maximum Likelihood Estimation (MLE) model
    model = MLE(n)
    model.fit(train_data, padded_sentences)

    with open(options.output, "wb") as file:
        pickle.dump(model, file)


if __name__ == '__main__':
    main()
