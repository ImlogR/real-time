from .models import ChatModel
from django.utils import timezone
from datetime import timedelta
# import spacy
# import random
# from spacy.util import minibatch, compounding
# from spacy.training.example import Example

def spammer(user):
    now= timezone.now()
    minute_ago= now - timedelta(minutes=1)
    message_count= ChatModel.objects.filter(sent_by= user, timestamp__gt= minute_ago).count()
    if message_count > 50:
        return True
    else:
        return False
    
    
# def spammed_message(message):

#     nlp= spacy.load('en_core_web_md')
#     TRAIN_DATA = [
#         ("Send me money now", {"cats": {"SPAM": 1.0, "NOT_SPAM": 0.0}}),
#         ("Earn money fast", {"cats": {"SPAM": 1.0, "NOT_SPAM": 0.0}}),
#         ("Hey, how are you?", {"cats": {"SPAM": 0.0, "NOT_SPAM": 1.0}}),
#         ("What are you up to?", {"cats": {"SPAM": 0.0, "NOT_SPAM": 1.0}}),
#     ]

#     # Define the pipeline for the spam classification model
#     pipe_config = {
#         'pipeline': [
#             {'name': 'textcat_multilabel', 'cfg': {'exclusive_classes': True, 'architecture': 'simple_cnn'}}
#         ]
#     }
#     LABELS= ["SPAM", "NOT_SPAM"]

#     # Create a new spaCy pipeline for the spam classification model
#     spam_pipe = spacy.blank('en')
#     spam_pipe.from_config(pipe_config)
#     # spam_pipe.initialize(lambda: iter([nlp.make_doc("")] * 10), **pipe_config)


#     # Add the spam classification labels to the pipeline
#     textcat = spam_pipe.create_pipe("textcat_multilabel", config={"exclusive_classes": True})
#     for label in LABELS:
#         textcat.add_label(label)
#     spam_pipe.add_pipe(textcat)
#     # Define the optimizer for the spam classification model
#     optimizer = spam_pipe.begin_training()

#     # Train the spam classification model
#     for i in range(10):
#         # Shuffle the training data
#         random.shuffle(TRAIN_DATA)
#         # Create minibatches of the training data
#         batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
#         # Train the model on each minibatch
#         for batch in batches:
#             texts, annotations = zip(*batch)
#             spam_pipe.update(texts, annotations, sgd=optimizer)
#     return spam_pipe(message)

# def spammed_message(message):
#     nlp = spacy.blank('en')
#     textcat = nlp.add_pipe("textcat_multilabel", config={
#         "exclusive_classes": True,
#         "architecture": "simple_cnn",
#         "textcat_multilabel": {
#             "labels": ["SPAM", "NOT_SPAM"]
#         }
#     })
#     optimizer = nlp.begin_training()
#     TRAIN_DATA = [
#         ("Send me money now", {"cats": {"SPAM": 1.0, "NOT_SPAM": 0.0}}),
#         ("Earn money fast", {"cats": {"SPAM": 1.0, "NOT_SPAM": 0.0}}),
#         ("Hey, how are you?", {"cats": {"SPAM": 0.0, "NOT_SPAM": 1.0}}),
#         ("What are you up to?", {"cats": {"SPAM": 0.0, "NOT_SPAM": 1.0}}),
#     ]
#     for i in range(10):
#         random.shuffle(TRAIN_DATA)
#         losses = {}
#         batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
#         for batch in batches:
#             examples = []
#             for text, annotations in batch:
#                 examples.append(Example.from_dict(nlp.make_doc(text), annotations))
#             nlp.update(examples, sgd=optimizer, losses=losses)
#     doc = nlp(message)
#     return doc.cats["SPAM"]


