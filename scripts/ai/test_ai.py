import pickle
import random
from argparse import ArgumentParser

# Requires NLTK to be installed:
# python3 -m pip install nltk
# python3 -c 'import nltk;nltk.download("punkt")'
# May be slow at first start due to NLTK preparing its dependencies
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.lm import MLE


detokenize = TreebankWordDetokenizer().detokenize


def generate_sentence(model: MLE, length: int, seed=random.randint(0, 1e10)):
    content = []
    for token in model.generate(length, random_seed=seed):
        if token == '<s>':
            continue
        if token == '</s>':
            break
        content.append(token)
    return detokenize(content)


def main() -> None:
    """Main entrypoint."""
    # Create an argument parser for parsing CLI arguments
    parser = ArgumentParser(description="A tool to train an AI to predict the probability of a word in a sentence")

    # Add parameters for the server connection
    parser.add_argument("-i", "--input", required=True, type=str, help="The serialized model previously trained")
    parser.add_argument("-w", "--word", required=True, type=str, help="The word to check the probability for")
    parser.add_argument("-c", "--context", required=True, type=str, help="The context / sentence for the word")

    # Parse the arguments
    options = parser.parse_args()

    model = None
    with open(options.input, "rb") as file:
        model = pickle.load(file)

    print(model.logscore(options.word, options.context.split()))
    print(generate_sentence(model, 10))

if __name__ == '__main__':
    main()
