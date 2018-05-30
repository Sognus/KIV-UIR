from BagOfWords import BagOfWords
from NGram import NGram
from KNN import KNN
from TFID import TFID
from Centroid import Centroid
from Statistics import Statistics
import time
import importlib
import sys
import os.path


class Main:

    def __init__(self):
        self.version = "1.0.0"
        pass

    def print_usage(self):
        print("priklad zadani: Main.py tweets.csv bow knn")

    def get_vector_algoritm(self, name, filename):
        if name == 'bow':
            return BagOfWords(filename)
        if name == 'ngram':
            return NGram(filename)
        if name == 'tfid':
            return TFID(filename)
        # Unsupported or non-existing vectorization algoritm
        return None

    def get_detection_algoritm(self, name, tweets, vectors):
        if name == "knn":
            return KNN(tweets, vectors)
        if name == "centroid":
            return Centroid(tweets, vectors)
        # Unsupported or non existing detection algoritm
        return None

    def print_vector_algoritms(self):
        print("Podporovane vektorizacni algoritmy")
        print("bow")
        print("ngram")
        print("tfid")

    def print_detection_algoritms(self):
        print("Podporovane detekcni algoritmy: ")
        print("knn")
        print("centroid")

    def run(self):
        # Fix Linux retardness
        importlib.reload(sys)

        # Check for program arguments
        if len(sys.argv) < 4:
            print("Tento program vyzaduje minimalne tri parametry")
            self.print_usage()
            exit(-1)

        # Validate File
        filename = sys.argv[1]
        fileCheck = os.path.isfile(filename)
        if not fileCheck:
            print("Vami zadany parametr vstupniho souboru je nespravny, nejspis neexistuje nebo k nemu nemate prava!")
            exit(-2)

        # Validate vectorization algoritm
        vector_algoritm = sys.argv[2]
        vectorization = self.get_vector_algoritm(vector_algoritm, filename)
        if vectorization is None:
            print("Vami zadny parametr algoritmu vytvoreni vektoru neexistuje!")
            self.print_vector_algoritms()
            exit(-3)

        # Start time measure
        start_time = time.time()

        # Load input CSV and create vectors
        print("STARTING VECTORIZATION ALGORITM")
        vectorization.load_csv()
        vectorization.create_vector()
        print("VECTORIZATION ALGORITM COMPLETED\n")

        # Validate detection
        detect_algoritm = sys.argv[3]
        detection = self.get_detection_algoritm(detect_algoritm, vectorization.tweets, vectorization.vectors)
        if detection is None:
            print("Vami zadany parametr detekcniho algoritmu neexistuje!")
            self.print_detection_algoritms()
            exit(-4)

        # Check for unexpected error - are they unexpected when I am expecting unexpected? No I guess
        try:
            print("STARTING DETECTION ALGORITM")
            detection.start()
            print("DETECTION ALGORITM COMPLETED\n")
            print("PROGRAM COMPLETED IN {:.2f} SECONDS\n".format(time.time() - start_time))

            print("STARTING STATISTICS MODULE")
            stat = Statistics("tweets.csv", "detected.csv", detection.training_count)
            # stat.print_topic_stats()
            stat.print_complete_stat()
            print("STATISTICS MODULE COMPLETED\n")
        except:
            print("Pri zpracovani programu doslo k chybe!")
            exit(-5)


def main():
    main = Main()
    main.run()

if __name__ == "__main__":
    main()
