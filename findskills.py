import nltk
from nltk.tokenize import word_tokenize
from string import punctuation

PUNCTUATION = list(punctuation)

SKILLS_SECTION = [
    "what do you bring",
    "qualifications",
    "requirements",
    "must haves",
    "what you will do",
    "minimum requirements",
    "preferred qualifications",
    "skills",
    "keys to your success",
    "about you",
    "required skills",
    "who you are"
]

OTHER_SECTIONS = [
    "responsibilities",
    "workplace information",
    "about us",
    "who we are",
    "role location",
    "position description",
    "job duties and responsibilities",
    "company overview",
    "the position",
    "join us",
    "who we are",
    "compensation and benefits",
    "why work with us?",
    "company overview",
    "about the role",
    "about the possition",
]

# determine if the current line is a skill or not
def find_skills(possible_skill_line):

    # following module 5 
    # Noun phrase (e.g. Java, ability to work independently, university degree, written communication)
        # Java -> NN
        # ability to work independently -> NN TO VB RB
        # university degree -> NN NN
        # written communication -> VBN NN
    # Verb phrase (e.g., develop web application, design software)
    # Noun + Gerund (e.g., problem solving, web programming)
    
    # tokenize the string
    string_tokenized = word_tokenize(possible_skill_line)
    words = []
    # remove punctuation
    for word in string_tokenized:
        if word not in PUNCTUATION:
            words.append(word)
    # use part of speach (pos) tagging for the tokens
    # for word_tuple in word_types:
    #     word = word_tuple[0]
    #     pos = word_tuple[1]
    word_types = nltk.pos_tag(words)
    # if we get an empty string return nothing
    if not word_types:
        return []
    
    # if it is a noun phrase return the skill line
    if noun_phrase(word_types):
        return [possible_skill_line]
    
    # if it is a verb phrase return the skill line
    if verb_phrase(word_types):
        return [possible_skill_line]
    
    # if it is a gerund phrase return the skill line
    if gerund_phrase(word_types):
        return [possible_skill_line]
    
    # if the first two words are "you" and "are"
    # return this word split on "you are"
    if words[:2] == ["you","are"]:
        return you_are_phrase(word_types)

    return []

# you are phrase returns a list of skills
def you_are_phrase(sentence):
    # get the words in the sentence
    words = list(dict(sentence).keys())
    you_indexes = []
    are_indexes = []
    you_are_indexes = []
    # find the indexs of you and are
    for index in range(len(words)):
        if words[index] == "you":
            you_indexes.append(index)
        if words[index] == "are":
            are_indexes.append(index)
    # if are if right after you, add the you index to you_are_indexes
    for index in you_indexes:
        if index+1 in are_indexes:
            you_are_indexes.append(index)
    
    skill_phrases = []
    # split the words into sentences based on the you are indexes
    # ['you' 'are' 'independent' 'you' 'are' 'a' 'self' 'starter']
    # becomes
    # [["you" "are" "independent"] ["you" "are" "a" "self" "starter""]]
    phrases = [words[i:j] for i, j in zip([0] + you_are_indexes, you_are_indexes + [None])]
    # for each phrase
    for phrase in phrases:
        # if the phrase is more than just "you are" ie more than 2 words long
        if len(phrase) > 2:
            # this check is reduntance but we leave it here to double check
            if phrase[0] == "you" and phrase[1] == "are":
                # we create a sub array starting at the word after "are"
                skill = phrase[2:]
                # join all the words to create a single string
                skill_phrase = ' '.join(skill)
                # append this phrase to our skill phrases
                skill_phrases.append(skill_phrase)
    # return an array of string, which are all skills
    return skill_phrases

# returns tru if the phrase is a noun phrase
def noun_phrase(sentence):
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

# returns true if the sentence is a verb phrase
def verb_phrase(sentence):
    if(sentence[0][1] == "VB"): #just a verb
        return True
    if(len(sentence) > 1):
        if(sentence[0][1] == 'RB' and sentence[1][1] == "VB"):
            return True
    return False

# returns true if the sentence is a gerund phrase
def gerund_phrase(sentence):
    if(sentence[0][1] == "VBG" and len(sentence) > 1 and sentence[1][1] == "NN"): #gerund noun
        return True
    return False
        #verb phrase = [Adv] V [NP]
        #noun v-ing