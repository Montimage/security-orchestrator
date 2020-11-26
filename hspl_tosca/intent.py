import pickle
from nltk import NaiveBayesClassifier
from nltk.tokenize import RegexpTokenizer

def features(sentence):
    tokenizer = RegexpTokenizer(r'\w+')
    features = {}
    tokens=tokenizer.tokenize(sentence.lower())
    #print(tokens)
    for word in tokens:
        features['count(%s)' % word] = tokens.count(word)
        features['has(%s)' % word] = word in tokens
    #print(features)
    return features
filename='classifier.pickle'
def train():
    block = ["if attack deny attacker","block it", "deny from access","block wissam to access internet in vfw"]
    allow = ["if attack allow only user","let them access internet","permit them access"]

    trainer = NaiveBayesClassifier.train
    sentencelist = ([(sentence, 'block') for sentence in block] + [(sentence, 'allow') for sentence in allow])

    train = sentencelist

    classifier = trainer( [(features(n), g) for (n, g) in train] )

    with open(filename, 'wb') as outfile:
        pickle.dump(classifier, outfile)
        outfile.close()
def predict(sentence):
    f = open(filename, 'rb')
    classifier = pickle.load(f)
    f.close()
    return(classifier.classify(features(sentence)))
#train()
#print(predict("block wissam to access internet in vfw"))
#print(predict("in case of ddos attack deny attacker to access internet"))