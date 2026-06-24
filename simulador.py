from constantes import (
    TAMANHO_MEMORIA_VIRTUAL, TAMANHO_MEMORIA_PRINCIPAL,
    TAMANHO_PAGINA, NUM_FRAMES, NUM_PAGINAS, NUM_ACESSOS_POR_PROCESSO
)
from memoria_principal import MemoriaPrincipal
from memoria_virtual import MemoriaVirtual
from mmu import MMU
from processo_leve import ProcessoLeve

class Simulador:
    def __init__(self):
        self.mem_virtual   = MemoriaVirtual(TAMANHO_PAGINA)
        self.mem_principal = MemoriaPrincipal(NUM_FRAMES, TAMANHO_PAGINA)
        self.mmu           = MMU(self.mem_principal, self.mem_virtual)
        self.threads       = []

    def criar_processo(self, id_processo, tamanho_bytes):
        tamanho_bytes = max(1, min(tamanho_bytes, TAMANHO_MEMORIA_VIRTUAL))
        num_paginas   = self.mem_virtual.criar_processo(id_processo, tamanho_bytes)
        self.mmu.registrar_processo(id_processo, num_paginas)
        t = ProcessoLeve(id_processo, num_paginas, self.mmu, NUM_ACESSOS_POR_PROCESSO)
        self.threads.append(t)
        print(f"[Simulador] Processo {id_processo} criado | "
              f"Tamanho: {tamanho_bytes // 1024} KB | {num_paginas} página(s)")

    def executar(self):
        print("  SIMULADOR DE MEMÓRIA VIRTUAL")
        print(f"  Memória Principal : {TAMANHO_MEMORIA_PRINCIPAL//1024} KB "
              f"| {NUM_FRAMES} frames de {TAMANHO_PAGINA//1024} KB cada")
        print(f"  Memória Virtual   : {TAMANHO_MEMORIA_VIRTUAL//1024} KB "
              f"| {NUM_PAGINAS} páginas de {TAMANHO_PAGINA//1024} KB cada")
        print(f"  Substituição      : LRU (Least Recently Used)")
        print(f"  Processos leves   : {len(self.threads)} threads")

        for t in self.threads:
            t.start()

        for t in self.threads:
            t.join()

        self._exibir_estado_final()

    def _exibir_estado_final(self):
        mmu = self.mmu
        print("  ESTADO FINAL DA SIMULAÇÃO")

        print("  Memória Principal (frames):")
        for i in range(NUM_FRAMES):
            ocup = self.mem_principal.ocupacao[i]
            if ocup:
                proc, pag = ocup
                print(f"  Frame {i:2d}: Processo {proc}, Página {pag}")
            else:
                print(f"  Frame {i:2d}: [livre]")

        print("  Tabelas de Páginas (páginas em RAM):")
        for id_proc, tabela in sorted(mmu.tabelas.items()):
            em_ram = [(i, e.frame) for i, e in enumerate(tabela.entradas) if e.presente]
            print(f"  Processo {id_proc}: {len(em_ram)} página(s) em RAM → {em_ram}")

        print("  Estatísticas:")
        print(f"  Total de acessos  : {mmu.total_acessos}")
        print(f"  Faltas de página  : {mmu.total_faltas}")
        taxa = (mmu.total_faltas / mmu.total_acessos * 100) if mmu.total_acessos else 0
        print(f"  Taxa de falta     : {taxa:.1f}%")
