import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))
punctuations = set(string.punctuation)
stemmer = PorterStemmer()
        

# Load the model
model_path = "models/lstm/model.h5"
loaded_model = tf.keras.models.load_model(model_path)

# Load the tokenizer
tokenizer_path = "models/lstm/tokenizer.pickle"
with open(tokenizer_path, 'rb') as handle:
    loaded_tokenizer = pickle.load(handle)

# Define the new text
new_text = "Dogs are pet"

def preprocess_text(text):
    # Tokenize the text
    words = word_tokenize(text)

    # Remove stopwords and punctuations, and lowercase the words
    words = [word.lower() for word in words if word.lower() not in stop_words and word not in punctuations]

    # Apply stemming
    words = [stemmer.stem(word) for word in words]

    # Join the words back into a single string
    preprocessed_text = ' '.join(words)

    return preprocessed_text

# Preprocess the new text
preprocessed_text = preprocess_text(new_text)  # using the same preprocess_text function you defined during training

print("Step 1")
print(preprocessed_text)

# Convert text to sequences of integers
new_text_sequence = loaded_tokenizer.texts_to_sequences([preprocessed_text])

print("Step 2")
print(new_text_sequence)

# Pad sequences to ensure uniform length for LSTM input
max_sequence_length = 100  # same as during training
new_text_padded = pad_sequences(new_text_sequence, maxlen=max_sequence_length, padding='post')

print("Step 3")
print(new_text_padded)


# Make a prediction
prediction = loaded_model.predict(new_text_padded)

# Print the result
if prediction >= 0.5:
    print("This text is likely to be fake.")
else:
    print("This text is likely to be real.")