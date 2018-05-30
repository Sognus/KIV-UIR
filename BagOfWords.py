import unidecode
import re
import csv


class BagOfWords:

    def __init__(self, filename):
        # jmeno textove reprezentace
        self.name = "bag_of_words"
        # csv soubor ze ktereho se nacita
        self.filename = filename
        # Nactene radky
        self.tweets = {}
        # Seznam slov
        self.words = {}
        # Seznam vectoru
        self.vectors = {}
        # Index, kde jsou slova v csv radku
        self.word_index = 5

    def load_csv(self):
        with open(self.filename, mode="r", encoding='utf-8') as csvf:
            reader = csv.reader(csvf, quotechar=None, delimiter=";")
            for i, line in enumerate(reader):
                # Load tweets - whole csv lines
                self.tweets[i] = line
                # Split word part to get words alone
                words_split = self.tweets[i][self.word_index].split(' ')
                # For each found word, edit and filter it and add it to dict
                for word in words_split:
                    regex = re.compile('[^ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮa-zA-Z]')
                    word = regex.sub('', word)
                    word = unidecode.unidecode(word)
                    word = word.lower()
                    word = self.word_filter(word)
                    if word.isspace() or word == "" or word == '\n':
                        continue
                    if word in self.words:
                        self.words[word] = self.words[word] + 1;
                        # print("{}: +1".format(word))
                    else:
                        self.words[word] = 1
                        # print("{}: added".format(word))

    def create_vector(self):
        for i in range(0, len(self.tweets)):
            # prave vytvareny vector
            vector = list()
            # Seznam slov z jednotlivych tweetu
            word_arr = self.tweets[i][self.word_index].split(' ')
            word_filtered = list()
            # Change words - filter bad chars - strip diacritics
            for word in word_arr:
                regex = re.compile('[^ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮa-zA-Z]')
                word = regex.sub('', word)
                word = unidecode.unidecode(word)
                word = word.lower()
                word = self.word_filter(word)
                if word.isspace() or word == "" or word == '\n':
                    continue
                word_filtered.append(word)
            # After cycle
            # For each word in dictionary - check if line contains that word
            for wrd in self.words:
                if wrd in word_filtered:
                    vector.append(1.0)
                else:
                    vector.append(0.0)
            # After cycle
            self.vectors[i] = vector

    def word_filter(self, word):
        filter = ["CT24zive", "echocz", "rt", "zpravy", "dnes", "byl", "by", "jen", "jsme",
                  "bylo", "mu", "ma", "ho", "cr", "cz", "ale", "via", "uz", "i", "a", "tak", "kam", "jestli", "protoze",
                  "zatim", "nebo", "dalsi", "prekvapilo", "konecne", "zacina", "bude", "nebude", "takto", "bez", "beze",
                  "blizko", "dle", "do", "k", "ke", "kol", "krom", "krome", "ku", "kvuli", "mezi", "mimo", "na", "nad",
                  "nade", "naproti", "si", "je", "navzdory", "nedaleko", "o", "ob", "od", "ode", "ohledne", "okolo",
                  "oproti", "po", "pobliz", "pod", "pode", "podel", "podle", "podleva", "podliva", "pomoci", "pred",
                  "prede", "pres", "prese", "pri", "pro", "prostrednictvim", "proti", "s", "se", "skrz", "skrze",
                  "stran",
                  "u", "uprostred", "v", "vcetne", "ve", "vedle", "versus", "vinou", "vne", "vo", "vod", "vstric",
                  "vuci",
                  "vukol", "vz", "vzdor", "vzhledem", "z", "za", "ze", "zkraje", "zpod", "zpoza", "an", "ana", "ano",
                  "any", "buhvico", "buhvikdo", "ci", "cisi", "co", "cokoli", "cokoliv", "copak", "cos", "cosi", "coz",
                  "coze", "ja", "jakkoli", "jakovy", "jaky", "jaka", "jake", "jaci", "jakykoli", "jakakoli", "jakekoli",
                  "jacikoli", "jakykoliv", "jakakoliv", "jakekoliv", "jacikoliv", "jakysi", "jakasi", "jakesi",
                  "jacisi",
                  "jeho", "jehoz", "jejiz", "jeji", "jejich", "jejichz", "jejiz", "jenz", "jiz", "jez", "jich", "kazdy",
                  "kdekoli", "kdekoliv", "kdo", "kdokoli", "kdokoliv", "kdosi", "kdy", "kdykoli", "kdykoliv", "kterej",
                  "ktery", "ktera", "ktere", "kteri", "kterykoliv", "ky", "lecco", "leckdo", "lecktery", "lecktera",
                  "lecktere", "leckteri", "malokdo", "me", "muj", "moje", "my", "my", "mi", "naky", "naka", "nake",
                  "naci", "nas", "nase", "nasi", "neci", "neco", "nejaky", "nejaka", "nejake", "nejaci", "nekdo",
                  "nektery", "nektera", "nektere", "nekteri", "nesvuj", "nesva", "nesve", "nesvi", "nic", "nici",
                  "nikdo",
                  "nizadny", "nizadna", "nizadne", "nizadni", "odkdy", "on", "ona", "onano", "onen", "oni", "ono",
                  "ony",
                  "pranic", "prazadny", "prazadna", "prazadne", "prazadni", "sa", "sam", "sama", "samo", "sami", "samy",
                  "sama", "same", "sami", "se", "svuj", "sva", "sve", "svi", "svoje", "svoji", "ta", "tenhle", "tahle",
                  "tohle", "tihle", "takovy", "takova", "takove", "takovi", "takovyhle", "takovahle", "takovehle",
                  "takovihle", "takovyto", "takovato", "takoveto", "takovito", "taky", "taka", "take", "taci", "tato",
                  "ten", "tenhle", "tento", "tentyz", "ti", "tito", "to", "tohle", "toto", "tuten", "tvuj", "ty",
                  "tyto",
                  "tyz", "vas", "vesker", "veskery", "von", "vse", "vsecek", "vsechen", "vsechno", "vseliky", "vy"]
        if word in filter:
            return ""
        else:
            return word
