import math
import operator
import copy
import csv


class KNN:
    # konstanty: nehrabat
    training_base = 300
    neighbours = 3
    topics = ["po", "pr", "ze", "sp", "ku", "kr", "pc", "ji", "-"]
    # Index tematu v CSV (self.tweets)
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

        while self.training_count > len(tweets):
            self.training_count = self.training_count / 2

    def start(self):
        # Prepare file for ouput
        outputFile = open("detected.csv", "w+", encoding='utf-8', newline='')
        writer = csv.writer(outputFile, delimiter=';', quotechar=None)

        # For tweets that are not in training set do
        for i in range(self.training_count, len(self.tweets)):
            current_tweet = self.tweets[i]
            current_vector = self.vectors[i]
            tweet_point = []

            # Vypocet vzdalenosti od trenovaciho setu
            for j in range(0, self.training_count):
                training_tweet = self.tweets[j]
                training_vector = self.vectors[j]
                distance = self.calc_distance(current_vector, training_vector)
                tweet_point.append([training_tweet[self.topic_index], distance])

            # Zesortíme body
            tweet_point.sort(key=lambda x: x[1])

            # Nalezene typy
            mark_topic = '-'
            found_topics = {}
            for k in range(0, self.neighbours):
                if len(tweet_point) <= k:
                    break

                # prvnich n vzdalenosti
                tweet_topic = tweet_point[k][0]

                if tweet_topic in found_topics:
                    found_topics[tweet_topic] = found_topics[tweet_topic] + 1
                else:
                    found_topics[tweet_topic] = 1

            found_topics = sorted(found_topics.items(), key=operator.itemgetter(1), reverse=True)
            mark_topic = found_topics[0][0]
            tweet_detected = copy.copy(current_tweet)

            # TODO: Mozna pri overovani pocitat Fmiru a dalsi blbosti
            if (mark_topic == '-'):
                tweet_detected[self.event_index] = 0
                tweet_detected[self.topic_index] = mark_topic
            else:
                tweet_detected[self.event_index] = 1
                tweet_detected[self.topic_index] = mark_topic
            # Write to ouput file
            writer.writerow(tweet_detected)
        # Close file
        outputFile.close()

    # vypocet euklidovské vzdalenosti mezi dvema vektory
    def calc_distance(self, vectorA, vectorB):
        distance = 0.0
        for i in range(0, len(vectorA)):
            dist = vectorA[i] - vectorB[i]
            distance = distance + (dist * dist)
        return math.sqrt(distance)
