# Simulador de Gerenciamento de Memória Virtual

Simulação de um gerenciador de memória virtual com paginação, desenvolvida como Trabalho Prático II da disciplina de Análise e Aplicação de Sistemas Operacionais - Universidade do Vale do Rio dos Sinos (UNISINOS), 2026.

---

## Autor

- Ana Clara de Oliveira Anderle.

---

## Descrição Geral

O gerenciamento de memória virtual é um dos pilares dos sistemas operacionais modernos. Nele, cada processo enxerga um espaço de endereçamento próprio que é maior do que a memória física disponível. A unidade responsável por traduzir endereços virtuais em físicos é a MMU (Memory Management Unit).

Este projeto implementa, em Python, uma simulação completa do ciclo de paginação: processos geram endereços virtuais aleatórios, a MMU consulta a tabela de páginas de cada processo, detecta faltas de página, carrega páginas em frames livres ou aciona o algoritmo LRU para substituir a página menos recentemente usada.

Além da lógica de paginação, o projeto aplica conceitos fundamentais de Sistemas Operacionais, como processos leves (threads), sincronização por lock e acesso concorrente à MMU compartilhada.

---

## Estrutura do Projeto

```
gerenciador-memoria/
│
├── simulador_memoria.py       # Ponto de entrada: cria processos e inicia a simulação
│
├── simulador.py               # Orquestra threads, memória e MMU; exibe estado final
│
├── mmu.py                     # MMU: tradução de endereços, falta de página,
│                              # carregamento de páginas e lock de exclusão mútua
│
├── algoritmo_lru.py           # Algoritmo LRU com OrderedDict; escolhe a página vítima
│
├── memoria_principal.py       # Memória principal: 8 frames de 8 KB (64 KB total)
│
├── memoria_virtual.py         # Memória virtual: 128 páginas de 8 KB (1 MB total)
│
├── tabela_paginas.py          # Tabela de páginas por processo
│
├── entrada_tabela_paginas.py  # Entrada individual da tabela: número do frame e bit presente
│
├── processo_leve.py           # Thread de processo: gera acessos virtuais aleatórios
│
└── constantes.py              # Tamanhos e configurações globais da simulação
```

### Descrição detalhada de cada módulo

**`constantes.py`** — Define as constantes do sistema: `TAMANHO_MEMORIA_PRINCIPAL = 64 KB`, `TAMANHO_MEMORIA_VIRTUAL = 1 MB`, `TAMANHO_PAGINA = 8 KB`, derivando `NUM_FRAMES = 8` e `NUM_PAGINAS = 128`. Também define `NUM_ACESSOS_POR_PROCESSO`, que controla quantos endereços cada thread gera durante a simulação.

**`entrada_tabela_paginas.py`** — Implementa a classe `EntradaTabelaPaginas`, a menor unidade da tabela de páginas. Armazena o número do frame físico onde a página está carregada e o bit `presente`, que indica se a página está atualmente na memória principal.

**`tabela_paginas.py`** — Implementa `TabelaDePaginas`, uma lista de entradas indexada pelo número de página virtual. Expõe `obter_entrada(num_pagina)` para leitura e `atualizar(num_pagina, frame, presente)` para escrita, usados pela MMU após cada carga ou substituição de página.

**`memoria_virtual.py`** — Implementa `MemoriaVirtual`, que representa o espaço de 1 MB em disco. Ao criar um processo, aloca suas páginas preenchidas com bytes aleatórios, simulando o conteúdo que estaria armazenado em disco. Expõe `obter_pagina(id_processo, num_pagina)` para que a MMU copie o conteúdo para a RAM.

**`memoria_principal.py`** — Implementa `MemoriaPrincipal`, que representa os 64 KB de RAM física organizados em 8 frames de 8 KB. Mantém `frames` (dados) e `ocupacao` (qual processo/página ocupa cada frame). Expõe `frame_livre()`, `carregar_pagina()` e `ler_byte()`.

**`algoritmo_lru.py`** — Implementa `AlgoritmoLRU` usando `collections.OrderedDict` como estrutura central. Registra acessos via `registrar_acesso(num_frame)` e elege a vítima via `escolher_vitima()`. Detalhes na seção **Algoritmo de Substituição de Páginas**.

**`mmu.py`** — Implementa `MMU`, o componente central da simulação. Traduz endereços virtuais em físicos, detecta faltas de página, coordena o carregamento de páginas e protege todo o fluxo de tradução com `threading.Lock`. Detalhes na seção **Simulação do Sistema Operacional**.

**`processo_leve.py`** — Implementa `ProcessoLeve`, subclasse de `threading.Thread`. Cada instância representa um processo que gera `NUM_ACESSOS_POR_PROCESSO` endereços virtuais aleatórios dentro do seu espaço de endereçamento e os envia à MMU.

**`simulador.py`** — Implementa `Simulador`, que instancia a memória virtual, a memória principal e a MMU, cria os processos leves, inicia todas as threads e exibe o estado final (frames ocupados, tabelas de páginas e estatísticas de falta de página).

**`simulador_memoria.py`** — Ponto de entrada do programa. Define os processos com seus tamanhos, chama `sim.criar_processo()` para cada um e dispara `sim.executar()`.

---

## Como Compilar

O projeto utiliza apenas a biblioteca padrão do Python. Não há etapa de compilação nem instalação de dependências externas.

**Pré-requisito:** Python 3.8 ou superior.

---

## Como Executar

### Execução padrão

```bash
python simulador_memoria.py
```

### Saída esperada

A execução produz quatro seções diferentes no terminal:

**1. Criação dos processos**

```
[Simulador] Processo 1 criado | Tamanho: 20 KB | 3 página(s)
[Simulador] Processo 2 criado | Tamanho: 36 KB | 5 página(s)
[Simulador] Processo 3 criado | Tamanho: 10 KB | 2 página(s)
```

**2. Cabeçalho da simulação**

```
  SIMULADOR DE MEMÓRIA VIRTUAL
  Memória Principal : 64 KB | 8 frames de 8 KB cada
  Memória Virtual   : 1024 KB | 128 páginas de 8 KB cada
  Substituição      : LRU (Least Recently Used)
  Processos leves   : 3 threads
```

**3. Instruções das threads (intercaladas)**

```
[P1] INSTRUÇÃO: ACESSO mem[0x000d2a]  →  página 0, offset 3370
  [!!] FALTA DE PÁGINA: página 0 não está na memória principal
       Frame livre encontrado: Frame 0 → carregando página 0
  [OK] Página 0 presente no Frame 0  | End. físico: 0x000d2a  | Conteúdo: 0x69 (105)

[P1] INSTRUÇÃO: ACESSO mem[0x00372b]  →  página 1, offset 5931
  [!!] FALTA DE PÁGINA: página 1 não está na memória principal
       Sem frames livres | LRU escolheu Frame 1 (P2/pág.0) → substituindo
  [OK] Página 1 presente no Frame 1  | End. físico: 0x00372b  | Conteúdo: 0x26 (38)
```

**4. Estado final e estatísticas**

```
  ESTADO FINAL DA SIMULAÇÃO
  Memória Principal (frames):
  Frame  0: Processo 1, Página 0
  Frame  1: Processo 1, Página 1
  Frame  2: Processo 3, Página 0
  Frame  3: Processo 1, Página 2
  Frame  4: Processo 2, Página 1
  Frame  5: Processo 2, Página 2
  Frame  6: Processo 3, Página 1
  Frame  7: Processo 2, Página 4
  Tabelas de Páginas (páginas em RAM):
  Processo 1: 3 página(s) em RAM → [(0, 0), (1, 1), (2, 3)]
  Processo 2: 3 página(s) em RAM → [(1, 4), (2, 5), (4, 7)]
  Processo 3: 2 página(s) em RAM → [(0, 2), (1, 6)]
  Estatísticas:
  Total de acessos  : 30
  Faltas de página  : 11
  Taxa de falta     : 36.7%
```

---

## Parâmetros de Entrada

Os parâmetros são configurados diretamente no código-fonte.

### Constantes do sistema (`constantes.py`)

| Parâmetro | Valor padrão | Descrição |
|---|---|---|
| `TAMANHO_MEMORIA_PRINCIPAL` | 64 KB | Tamanho da RAM física |
| `TAMANHO_MEMORIA_VIRTUAL` | 1 MB | Tamanho do espaço virtual total |
| `TAMANHO_PAGINA` | 8 KB | Tamanho de cada página e frame |
| `NUM_FRAMES` | 8 | Número de frames na memória principal |
| `NUM_PAGINAS` | 128 | Número de páginas na memória virtual |
| `NUM_ACESSOS_POR_PROCESSO` | 10 | Quantidade de acessos gerados por cada thread |

### Processos criados (`simulador_memoria.py`)

| Processo | Tamanho | Páginas virtuais |
|---|---|---|
| Processo 1 | 20 KB | 3 páginas |
| Processo 2 | 36 KB | 5 páginas |
| Processo 3 | 10 KB | 2 páginas |

O tamanho de cada processo pode variar entre 1 byte e 1 MB. O número de páginas é calculado automaticamente por `MemoriaVirtual.criar_processo()`.

---

## Algoritmo de Substituição de Páginas

### Visão geral

Quando todos os 8 frames estão ocupados e uma nova página precisa ser carregada, a MMU aciona o `AlgoritmoLRU`, que elege como vítima o frame menos recentemente acessado. Após a escolha, a entrada da página substituída é invalidada na tabela de páginas do processo dono, e a nova página é carregada no frame liberado.

### Estrutura: `collections.OrderedDict`

O `AlgoritmoLRU` usa um `OrderedDict` como fila de prioridade. A chave é o número do frame; a posição no dicionário representa a ordem de uso (início = menos recente, fim = mais recente).

**Por que `OrderedDict` e não uma lista comum?** Um `OrderedDict` permite mover um elemento existente para o fim com `move_to_end()` em O(1), sem percorrer a estrutura. Uma lista exigiria `remove()` + `append()`, totalizando O(n) por acesso.

### Fluxo de substituição

Quando `frame_livre()` retorna `-1` (sem frames disponíveis):

1. `lru.escolher_vitima()` retorna o frame menos recentemente usado via `popitem(last=False)`.
2. A MMU consulta `mem_principal.ocupacao[frame_vitima]` para identificar qual processo e página ocupam o frame.
3. A entrada da página vítima é invalidada: `tabela.atualizar(pag_vitima, -1, presente=False)`.
4. A nova página é carregada no frame liberado e a tabela do processo requisitante é atualizada.

---

## Simulação do Sistema Operacional

### Processos Leves (Threads)

O sistema opera com tantas threads quanto processos criados. Cada `ProcessoLeve` é uma `threading.Thread` que roda de forma concorrente, gerando endereços virtuais aleatórios dentro do seu espaço de endereçamento e chamando `mmu.traduzir_e_acessar()`.

**Thread de processo:**
- Criada via `threading.Thread` (subclasse `ProcessoLeve`).
- Responsabilidade: gerar `NUM_ACESSOS_POR_PROCESSO` endereços aleatórios e enviá-los à MMU.
- Marcada como `daemon=True`, garantindo encerramento automático se a thread principal falhar.
- Sincronização: aguarda `t.join()` no `Simulador.executar()` antes de exibir o estado final.

### Exclusão Mútua com `threading.Lock` na MMU

Como múltiplas threads acessam a MMU simultaneamente, toda a operação de tradução, desde a consulta à tabela de páginas até a eventual carga de uma nova página, é protegida por `self.lock` (instância de `threading.Lock`).

**Por que o lock abrange todo o bloco de tradução e não só a escrita?** A operação de tradução não é atômica: ela lê o bit `presente` da tabela, e com base nessa leitura decide se carrega a página. Se duas threads lessem `presente = False` para a mesma página antes de qualquer uma carregar, ambas tentariam carregar a mesma página em frames diferentes, corrompendo a tabela de páginas. O lock garante que apenas uma thread por vez executa o ciclo completo.

### Concorrência

**Como múltiplas threads operam:** as threads são iniciadas todas ao mesmo tempo com `t.start()`. Cada uma gera acessos com um intervalo de `0,02 s` entre eles (`time.sleep(0.02)`), simulando a cadência de instruções de um processo real.

**Como condições de corrida foram evitadas:**

1. **Na tabela de páginas e nos frames:** o `with self.lock` na MMU serializa toda tradução, impedindo que duas threads modifiquem simultaneamente a tabela de páginas ou o vetor de frames.
2. **Nos contadores de estatísticas:** `total_acessos` e `total_faltas` também são incrementados dentro do lock, garantindo consistência nos totais exibidos ao final.
3. **No estado do LRU:** como `registrar_acesso` e `escolher_vitima` são chamados exclusivamente de dentro do lock da MMU, o `OrderedDict` nunca é acessado concorrentemente.

---

## Principais Decisões de Projeto

### 1. Linguagem: Python 3.8+

Python fornece `threading.Thread`, `threading.Lock` e `collections.OrderedDict` na biblioteca padrão, com uma sintaxe orientada a objetos que permite modelar diretamente os componentes do sistema (MMU, tabela de páginas, frames).

---

### 2. Lock cobrindo todo o ciclo de tradução

Proteger apenas a escrita na tabela de páginas seria insuficiente: a decisão de carregar uma página depende de uma leitura prévia do bit `presente`. O lock abrange leitura + decisão + escrita como uma transação atômica.

---

### 3. `OrderedDict` no LRU

A escolha do `OrderedDict` garante O(1) tanto para registrar acessos (`move_to_end`) quanto para eleger a vítima (`popitem(last=False)`), sem estruturas auxiliares. Alternativas como `list` ou `deque` exigiriam busca linear para remover e reinserir um frame ao ser acessado novamente.

---

### 4. Separação entre memória virtual e principal

A `MemoriaVirtual` representa o disco: armazena os dados de todas as páginas de todos os processos, mas não os mantém em RAM. A `MemoriaPrincipal` representa a RAM: só conhece os dados que foram explicitamente carregados. Essa separação torna o fluxo de falta de página explícito e verificável, a carga sempre passa por `mem_virtual.obter_pagina()` → `mem_principal.carregar_pagina()`.

---

## Resultados Obtidos

A simulação com 3 processos (20 KB, 36 KB e 10 KB) e 10 acessos por thread produziu os seguintes resultados:

**Acessos e faltas de página:**
Com 30 acessos no total, 11 resultaram em falta de página — uma taxa de 36,7%. As primeiras faltas ocorrem obrigatoriamente (cold start: nenhuma página está carregada inicialmente). As faltas subsequentes ocorrem quando o LRU precisa substituir uma página para acomodar outra.

**Estado final da memória:**
Todos os 8 frames estavam ocupados ao final da simulação. O Processo 1 manteve suas 3 páginas em RAM; os Processos 2 e 3 tiveram páginas substituídas ao longo da execução, encerrando com 3 e 2 páginas em RAM, respectivamente.

**Eficiência do LRU:**
O algoritmo substituiu corretamente as páginas menos recentemente usadas, como evidenciado pelas mensagens `LRU escolheu Frame X (PY/pág.Z) → substituindo`, que aparecem apenas após todos os frames estarem ocupados.
