class Document:
    def __init__(self, doc, label, vector=None, rank=0.0):
        if vector is None:
            vector = []
        self.doc = doc
        self.label = label
        self.vector = vector
        self.rank = rank

    def toString(self):
        return str(self.rank)