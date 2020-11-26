import spacy
import random

modelfile = "entity.pickle"

TRAIN_DATA = [('in vfw, block attacker to access internet, if ddos happens in router 1', {
	'entities': [(14, 22, 'object'), (62, 70, 'trigger'), (3, 6, 'target'), (46, 50, 'event')]
}), ('in vfw, allow user to access internet, if ddos happens in router 2', {
	'entities': [(14, 18, 'object'), (58, 66, 'trigger'), (3, 6, 'target'), (42, 46, 'event')]
}), ('in case of ddos attack on router 2, in vfw, allow user to access internet', {
	'entities': [(50, 54, 'object'), (26, 34, 'trigger'), (39, 42, 'target'), (11, 15, 'event')]
}), ('on router 3, if ddos attack happens, deny attacker to access internet in firewall2', {
	'entities': [(42, 50, 'object'), (3, 11, 'trigger'), (73, 82, 'target'), (16, 20, 'event')]
}),('on r3, if man in the middle is detected, deny user to access internet in firewall2', {
        'entities': [(46, 50, 'object'), (3, 5, 'trigger'), (73, 82, 'target'), (10, 27, 'event')]
}),('on router, if man in the middle is detected, deny 10.0.0.1 to access internet in firewall2', {
        'entities': [(50, 58, 'object'), (3, 9, 'trigger'), (81, 90, 'target'), (14, 31, 'event')]
}),('if cross site scripting is detected on vm1, deny vm1 to access internet by firewall', {
        'entities': [(39, 42, 'object'), (39, 42, 'trigger'), (75, 83, 'target'), (3, 23, 'event')]
}),('if alice is detected as a trojan, in firewall, deny alice to access internet', {
        'entities': [(3, 8, 'object'), (3, 8, 'trigger'), (37, 45, 'target'), (26, 32, 'event')]
}),('if alice is detected as a trojan, in firewall, allow only user', {
        'entities': [(58, 62, 'object'), (3, 8, 'trigger'), (37, 45, 'target'), (26, 32, 'event')]
})]



def train_spacy(data,iterations):
    TRAIN_DATA = data
    nlp = spacy.blank('en')  
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
       

    for _, annotations in TRAIN_DATA:
         for ent in annotations.get('entities'):
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes): 
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print("Statring iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                    [text], 
                    [annotations],
                    drop=0.2,  
                    sgd=optimizer,
                    losses=losses)
            print(losses)
    return nlp


#prdnlp = train_spacy(TRAIN_DATA, 20)
#prdnlp.to_disk(modelfile)
prdnlp=spacy.load(modelfile)

def predict(test_text):
    
    doc = prdnlp(test_text)
    result=[]
    for ent in doc.ents:
        a={}
        a[ent.text]=ent.label_
        result.append(a)
    return result
#test_text = "in case of ddos attack in router 1, in vfw, block attacker to access internet"
#print(predict(test_text))