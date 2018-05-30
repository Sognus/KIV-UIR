import csv
import re
import unidecode


class NGram:

    def __init__(self, filename):
        # jmeno textove reprezentace
        self.name = "ngram"
        # csv soubor ze ktereho se nacita
        self.filename = filename
        # Nactene radky
        self.tweets = {}
        # Seznam slov
        self.words = {}
        # Seznam vectoru
        self.vectors = []
        # Index, kde jsou slova v csv radku
        self.word_index = 5

    def load_csv(self):
        words = []
        with open(self.filename, mode="r", encoding='utf-8') as csvf:
            reader = csv.reader(csvf, quotechar=None, delimiter=";")
            for i, line in enumerate(reader):
                # Load tweets - whole csv lines
                self.tweets[i] = line
                tweet_text = line[self.word_index]
                words += self.create_words(tweet_text)
        #  Calculate phrase occurence
        for word in words:
            if word in self.words:
                self.words[word] += 1
            else:
                self.words[word] = 1

    def create_vector(self):
        for i in range(0, len(self.tweets)):
            # prave vytvareny vector
            vector = list()
            current_tweet = self.tweets[i]
            current_text = current_tweet[self.word_index]
            current_tweet_words = self.create_words(current_text)
            # for each found word 2-tuple check if 2-tuple is present in current vector
            for y in self.words:
                if y in current_tweet_words:
                    vector.append(self.words[y])
                else:
                    vector.append(0.0)
            self.vectors.append(vector)

    # Get list
    def create_words(self, tweet_text):
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
            tweet_filtered.append(word)
        # after cycle
        # For every filtered word we need to create 2-tuples
        last = ""
        for i in range(0, len(tweet_filtered)):
            if last == "" and tweet_filtered[i] != "" and tweet_filtered[i] is not None:
                last = tweet_filtered[i]
                continue
            if tweet_filtered[i] != "" and tweet_filtered[i] is not None:
                list_of_words.append(last + " " + tweet_filtered[i])
                last = tweet_filtered[i]
        return list_of_words

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
