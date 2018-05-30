class Cluster:

    def __init__(self, vector):
        self.centroid = vector
        self.tweets = []
        self.vectors = []

    # přidá tweet a vector ke clusteru
    def add_tweet(self, tweet, vector):
        self.tweets.append(tweet)
        self.vectors.append(vector)

    def recalculate(self):
        # Nelze provest prepocet pokud nejsou zadne vektory ze kterych by se pocitalo
        if len(self.tweets) < 1 or len(self.vectors) < 1:
            return False

        # Velikost vektoru
        size = len(self.vectors[0])

        # Pro kazdy tweet prirazeny k tezisti
        for i in range(0, len(self.vectors)):
            vector = self.vectors[i]
            # Pro vsechny dimenze vektoru
            for y in range(0, size):
                self.centroid[y] += vector[y]
        # Pro vsechny dimenze teziste vypocitej prumer
        for z in range(0, size):
            self.centroid[z] /= size
