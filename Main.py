import json
import os

from modules.GetSubtitles import get_subtitles
from modules.storyGetter import story_getter
from modules.Speechify2 import speechify2
from modules.Speechify import speechify
from modules.Partify import partify
from modules.BgAdder import bg_adder
from modules.Speedify import speedify
from modules.ssGetter import ss_getter
from modules.addSubtitles import add_subtitles
from pushbullet import Pushbullet
import modules.deleter as deleter

def text_saver():
    with open('modules/stories.json', 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    for index,story in enumerate(data,start=1):
        with open(f'VideoFinal/Story{index}/story{index}.txt','w',encoding='utf-8') as f:
            f.write(story['title'])
            f.write(story['content'])


pb=Pushbullet("o.uhvrEttwLRN1Mzf80nW0l9hc7w0ltiPj")
try:
    os.makedirs('temps',exist_ok=True)
    pb.push_note("Fabrica de clipuri","A inceput fabrica de clipuri")
    x = int(input("Cate clipuri facem astazi sefule?\n"))
    sub=int(input("Cu ce sub-reddit sa facem azi?\n0 - stories\n1 - Am I the asshole\n2 - nosleep (horror)\n3 - Today I fucked up\n"))
    while 0 > sub > 3:
        print("Trebuie sa alegi una din ele\n\n")
        sub = int(input("Cu ce sub-reddit sa facem azi?\n0 - stories\n1 - Am I the asshole\n2 - nosleep (horror)\n3 - Today I fucked up\n"))

    print(f"Se procura {x} povesti\n")
    # story_getter(x,sub)
    print("Hai sa facem si vocile pentru povestile astea\n")
    speechify()
    # speechify2()
    print("Tre sa le grabim putin\n")
    # speedify()
    print("Si acum sa le impartim\n")
    partify("temps/StoryVocal")
    print("Daca tot le am impartit, le facem si subtitrari\n")
    get_subtitles(False)
    print("facem o poza pentru fiecare postare si sanatate")
    ss_getter()
    print("adaugam suntetul pe fundal")
    bg_adder()
    pb.push_note("Fabrica de clipuri","S-au facut clippurile fara subtitrari")
    print("acum avem de toate si ai de stat vreo 10 min per clip sa se faca")
    add_subtitles()
    print(f'\n\nGATA BOSSULE\nACUM AI CLIPURI CU {x} povesti')

    deleter.delete_temps()
    pb.push_note("Fabrica de clipuri",f"S-au terminat clipurile")
except Exception as e:
    pb.push_note("Eroare",f"Se pare ca a dat eroare, na si eroare sa vezi si tu {e}")
    print(e)
