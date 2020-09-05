import logging
from argparse import ArgumentParser
from typing import Dict, List
from os import path

# Requires numpy, keras, tensorflow and sklearn:
# python3 -m pip install numpy keras tensorflow sklearn
# May be slow at first start due to Python preparing the dependencies
import numpy as np
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import LSTM, Dense, GRU, Embedding
from sklearn.model_selection import train_test_split

# Configure the default logging format
logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)-5s] %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


def create_sequences(corpus: str, length: int, token_map: Dict[str, int]) -> List[str]:
    """Create sequences of text from sentences."""
    sequences = []
    for sentence in corpus.split("\n"):
        for i in range(length, len(sentence)):
            sequence = sentence[i-length:i+1]
            sequences.append([token_map[character] for character in sequence])
    return sequences


def main() -> None:
    """Main entrypoint."""
    # Create an argument parser for parsing CLI arguments
    parser = ArgumentParser(description="A tool to train an AI to generate sentences")

    # Add parameters for the server connection
    parser.add_argument("-i", "--input", required=True, type=str, help="The input file to read sentences from")
    parser.add_argument("-t", "--training-data", required=True, type=str, help="The input file to read training data from")
    parser.add_argument("-o", "--output", required=True, type=str, help="The output file to serialize the model to")

    # Parse the arguments
    options = parser.parse_args()

    # Read the corpus
    logger.info("Loading corpus")
    corpus = None
    with open(options.input, "r") as file:
        corpus = file.read()

    # Create a token map of the words
    logger.info("Creating token map")
    characters = sorted(list(set(" ".join(corpus.split("\n")))))
    token_map = dict((character, index) for index, character in enumerate(characters))
    logger.info("%d tokens mapped", len(token_map))

    training_data = None
    if path.exists(options.training_data):
        logger.info("Reading training data")
        with open(options.training_data, "rb") as file:
            training_data = np.load(file)
    else:
        # Create sequences
        logger.info("Creating input sequences")
        training_data = np.array(create_sequences(corpus, 30, token_map))

        # Serialize the training data if specified
        logger.info("Storing training data")
        with open(options.training_data, "wb") as file:
            np.save(file, training_data)

    # Create training and validation sets
    vocabulary_size = len(token_map)
    X, y = training_data[:,:-1], training_data[:,-1]
    y = to_categorical(y, num_classes=vocabulary_size)
    X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.1, random_state=42)
    print('Train shape:', X_tr.shape, 'Val shape:', X_val.shape)

    # Create the model
    model = Sequential()
    model.add(Embedding(vocabulary_size, 50, input_length=30, trainable=True))
    model.add(GRU(150, recurrent_dropout=0.1, dropout=0.1))
    model.add(Dense(vocabulary_size, activation='softmax'))
    print(model.summary())

    # Compile the model
    logger.info("Compiling model")
    model.compile(loss='categorical_crossentropy', metrics=['acc'], optimizer='adam')

    # Train the model
    logger.info("Training model")
    model.fit(X_tr, y_tr, epochs=100, verbose=2, validation_data=(X_val, y_val))

    # Serialize the model
    logger.info("Serializing model")
    model.save(options.output)


if __name__ == '__main__':
    main()
