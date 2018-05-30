from Statistic import Statistic
import csv
import math


# Vsechny statistiky
class Statistics:
    # Kolekce statistik
    stats = {}
    keys = {}

    # Konstanty
    # CSV index topics
    topic_index = 1

    # Celkova spravnost
    good = 0
    bad = 0

    def __init__(self, inputFile, outputFile, trainingCount):
        self.create_stats()
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.trainingCount = trainingCount
        self.create_topic_map()
        self.calculate_statistics()
        pass

    def create_stats(self):
        self.stats['po'] = Statistic('po')
        self.stats['pr'] = Statistic('pr')
        self.stats['ze'] = Statistic('ze')
        self.stats['sp'] = Statistic('sp')
        self.stats['ku'] = Statistic('ku')
        self.stats['kr'] = Statistic('kr')
        self.stats['pc'] = Statistic('pc')
        self.stats['ji'] = Statistic('ji')

    def create_topic_map(self):
        self.keys['po'] = "POLITICS"
        self.keys['pr'] = "INDUSTRY"
        self.keys['ze'] = "AGRICULTURE"
        self.keys['sp'] = "SPORT"
        self.keys['ku'] = "CULTURE"
        self.keys['kr'] = "CRIME"
        self.keys['pc'] = "WEATHER"
        self.keys['ji'] = "OTHER"

    def get_stats(self, zkratka):
        if zkratka not in self.stats.keys():
            return None
        else:
            return self.stats[zkratka]

    def calculate_statistics(self):
        csv_input = open(self.inputFile, mode="r", encoding='utf-8')
        input_reader = csv.reader(csv_input, quotechar=None, delimiter=";")
        csv_output = open(self.outputFile, mode="r", encoding='utf-8')
        output_reader = csv.reader(csv_output, quotechar=None, delimiter=";")

        # Read non training rows from input CSV
        input_lines = []
        for input_row in input_reader:
            if input_reader.line_num > self.trainingCount:
                input_lines.append(input_row)

        # Read all lines from ouput CSV
        output_lines = []
        for output_row in output_reader:
            output_lines.append(output_row)

        # For every line loaded we need to evaluate
        for i in range(0, len(output_lines)):
            expected = input_lines[i]
            real = output_lines[i]
            expected_topic = expected[self.topic_index]
            real_topic = real[self.topic_index]
            if expected_topic == real_topic:
                self.good += 1
                # Add True NEGATIVE for every other topic
                for topicKey in self.stats:
                    if topicKey != expected_topic:
                        self.get_stats(topicKey).tn += 1
                # Add true positive for correct detection
                self.get_stats(expected_topic).tp += 1
            else:
                self.bad += 1
                # Add TRUE
                self.get_stats(expected_topic).fp += 1
                self.get_stats(real_topic).fn += 1

        # Close files after done reading from them
        csv_input.close()
        csv_output.close()

    def print_complete_stat(self):
        total = self.good + self.bad
        all = [0] * 5
        ok = [0] * 5
        for i in range(0, len(self.stats.keys())):
            stat = self.get_stats(list(self.stats.keys())[i])
            topicTweets = stat.fn + stat.tp
            ratio = topicTweets / total

            precision = stat.precision()
            if not math.isnan(precision):
                ok[0] += 1.0 * ratio
                all[0] += precision * ratio

            recall = stat.recall()
            if not math.isnan(recall):
                ok[1] += 1.0 * ratio
                all[1] += recall * ratio

            fmeasure = stat.fmeasure()
            if not math.isnan(fmeasure):
                ok[2] += 1.0 * ratio
                all[2] += fmeasure * ratio

            error = stat.error()
            if not math.isnan(error):
                ok[3] += 1.0 * ratio
                all[3] += error * ratio

            acc = stat.accuracy()
            if not math.isnan(acc):
                ok[4] += 1.0 * ratio
                all[4] += acc * ratio

        # After cycle
        for y in range(0, len(all)):
            all[y] /= ok[y]

        print("%s: presnost: %.2f%%, uplnost: %.2f%%, fmira: %.2f%%, chybovost %.2f%%, accuracy: %.2f%%" % (
            "CELKOVE", all[0] * 100, all[1] * 100, all[2] * 100, all[3] * 100, all[4] * 100))

    def print_topic_stats(self):
        # Pro vsechny kategorie
        for topicKey in self.stats:
            # ziskame statistiku kategorie
            cat_stat = self.stats[topicKey]
            precision = cat_stat.precision() * 100
            recall = cat_stat.recall() * 100
            fmeasure = cat_stat.fmeasure() * 100
            error = cat_stat.error() * 100
            accuracy = cat_stat.accuracy() * 100
            print("%s: presnost: %.2f%%, uplnost: %.2f%%, fmira: %.2f%%, chybovost %.2f%%, accuracy: %.2f%%" % (
                self.translate_key(topicKey), precision, recall, fmeasure, error, accuracy))

    def translate_key(self, topicKey):
        if topicKey not in self.keys.keys():
            return "UNKNOWN"
        else:
            return self.keys[topicKey]
