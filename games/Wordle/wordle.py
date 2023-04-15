guess_max=6
colors={'green':'green','yellow':'gold','grey':'dimgrey'}

def get_words():
    return [[{'value':'m','color':colors['grey']} for i in range(5)]
                    for j in range(guess_max)]