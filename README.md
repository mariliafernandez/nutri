# nutritionall API

API com dados de informação nutricional de diversos alimentos, extraídos das seguintes fontes brasileiras:
* TACO 
    > JSON extraído do repositório: https://github.com/marcelosanto/tabela_taco
* IBGE
    > Pesquisa de Orçamentos Familiares (2008-2009) > Tabelas de Composição Nutricional dos Alimentos Consuimdos no Brasil > tab01.zip: https://ftp.ibge.gov.br/Orcamentos_Familiares/Pesquisa_de_Orcamentos_Familiares_2008_2009/Tabelas_de_Composicao_Nutricional_dos_Alimentos_Consumidos_no_Brasil/


## Documentação
URL da API: https://www.nutritionall.xyz
Swagger: https://www.nutritionall.xyz/docs

### GET /categories - Listar categorias
**Descrição:** Retorna uma lista de categorias distintas disponíveis na base de dados.

**Response Body:**
```json
{
    "categories": ["string"]
}
```
**Exemplo curl**
```bash
curl --request GET --url https://www.nutritionall.xyz/categories
```


### POST /search - Buscar alimentos
**Descrição:** Busca alimentos na base de dados com base nos filtros fornecidos.

**Request Body:**
```json
{
  "name": "string | null",  // nome do alimento
  "order_by": "string | null",  // ordenação dos resultados, opções: "energy_kcal", "protein_g", "carbohydrate_g", "lipid_g", "fiber_g", null
  "ascending": "boolean",  // tipo de ordenação
  "max_results": "int",  // limite máximo de resultados
  "categories": "list"  // filtro de categorias
}
```

**Response body:**
```json
{
    "items": [  // informação nutricional dos alimentos selecionados
        {
            "id": "int",
            "description": "string",
            "category": "string",
            "energy_kcal": "float|null",
            "protein_g": "float|null",
            "lipid_g": "float|null",
            "carbohydrate_g": "float|null",
            "fiber_g": "float|null",
            "source": "string",
            "grams": "int"
        }
    ]
}
```
**Exemplo curl**
```bash
curl --request POST \
  --url https://www.nutritionall.xyz/search \
  --header 'Content-Type: application/json' \
  --data '{
    "name": "pão",
    "order_by":"carbohydrate_g",
    "ascending": false,
    "max_results":10,
    "categories":["Panificados"]
}'
```

### POST /calculate_macros - Calcular macros
**Descrição:** Calcula os macronutrientes de uma refeição com base nos alimentos e quantidades fornecidos.

**Request Body:**
```json
{
    "meal": [
        {
            "food_id": "int",  // id do alimento
            "grams": "int"  // quantidade em gramas do alimento
        }
    ]
}
```

**Response body:**
```json
{
    "items": [  // informação nutricional dos alimentos selecionados
        {
            "id": "int",
            "description": "string",
            "category": "string",
            "energy_kcal": "float | null",
            "protein_g": "float | null",
            "lipid_g": "float | null",
            "carbohydrate_g": "float | null",
            "fiber_g": "float | null",
            "grams": "int",
            "source": "string"
        }
    ],
    "portions": ["float"],  // porção dos alimentos selecionados (%)
    "carbohydrate_g": "float",  // quantidade total de carboidratos (em gramas)
    "protein_g": "float",  // quantidade total de proteínas (em gramas)
    "lipid_g": "float",  // quantidade total de gorduras (em gramas)
    "energy_kcal": "float", // quantidade total de energia (em kcal)
}
```

**Exemplo curl**
```bash
curl --request POST \
  --url https://www.nutritionall.xyz/calculate_macros \
  --header 'Content-Type: application/json' \
  --data '{
	"meal": [
        {
            "food_id": 6800,
            "grams": 100
        },
        {
            "food_id":7000,
            "grams":180
        }
    ]
}'
```

### POST /calculate_insulin - Calcular insulina
**Descrição:** Calcula a quantidade de insulina necessária com base na refeição e no fator de insulina/carboidrato fornecido.

**Request Body:**
```json
{
    "meal": [
        {
            "food_id": "int",  // id do alimento
            "grams": "int"  // quantidade em gramas do alimento
        }
    ],
    "factor_insulin_cho": "int",  // fator insulina/carboidrato
    "mode": "string"  // opções: "carbo" (contagem de carboidratos), "fpi" (fat-protein increment), "fpu" (fat-protein unit)
}
```

**Response Body:**
```json
{
    "items": [  // informação nutricional dos alimentos selecionados
        {
            "id": "int",
            "description": "string",
            "category": "string",
            "energy_kcal": "float | null",
            "protein_g": "float | null",
            "lipid_g": "float | null",
            "carbohydrate_g": "float | null",
            "fiber_g": "float | null",
            "grams": "int",
            "source": "string"
        }
    ],
    "insulin_needed": "float",  // quantidade de insulina necessária para a refeição
}
```

**Exemplo curl**
```bash
curl --request POST \
  --url https://www.nutritionall.xyz/calculate_insulin \
  --header 'Content-Type: application/json' \
  --data '{
        "meal": [
            {
                "food_id": 6712,
                "grams": 100
            },
            {
                "food_id":6715,
                "grams":180
            }
    ],
    "factor_insulin_cho": 10,
    "mode":"fpi"
}'
```
<!-- curl --request GET --url https://www.nutritionall.xyz/categories \