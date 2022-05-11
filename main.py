import requests
from bs4 import BeautifulSoup

html = ''
with open('data-files/html.txt') as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')

def get_boxes():
    Boxes = {}
    for val in soup.find_all('td'):
        style = val.get('style')
        if(style):
            coordinates = val.get('id')[3:].split(',')
            if(not coordinates[0][0].isdigit()): continue
            height = int(style[style.find("height:")+len("height: ")
                                    : style.find("height:")+len("height: ")+1])
            if(height > 3): continue
            color = style[style.find("var", style.find(
                "var") + 1) + len("var(--"):style.find("var", style.find("var") + 1)+len("var(--")+1]
            letter = val.get_text().lower()
            col = coordinates[-1]
            blacks = letter + col if(color == 'b') else ''
            yellows = letter + col if(color == 'y') else ''
            greens = letter + col if(color == 'g') else ''
        
            current_box = coordinates[0]
            if(current_box in Boxes):
                Boxes[current_box]["blacks"] =  Boxes[current_box]["blacks"] + blacks
                Boxes[current_box]["yellows"] =  Boxes[current_box]["yellows"] + yellows
                Boxes[current_box]["greens"] =  Boxes[current_box]["greens"] + greens
            else:
                Boxes[current_box] = {"blacks": blacks, "yellows": yellows, "greens": greens}
    return Boxes



def read_file(file_name):
    contents = ''
    with open(file_name) as f:
        contents = f.read()
    return contents.split('\n')

def solve(black, yellow, green):
    words = read_file('data-files/english3.txt')
    possible_words = []
    if(len(green) >= 10):
        last_row = green[-10:]
        j = 1
        answer = ''
        correct = True
        for i in range(5):
            if(str(i+1) != last_row[j]):
                correct = False
                break
            j = j + 2
        if correct:
            for e in last_row[0::2]:
                answer += e
            return ["[SOLVED] (was " + answer + ")"]
    for i in range(len(words)):
        word = words[i]
        if len(word) != 5:
            continue
        canidate = True
        for j, letter in enumerate(black):
            if(letter in word and letter not in yellow and letter not in green):
                canidate = False
                break
        if not canidate:
            continue
        if len(yellow) > 1:
            for j in range(0, len(yellow) - 1, 2):

                letter = yellow[j]
                if letter not in word:
                    canidate = False
                    break
                yellow_index = yellow[j + 1]
                letter_locale = word.index(letter) + 1
                if int(letter_locale) == int(yellow_index):
                    canidate = False
                    break
        if not canidate:
            continue
        if len(green) > 1:
            for k in range(0, len(green) - 1, 2):
                letter = green[k]
                if letter not in word:
                    canidate = False
                    break
                letter_locale = word.index(letter) + 1
                green_index = green[k + 1]
                if word[int(green_index) - 1] != letter:
                    canidate = False
                    break
        if canidate:
            possible_words.append(word)
    
    return possible_words

def print_results(Boxes):
    pq = []
    solved_pq = []
    for key in Boxes:
        data = Boxes[key]
        key = "0" + key if int(key) < 10 else key
        words = solve(data["blacks"], data["yellows"], data["greens"])
        if("SOLVED" in ''.join(words)):
            solved_pq.append("[" + key + "] -> " + ', '.join(words))
        else:
            pq.append("[" + key + "] -> " + ', '.join(words))
    
    pq.sort(reverse=True, key=len)
    solved_pq.sort(reverse=True)
    print("\n".join(solved_pq))
    print("\n".join(pq))

def main():
    
    print_results(get_boxes())

main()