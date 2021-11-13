import os
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation

PUNCTUATION = list(punctuation)

def find_skills(possible_skill_line):
    #proccessed_job_descriptions = read_proccessed_job_descritions()
    #processed_word_type_sentences = read_processed_word_type_sentences()

    SKILLS_SECTION = ["What do you bring", "qualifications", "requirements", "responsibilities", "must haves", "What you will do"]

    # following module 5 
    # Noun phrase (e.g., Java, ability to work independently, university degree, written communication)
        # Java -> NN
        # ability to work independently -> NN TO VB RB
        # university degree -> NN NN
        # written communication -> VBN NN
    # Verb phrase (e.g., develop web application, design software)
    # Noun + Gerund (e.g., problem solving, web programming)
    
    string_tokenized = word_tokenize(possible_skill_line)
    words = []
    for word in string_tokenized:
        if word not in PUNCTUATION:
            words.append(word)
    word_types = nltk.pos_tag(words)
    if not word_types:
        return []
    
    if noun_phrase(word_types):
        return [possible_skill_line]
    
    if verb_phrase(word_types):
        return [possible_skill_line]
    
    if gerund_phrase(word_types):
        return [possible_skill_line]
    
    if words[:2] == ["you","are"]:
        return you_are_phrase(word_types)

    return []

    # for word_tuple in word_types:
    #     word = word_tuple[0]
    #     pos = word_tuple[1]

def you_are_phrase(sentence):
    words = list(dict(sentence).keys())
    you_indexes = []
    are_indexes = []
    you_are_indexes = []
    for index in range(len(words)):
        if words[index] == "you":
            you_indexes.append(index)
        if words[index] == "are":
            are_indexes.append(index)
    for index in you_indexes:
        if index+1 in are_indexes:
            you_are_indexes.append(index)
    
    skill_phrases = []
    phrases = [words[i:j] for i, j in zip([0] + you_are_indexes, you_are_indexes + [None])]
    for phrase in phrases:
        if len(phrase) > 2:
            if phrase[0] == "you" and phrase[1] == "are":
                skill = phrase[2:]
                skill_phrase = ' '.join(skill)
                skill_phrases.append(skill_phrase)
    return skill_phrases

def noun_phrase(sentence):
    # print(sentence)
    if(sentence[0][1] == "NN"): #just a noun
        return True
    if(len(sentence) > 1):
        if(sentence[0][1] == 'VBN' and sentence[1][1] == "NN"): #descriptor noun
            return True
        if(sentence[0][1] == "DT" and sentence[1][1] == "NN"): #determinate noun
            return True
    return False
    # Noun phrase (e.g., Java, ability to work independently, university degree, written communication)
        # Java -> NN
        # ability to work independently -> NN TO VB RB
        # university degree -> NN NN
        # written communication -> VBN NN
        
        #noun phrase = [DT or VBN] N [PP]
        # PP = P DP
        # DP -> D NP
        # NP -> N PP
        # PP -> P DP
def verb_phrase(sentence):
    if(sentence[0][1] == "VB"): #just a verb
        return True
    if(len(sentence) > 1):
        if(sentence[0][1] == 'RB' and sentence[1][1] == "VB"):
            return True
    return False

def gerund_phrase(sentence):
    if(sentence[0][1] == "VBG" and len(sentence) > 1 and sentence[1][1] == "NN"): #gerund noun
        return True
    return False
        #verb phrase = [Adv] V [NP]
        #noun v-ing

    #probably some kind of word type processing at this point
    #picking only ones that are skills
    #skills start with 'you' or 


    #sort by frequency

def read_proccessed_job_descritions():
    here = os.path.dirname(os.path.abspath(__file__))
    read_file_path = os.path.join(here, 'processed_software_engineering.txt')
    with open(read_file_path, 'r', encoding='utf8') as f:
        proccessed_job_descriptions = f.readlines()
    return proccessed_job_descriptions

def read_processed_word_type_sentences():
    here = os.path.dirname(os.path.abspath(__file__))
    read_file_path_2 = os.path.join(here, 'word_type_software_engineering.txt')
    with open(read_file_path_2, 'r', encoding='utf8') as f:
        processed_word_type_sentences = f.readlines()
    return processed_word_type_sentences