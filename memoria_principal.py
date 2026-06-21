# Representa os 8 frames físicos de 8 KB cada (total 64 KB).
class MemoriaPrincipal:
    def __init__(self, num_frames, tamanho_frame):
        self.num_frames    = num_frames
        self.tamanho_frame = tamanho_frame
        self.frames   = [None] * num_frames
        self.ocupacao = [None] * num_frames

    def frame_livre(self):
        for i, f in enumerate(self.frames):
            if f is None:
                return i
        return -1

    def carregar_pagina(self, num_frame, dados, id_processo, num_pagina):
        self.frames[num_frame]   = dados[:]
        self.ocupacao[num_frame] = (id_processo, num_pagina)

    def ler_byte(self, num_frame, offset):
        return self.frames[num_frame][offset]

    def liberar_frame(self, num_frame):
        self.frames[num_frame]   = None
        self.ocupacao[num_frame] = None
