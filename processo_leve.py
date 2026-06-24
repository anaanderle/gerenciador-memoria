import threading
import random
import time

from constantes import TAMANHO_PAGINA

class ProcessoLeve(threading.Thread):
    def __init__(self, id_processo, num_paginas, mmu, num_acessos):
        super().__init__(name=f"Processo-{id_processo}", daemon=True)
        self.id_processo   = id_processo
        self.espaco_virtual = num_paginas * TAMANHO_PAGINA
        self.mmu           = mmu
        self.num_acessos   = num_acessos

    def run(self):
        print(f"[P{self.id_processo}] Thread iniciada"
              f"Espaço virtual: {self.espaco_virtual // 1024} KB "
              f"({self.espaco_virtual // TAMANHO_PAGINA} página(s))")
        for _ in range(self.num_acessos):
            # Gera um endereço virtual aleatório dentro do espaço do processo
            endereco = random.randint(0, self.espaco_virtual - 1)
            self.mmu.traduzir_e_acessar(self.id_processo, endereco)
            time.sleep(0.02)
        print(f"\n[P{self.id_processo}] Thread finalizada ({self.num_acessos} acessos realizados)")
