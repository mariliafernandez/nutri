# nutri

Busca de informação nutricional de alimentos na tabela TACO utilizando embeddings e regex

JSON `tabela_alimentos.json` extraído do repositório: https://github.com/marcelosanto/tabela_taco

## Dependências 
As dependências desse projeto estão listadas nos arquivos `Pipfile` e `Pipfile.lock`

## Execução
1. Rodar o banco vetorial
    ```shell
    chroma run
    ```
2. Rodar o código principal
    ```bash
    python main.py
    ```
