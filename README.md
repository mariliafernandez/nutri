# nutri

- API com dados de informação nutricional de diversos alimentos, integrados de fontes de fontes brasileiras confiáveis:
    * Tabela TACO (JSON extraído do repositório: https://github.com/marcelosanto/tabela_taco)
    * IBGE 

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
3. Download do modelo de NLP
    ```bash
    python -m spacy download pt_core_news_lg
    ```