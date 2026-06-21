from entrada_tabela_paginas import EntradaTabelaPaginas

# Mapeia páginas virtuais para frames físicos
class TabelaDePaginas:
    def __init__(self, num_paginas):
        self.entradas = [EntradaTabelaPaginas() for _ in range(num_paginas)]

    def obter_entrada(self, num_pagina):
        return self.entradas[num_pagina]

    def atualizar(self, num_pagina, frame, presente=True):
        self.entradas[num_pagina].frame    = frame
        self.entradas[num_pagina].presente = presente
