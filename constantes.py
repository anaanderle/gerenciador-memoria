TAMANHO_MEMORIA_PRINCIPAL = 64 * 1024        # 64 KB em bytes
TAMANHO_MEMORIA_VIRTUAL   = 1 * 1024 * 1024  # 1 MB em bytes
TAMANHO_PAGINA            = 8 * 1024         # 8 KB em bytes

NUM_FRAMES  = TAMANHO_MEMORIA_PRINCIPAL // TAMANHO_PAGINA  # 8 frames
NUM_PAGINAS = TAMANHO_MEMORIA_VIRTUAL   // TAMANHO_PAGINA  # 128 páginas

NUM_ACESSOS_POR_PROCESSO = 10  # quantidade de acessos de cada thread durante a simulação
