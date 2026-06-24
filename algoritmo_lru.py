from collections import OrderedDict

class AlgoritmoLRU:
    def __init__(self):
        self.ordem_uso = OrderedDict()

    def registrar_acesso(self, num_frame):
        if num_frame in self.ordem_uso:
            return self.ordem_uso.move_to_end(num_frame)

        self.ordem_uso[num_frame] = True

    def escolher_vitima(self):
        if not self.ordem_uso:
            return 0
        vitima, _ = self.ordem_uso.popitem(last=False)
        return vitima

    def remover(self, num_frame):
        self.ordem_uso.pop(num_frame, None)
