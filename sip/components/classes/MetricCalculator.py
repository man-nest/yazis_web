class MetricCalculator:
    def __init__(self, a:int = 20, b:int = 1, c:int = 2, d:int = 10):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

        self.recall = self.calculateRecall()
        self.precision = self.calculatePrecision()
        self.accuracy = self.calculateAccuracy()
        self.error = self.calculateError()
        self.f_measure = self.calculateFMeasure()

    def calculateRecall(self):
        return self.a / (self.a + self.c)

    def calculatePrecision(self):
        return self.a / (self.a + self.b)

    def calculateAccuracy(self):
        return (self.a + self.d) / (self.a + self.b + self.c + self.d)

    def calculateError(self):
        return (self.b + self.c) / (self.a + self.b + self.c + self.d)

    def calculateFMeasure(self):
        if self.precision == 0 or self.recall == 0:
            return 0
        elif self.precision == self.recall:
            return self.precision
        else:
            return 2 / (self.precision ** -1 + self.recall ** -1)
