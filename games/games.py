from games.Wordle import wordle
from games.Wordle_assist import wordle_assist

def game_data(obj,info):
    data={}
    if obj=='wordle':
        data['gamedata']={
            'words':wordle.get_words()
        }
    if obj=='wordle_assist':
        pass
    return data