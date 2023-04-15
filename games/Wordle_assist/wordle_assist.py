def get_right_word(words,green,yellow,gray):
    right_word=[]
    for k in list(green.keys()):
        if green[k] in gray:
            green.pop(k)
    for k in list(yellow.keys()):
        if k in gray:
            yellow.pop(k)
    for word in words:
        right=True
        for k in green:
            if word[k]!=green[k]:
                right=False
        for k in yellow:
            if k not in word:
                right=False
            for i in yellow[k]:
                if word[i]==k:
                    right=False
        for g in gray:
            if g in word:
                right=False
        if right:
            right_word.append(word)
    return right_word

def preview_words(green,yellow,gray):
    f=open('games/Wordle_assist/wordle.txt','r')
    wordle=f.read()
    f.close()
    words=wordle.split('\n')
    right_word=get_right_word(words,green,yellow,gray)
    scores=dict(zip(right_word,[0 for i in range(len(right_word))]))
    for v in right_word:
        other_word=right_word.copy()
        other_word.pop(other_word.index(v))
        scores[v]=0
        for w in other_word:
            Green,Yellow,Gray={},{},set()
            for i in range(len(v)):
                if v[i]==w[i]:
                    Green[i]=v[i]
                if v[i]!=w[i] and v[i] in w:
                    if v[i] not in Yellow.keys():
                        Yellow[v[i]]=set()
                    Yellow[v[i]].add(i)
                if v[i]!=w[i] and v[i] not in w:
                    Gray.add(v[i])
            for k in list(Green.keys()):
                if Green[k] in Gray:
                    Green.pop(k)
            for k in list(Yellow.keys()):
                if k in Gray:
                    Yellow.pop(k)
            score=len(get_right_word(right_word,Green,Yellow,Gray))
            scores[v]+=score
    min_score=min(scores.values())
    best_word=set()
    for k in scores:
        if scores[k]==min_score:
            best_word.add(k)
    return best_word

# print(preview_words({1:'i',3:'c'},{'e':{3}},{'r','a','s','d','f'}))