import random

# Simula o disco / espaço de endereçamento virtual de 1 MB.
class MemoriaVirtual:
    def __init__(self, tamanho_pagina):
        self.tamanho_pagina = tamanho_pagina
        self._paginas = {}

    def criar_processo(self, id_processo, tamanho_bytes):
        # (simulam o conteúdo real que estaria em disco)
        num_paginas = (tamanho_bytes + self.tamanho_pagina - 1) // self.tamanho_pagina
        for p in range(num_paginas):
            self._paginas[(id_processo, p)] = [
                random.randint(0, 255) for _ in range(self.tamanho_pagina)
            ]
        return num_paginas

    def obter_pagina(self, id_processo, num_pagina):
        return self._paginas.get((id_processo, num_pagina))
