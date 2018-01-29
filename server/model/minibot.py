##### LOAD LIBRARIES #####
# things we need for NLP
import nltk
from nltk.stem.lancaster import LancasterStemmer

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

# import utilities
import pickle
import json
import os


##### LOAD DATA AND SETUP MODEL #####
# things we need for NLP
stemmer = LancasterStemmer()

# import our chat-bot intents file from local path
appPath = os.path.dirname(os.path.abspath(__file__))
intentsPath = os.path.join(appPath, "intents.json")
with open(intentsPath) as json_data:
    intents = json.load(json_data)

# check if model already exists
appPath = os.path.dirname(os.path.abspath(__file__))
if not os.path.isfile(os.path.join(appPath, "model/training_data")): # if not create model
    ##### PROCESS DATA #####
    words = []
    classes = []
    documents = []
    ignore_words = ['?']
    # loop through each sentence in our intents patterns
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            # tokenize each word in the sentence
            w = nltk.word_tokenize(pattern)
            # add to our words list
            words.extend(w)
            # add to documents in our corpus
            documents.append((w, intent['tag']))
            # add to our classes list
            if intent['tag'] not in classes:
                classes.append(intent['tag'])
    # stem and lower each word and remove duplicates
    words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
    words = sorted(list(set(words)))
    # remove duplicates
    classes = sorted(list(set(classes)))

    ##### CREATE TRAINING AND TESTING DATA #####
    # create our training data
    training = []
    output = []
    # create an empty array for our output
    output_empty = [0] * len(classes)

    # training set, bag of words for each sentence
    for doc in documents:
        # initialize our bag of words
        bag = []
        # list of tokenized words for the pattern
        pattern_words = doc[0]
        # stem each word
        pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
        # create our bag of words array
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)

        # output is a '0' for each tag and '1' for current tag
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1

        training.append([bag, output_row])

    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)

    # create train and test lists
    train_x = list(training[:,0])
    train_y = list(training[:,1])

    ##### BUILD AND TRAIN MODEL #####
    # reset underlying graph data
    tf.reset_default_graph()
    # Build neural network
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)

    # Define model and setup tensorboard
    logsPath = os.path.join(appPath, 'tflearn_logs')
    model = tflearn.DNN(net, tensorboard_dir=logsPath)
    # Start training (apply gradient descent algorithm)
    model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
    modelPath  = os.path.join(appPath, 'model.tflearn')
    model.save(modelPath)

    ##### SAVE MODEL #####
    # save all of our data structures
    trainingDataPath = os.path.join(appPath, "training_data")
    pickle.dump( {'words':words, 'classes':classes, 'train_x':train_x, 'train_y':train_y}, open( trainingDataPath, "wb" ) )


else: # if the model already exists
    # restore all of our data structures from local files
    appPath = os.path.dirname(os.path.abspath(__file__))
    trainingDataPath = os.path.join(appPath, "training_data")
    data = pickle.load( open( trainingDataPath, "rb" ) )
    words = data['words']
    classes = data['classes']
    train_x = data['train_x']
    train_y = data['train_y']

    ##### SET UP MODEL #####
    # Build neural network
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, 8)
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)

    # Define model and setup tensorboard
    logsPath = os.path.join(appPath, 'tflearn_logs')
    model = tflearn.DNN(net, tensorboard_dir=logsPath)

    # load our saved model
    modelPath  = os.path.join(appPath, 'model.tflearn')
    model.load(modelPath)


# create a data structure to hold user context
context = {}
# error threshold for intent detection
ERROR_THRESHOLD = 0.25



##### DEFINE PROCESSING FUNCTIONS FOR NEW INPUT #####

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

def response(sentence, userID='123', show_details=False):
    results = classify(sentence)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if i['tag'] == results[0][0]:
                    # set context for this intent if necessary
                    if 'context_set' in i:
                        if show_details: print ('context:', i['context_set'])
                        context[userID] = i['context_set']

                    # check if this intent is contextual and applies to this user's conversation
                    if not 'context_filter' in i or \
                        (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
                        if show_details: print ('tag:', i['tag'])
                        # a random response from the intent
                        return random.choice(i['responses'])

            results.pop(0)
