import random
from simulador import Simulador

if __name__ == "__main__":
    random.seed(42)

    sim = Simulador()

    sim.criar_processo(id_processo=1, tamanho_bytes=20 * 1024)  # 20 KB → 3 páginas
    sim.criar_processo(id_processo=2, tamanho_bytes=36 * 1024)  # 36 KB → 5 páginas
    sim.criar_processo(id_processo=3, tamanho_bytes=10 * 1024)  # 10 KB → 2 páginas

    sim.executar()
