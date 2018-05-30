

# Statistika jedne kategorie
class Statistic:

    # True positive
    tp = 0

    # False positive
    fp = 0

    # True negative
    tn = 0

    # False negative
    fn = 0

    def __init__(self, name):
        self.name = name
        pass

    def accuracy(self):
        if (self.tp + self.tn + self.fp + self.fn) == 0:
            return float('nan')
        return (self.tp + self.tn) / (self.tp + self.tn + self.fp + self.fn)

    def error(self):
        if (self.tp + self.tn + self.fp + self.fn) == 0:
            return float('nan')
        return (self.fp + self.fn) / (self.tp + self.tn + self.fp + self.fn);

    def precision(self):
        if (self.tp + self.fp) == 0:
            return float('nan')
        return (self.tp) / (self.tp + self.fp);

    def recall(self):
        if (self.tp + self.fn) == 0:
            return float('nan')
        return (self.tp) / (self.tp + self.fn);

    def fmeasure(self):
        precision = self.precision()
        recall = self.recall()
        if (precision + recall) == 0:
            return float('nan')
        return (2 * precision * recall) / (precision + recall);