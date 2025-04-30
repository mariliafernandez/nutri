# NutritionALL API

A **NutritionALL API** facilita o acesso a informações nutricionais de alimentos e permite a integração de dados nutricionais em sua aplicação de forma simples e eficiente.

## 📚 Funcionalidades

- **Consulta de informações nutricionais** de bases brasileiras consolidadas:
  - TACO (Tabela Brasileira de Composição de Alimentos)
  - IBGE (Instituto Brasileiro de Geografia e Estatística)
- **Busca customizada** de alimentos por nome, categoria, nutrientes, e ordenação personalizada
- **Análise de relações** entre nutrientes (ex.: mais proteína por caloria, mais fibras por carboidrato)
- **Cálculo de macronutrientes** totais de uma refeição
- **Cálculo de dose de insulina** necessária para uma refeição (para insulino-dependentes)

---

## 📄 Documentação

Link para a documentação: https://www.nutritionall.xyz/api/docs 

## 🔗 Endpoints

| Método | Rota                      | Descrição |
|:------:|:---------------------------|:----------|
| `GET`  | `/api/health`               | Verifica a disponibilidade do serviço |
| `GET`  | `/api/categories`           | Retorna categorias de alimentos disponíveis |
| `POST` | `/api/search`               | Realiza busca de alimentos por critérios personalizados |
| `POST` | `/api/relation`             | Lista alimentos com base em relações nutricionais |
| `POST` | `/api/calculate`     | Calcula macronutrientes de uma refeição e insulina necessária |



### 🩺 `GET /api/health` - Health Check

Verifica a disponibilidade do serviço e a conexão com o banco de dados


**Resposta:**
| Campo      | Tipo     | Obrigatório | Descrição |
|------------|----------|-------------|-----------|
| `status`   | string   | Sim         | Status do serviço: `"ok"` ou `"nok"`. |
| `db_error` | string | Não     | Detalhes do erro de conexão com o banco (se houver) |


### 📂 `GET /api/categories` - Categorias Disponíveis

Retorna todas as categorias de alimentos presentes na base de dados


**Resposta:**
| Campo         | Tipo      | Obrigatório | Descrição |
|---------------|-----------|-------------|-----------|
| `categories`  | string[ ]  | Sim         | Nomes das categorias alimentares |


### 🔍 `POST /api/search` - Consulta de Alimentos

Consulta alimentos com base em nome, ordenação e filtros opcionais



**Requisição:**

| Campo         | Tipo               | Obrigatório | Descrição |
|---------------|--------------------|-------------|-----------|
| `name`        | string      | Não         | Termo de busca no nome do alimento |
| `order_by`    | string             | Não         | Campo para ordenação (`energy_kcal`, `protein_g`, `lipid_g`, `carbohydrate_g`, `fiber_g`) |
| `ascending`   | boolean            | Não         | Ordenar de forma crescente (default: `false`) |
| `max_results` | int     | Não         | Número máximo de resultados (default: `null`) |
| `categories`  | string[ ]           | Não         | Lista de categorias a filtrar (default: `[] - todas as categorias`) |

**Exemplo:**
Traz os 10 primeiros resultados de `batata` com a maior quantidade de energia (kcal) 
```json
{
  "name": "batata",
  "order_by": "energy_kcal",
  "ascending": false,
  "max_results": 10,
}
```

**Resposta:**
| Campo            | Tipo         | Obrigatório | Descrição |
|------------------|--------------|-------------|-----------|
| `id`             | int      | Sim         | ID do alimento |
| `description`    | string       | Sim         | Nome do alimento |
| `category`       | string       | Sim         | Categoria alimentar |
| `energy_kcal`    | float       | Não         | Energia em kcal por 100g |
| `protein_g`      | float       | Não         | Proteína em gramas por 100g |
| `lipid_g`        | float       | Não         | Lipídios em gramas por 100g |
| `carbohydrate_g` | float       | Não         | Carboidratos em gramas por 100g |
| `fiber_g`        | float       | Não         | Fibras em gramas por 100g |
| `source`         | string       | Sim         | Fonte dos dados: `"taco"` ou `"ibge"` |

### ⚖️ `POST /api/relation` -  Consulta por Relações Nutricionais

Retorna alimentos com base em relações entre dois nutrientes.

**Requisição:**
| Campo         | Tipo      | Obrigatório | Descrição |
|---------------|-----------|-------------|-----------|
| `col1`        | string    | Sim         | Numerador da relação, opções: `energy_kcal`, `protein_g`, `lipid_g`, `carbohydrate_g`, `fiber_g` |
| `col2`        | string    | Sim         | Denominador de relação, opções: `energy_kcal`, `protein_g`, `lipid_g`, `carbohydrate_g`, `fiber_g` |
| `ascending`   | boolean   | Não         | Ordenar de forma crescente (default: `false - descrescente`) |
| `max_results` | int    | Não         | Limite de resultados, (default: `null - todos os resultados`) |
| `categories`  | string[ ]  | Não         | Filtro por categorias, (default: `[] - todas as categorias`) |

**Exemplo:**

Consulta os top 3 alimentos da categoria `Farinhas, féculas e massas` com a maior quantidade de fibras por carboidrato:
```json
{
  "col1": "fiber_g",
  "col2": "carbohydrate_g",
  "max_results": 3,
  "categories": ["Farinhas, féculas e massas"]
}
```

**Resposta:**
| Campo               | Tipo          | Obrigatório | Descrição |
|---------------------|---------------|-------------|-----------|
| `id`             | int      | Sim         | ID do alimento |
| `description`    | string       | Sim         | Nome do alimento |
| `category`       | string       | Sim         | Categoria alimentar |
| `energy_kcal`    | float       | Não         | Energia em kcal por 100g |
| `protein_g`      | float       | Não         | Proteína em gramas por 100g |
| `lipid_g`        | float       | Não         | Lipídios em gramas por 100g |
| `carbohydrate_g` | float       | Não         | Carboidratos em gramas por 100g |
| `fiber_g`        | float       | Não         | Fibras em gramas por 100g |
| `source`         | string       | Sim         | Fonte dos dados: `"taco"` ou `"ibge"` |
| `relation_value`        | float        | Sim         | Valor da razão entre `col1` e `col2` |
| `relation_description`  | string     | Sim         | Descrição da relação (ex: `"fiber_g / carbohydrate_g"`) |

### 🍽️ `POST /api/calculate` - Cálculo de Macronutrientes e Insulina

Calcula o total de macronutrientes e calorias com base em uma refeição e, opcionalmente, a insulina necessária.
O cálculo de insulina possui três opções: 

* `carbo`: Considera apenas os carboidratos da refeição 
* `fpi` (Fat-Protein Increment): Considera os carboidratos da refeição mais um incremento de 30% 
* `fpu` (Fat-Protein Unit): Considera os carboidratos da refeição mais o equivalentes de gorduras e proteínas 

O cálculo considera a **quantidade total** de insulina necessária, pode ser necessário dividir em duas doses ao considerar a ação de proteínas e gorduras.


**Requisição:**
| Campo                | Tipo         | Obrigatório | Descrição |
|----------------------|--------------|-------------|-----------|
| `meal`               | `FoodPortion[]` | Sim      | Lista de alimentos com quantidade em gramas |
| `factor_insulin_cho` | int      | Não         | Fator insulina/carboidrato (opcional) |
| `mode`               | string       | Não         | Modo de cálculo: `"carbo"` (default), `"fpi"`, `"fpu"` |

**FoodPortion:**
| Campo    | Tipo    | Obrigatório | Descrição |
|----------|---------|-------------|-----------|
| `food_id`| int | Sim         | ID do alimento |
| `grams`  | int | Sim         | Quantidade em gramas |

**Exemplo:**
```json
{
  "meal": [
    { "food_id": 9005, "grams": 100 },
    { "food_id": 6801, "grams": 50 }
  ],
  "factor_insulin_cho": 10,
  "mode": "carbo"
}
```

**Resposta:**
| Campo            | Tipo    | Obrigatório     | Descrição |
|------------------|---------|-----------------|-----------|
| `energy_kcal`    | float   | Sim    | Energia total (em kcal) |
| `carbohydrate_g` | float   | Sim    | Carboidratos totais (em gramas) |
| `protein_g`      | float   | Sim    | Proteínas totais (em gramas)|
| `lipid_g`        | float   | Sim    | Gorduras totais (em gramas) |
| `fiber_g`        | float   | Sim    | Fibras totais (em gramas) |
| `insulin_needed` | float   | Não    | Quantidade estimada de insulina (se informado `factor_insulin_cho`) |

