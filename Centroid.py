from Cluster import Cluster
import csv
import math


class Centroid:

    # konstanty: nehrabat
    training_base = 300
    # pozice tematu v tweetu
    topic_index = 1
    # Index zda se jedna o event v CSV (self.tweets)
    event_index = 0


    def __init__(self, tweets, vectors):
        # Nactene radky
        self.tweets = tweets
        # K radkum vytvorene vektory
        self.vectors = vectors
        # Velikost trenovaci mnoziny
        self.training_count = self.training_base
        # teziste
        self.clusters = {}

        while self.training_count > len(tweets):
            self.training_count = self.training_count / 2

    def start(self):
        # Prepare file for ouput
        outputFile = open("detected.csv", "w+", encoding='utf-8', newline='')
        writer = csv.writer(outputFile, delimiter=';', quotechar=None)

        # Pridani tweetu z trenovaci mnoziny do shluku
        for i in range(0, self.training_count):
            tweet_training = self.tweets[i]
            vector_training = self.vectors[i]
            topic_training = tweet_training[self.topic_index]
            # Add new topic if it was not added yet
            if topic_training not in self.clusters:
                self.clusters[topic_training] = Cluster(self.vectors[i])
            cluster = self.clusters[topic_training]
            cluster.add_tweet(tweet_training, vector_training)
            cluster.recalculate()

        # Detekce tematu
        # Pro kazdy tweet z mnoziny pro detekovani udelej:
        for y in range(self.training_count, len(self.tweets)):
            curr_tweet = self.tweets[y]
            curr_vec = self.vectors[y]
            nearest_dist = float("Inf")
            nearest_topic = '-'
            # For every cluster keyval pair do:
            for clusterKey, clusterValue in self.clusters.items():
                # topic
                curr_topic = clusterKey
                curr_centroid = clusterValue.centroid
                distance = self.calc_distance(curr_vec, curr_centroid)
                if distance < nearest_dist:
                    nearest_dist = distance
                    nearest_topic = curr_topic
            # Prepare tweet to write to output
            tweet_detected = curr_tweet
            if (nearest_topic == '-'):
                tweet_detected[self.event_index] = 0
                tweet_detected[self.topic_index] = nearest_topic
            else:
                tweet_detected[self.event_index] = 1
                tweet_detected[self.topic_index] = nearest_topic
            # Write row to csv
            writer.writerow(tweet_detected)
        # After everything close fileHandler
        outputFile.close()

    # vypocet euklidovské vzdalenosti mezi dvema vektory
    def calc_distance(self, vectorA, vectorB):
        distance = 0.0
        for i in range(0, len(vectorA)):
            dist = vectorA[i] - vectorB[i]
            distance = distance + (dist * dist)
        return math.sqrt(distance)




