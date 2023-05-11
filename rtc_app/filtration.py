from better_profanity import profanity
from collections import Counter

def word_filter(sentence):
    # profanity.load_censor_words_from_file('/home/imlog/Downloads/abusive_words.txt')
    # return profanity.contains_profanity(sentence)
    return profanity.censor(sentence)

def simi_percentage(hash_values):
    c= Counter(hash_values)
    max_count= max(c.values())
    count= len(hash_values)
    percentage= (max_count/count)*100
    return percentage