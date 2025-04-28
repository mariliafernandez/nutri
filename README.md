# NutritionALL API

A **NutritionALL API** facilita o acesso a informações nutricionais de alimentos e permite a integração de dados nutricionais em sua aplicação de forma simples e eficiente.

## 📚 Funcionalidades

- **Consulta de informações nutricionais** de bases brasileiras consolidadas:
  - TACO (Tabela Brasileira de Composição de Alimentos)
  - IBGE (Instituto Brasileiro de Geografia e Estatística)
- **Busca customizada** de alimentos por nome, categoria, nutrientes, e ordenação personalizada
- **Análise de relações** entre nutrientes (ex.: mais proteína por caloria, mais fibras por carboidrato)
- **Cálculo de macronutrientes** totais de uma refeição
- **Cálculo de dose de insulina** baseada nos carboidratos ingeridos

---

## 📄 Documentação

Link para a documentação: https://www.nutritionall.xyz/api/docs 

### Endpoints 

| Método | Rota                      | Descrição |
|:------:|:---------------------------|:----------|
| `GET`  | `/api/health`               | Verifica a saúde do serviço |
| `GET`  | `/api/categories`           | Retorna categorias de alimentos disponíveis |
| `POST` | `/api/search`               | Realiza busca de alimentos por critérios personalizados |
| `POST` | `/api/relation`             | Lista alimentos com base em relações nutricionais |
| `POST` | `/api/calculate`     | Calcula macronutrientes de uma refeição e insulina necessária |
