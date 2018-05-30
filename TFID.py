import csv
import unidecode
import re
import math


class TFID:

    def __init__(self, filename):
        # jmeno textove reprezentace
        self.name = "tfid"
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

    # Load csv and create words list
    def load_csv(self):
        words = []
        with open(self.filename, mode="r", encoding='utf-8') as csvf:
            reader = csv.reader(csvf, quotechar=None, delimiter=";")
            for i, line in enumerate(reader):
                # Load tweets - whole csv lines
                self.tweets[i] = line
                tweet_text = line[self.word_index]
                words += self.get_words(tweet_text)
        #  Calculate word occurence
        for word in words:
            if word in self.words:
                self.words[word] += 1
            else:
                self.words[word] = 1

    # Get words from tweet
    def get_words(self, tweet_text):
        tweet_arr = tweet_text.split(' ');
        tweet_filtered = []
        list_of_words = []
        for i in range(0, len(tweet_arr)):
            word = tweet_arr[i]
            regex = re.compile('[^ěščřžýáíéóúůďťňĎŇŤŠČŘŽÝÁÍÉÚŮa-zA-Z]')
            word = regex.sub('', word)
            word = unidecode.unidecode(word)
            word = word.lower()
            word = self.word_filter(word)
            if word.isspace() or word == "" or word == '\n':
                continue
            # Add filtered word to its respective lists
            tweet_filtered.append(word)
            list_of_words.append(word)
        # return created list of words
        return list_of_words

    def create_vector(self):
        # For all tweets
        for i in range(0, len(self.tweets)):
            vector = [0] * len(self.words)
            current_tweet = self.tweets[i]
            current_text = current_tweet[self.word_index]
            # Slova aktualniho tweetu
            current_tweet_words = self.get_words(current_text)
            # A pro vsechna slova nalezena udelej nasledujici
            for y in range(0, len(current_tweet_words)):
                word = current_tweet_words[y]
                if word in self.words.keys():
                    # Zjisteni ktery index vektoru upravit
                    index = list(self.words.keys()).index(word)
                    # pocet vyskytu slova ve tweetu
                    tfcount = current_tweet_words.count(word)
                    # pocet_vyskytu_slova_ve_tweetu / pocet_slov_tweetu
                    tf = tfcount / len(current_tweet_words)
                    # pocet tweetu
                    idfcount = len(self.tweets)
                    # pocet_tweetu / pocet_vyskytu_slova
                    idf = math.log(idfcount / self.words[word])
                    # soucin tf * idf
                    val = tf * idf
                    # update index
                    vector[index] = val
            # Add vector to storage
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
