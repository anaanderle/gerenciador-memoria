import threading

from tabela_paginas import TabelaDePaginas
from algoritmo_lru import AlgoritmoLRU

# Núcleo do simulador. Responsável por:
#   1. Manter as tabelas de páginas de todos os processos
#   2. Traduzir endereço virtual → endereço físico
#   3. Detectar page faults e coordenar o carregamento de páginas
#   4. Gerenciar substituição via LRU quando a RAM está cheia
class MMU:
    def __init__(self, memoria_principal, memoria_virtual):
        self.mem_principal  = memoria_principal
        self.mem_virtual    = memoria_virtual
        self.tabelas        = {}
        self.lru            = AlgoritmoLRU()
        self.lock           = threading.Lock()
        self.total_acessos  = 0
        self.total_faltas   = 0

    def registrar_processo(self, id_processo, num_paginas):
        self.tabelas[id_processo] = TabelaDePaginas(num_paginas)

    def exibir_resultado(self, num_frame, offset, num_pagina):
        endereco_fisico = num_frame * self.mem_principal.tamanho_frame + offset
        conteudo = self.mem_principal.ler_byte(num_frame, offset)
        self.lru.registrar_acesso(num_frame)
        print(f"  [OK] Página {num_pagina} presente no Frame {num_frame}"
              f"  | End. físico: {endereco_fisico:#08x}"
              f"  | Conteúdo: {conteudo:#04x} ({conteudo})")

    def traduzir_e_acessar(self, id_processo, endereco_virtual):
        """
          Processo → Endereço Virtual → MMU → (página presente?) →
            Sim: lê da RAM e mostra conteúdo
            Não: falta de página → carrega (frame livre ou LRU) → mostra conteúdo
        """
        with self.lock:
            self.total_acessos += 1

            num_pagina = endereco_virtual // self.mem_virtual.tamanho_pagina
            offset     = endereco_virtual %  self.mem_virtual.tamanho_pagina

            tabela = self.tabelas[id_processo]
            entrada = tabela.obter_entrada(num_pagina)

            print(f"\n[P{id_processo}] INSTRUÇÃO: ACESSO mem[{endereco_virtual:#08x}]"
                  f"  →  página {num_pagina}, offset {offset}")

            if entrada.presente:
                # CASO 1: Página já está na memória principal
                num_frame = entrada.frame
                self.exibir_resultado(num_frame, offset, num_pagina)
            else:
                # CASO 2: Page Fault — página não está na RAM
                self.total_faltas += 1
                print(f"  [!!] FALTA DE PÁGINA: página {num_pagina} não está na memória principal")

                num_frame = self._carregar_pagina(id_processo, num_pagina, tabela)
                self.exibir_resultado(num_frame, offset, num_pagina)

    def _carregar_pagina(self, id_processo, num_pagina, tabela):
        """
        Trata o carregamento após um page fault:
          a) Frame livre disponível → usa o primeiro livre
          b) Sem frame livre → substitui via LRU
        """
        dados = self.mem_virtual.obter_pagina(id_processo, num_pagina)

        frame_livre = self.mem_principal.frame_livre()

        if frame_livre != -1:
            # CASO 2a: Existe frame livre → carrega diretamente
            print(f"       Frame livre encontrado: Frame {frame_livre} → carregando página {num_pagina}")
            self.mem_principal.carregar_pagina(frame_livre, dados, id_processo, num_pagina)
            tabela.atualizar(num_pagina, frame_livre, presente=True)
            return frame_livre
        else:
            # CASO 2b: Sem frames livres → substituição LRU
            frame_vitima = self.lru.escolher_vitima()
            ocup         = self.mem_principal.ocupacao[frame_vitima]

            if ocup:
                proc_vitima, pag_vitima = ocup
                # Invalida a entrada da página substituída na tabela do processo dono
                if proc_vitima in self.tabelas:
                    self.tabelas[proc_vitima].atualizar(pag_vitima, -1, presente=False)
                print(f"       Sem frames livres | LRU escolheu Frame {frame_vitima}"
                      f" (P{proc_vitima}/pág.{pag_vitima}) → substituindo")

            self.mem_principal.carregar_pagina(frame_vitima, dados, id_processo, num_pagina)
            tabela.atualizar(num_pagina, frame_vitima, presente=True)
            return frame_vitima
