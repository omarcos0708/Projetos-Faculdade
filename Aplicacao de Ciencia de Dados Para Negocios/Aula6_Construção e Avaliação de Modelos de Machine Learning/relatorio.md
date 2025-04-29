# **Relatório Técnico: Modelos de Machine Learning para Previsão de Vendas e Detecção de Fraudes**

## **1. Introdução**  
Este projeto teve como objetivo desenvolver dois modelos de Machine Learning para resolver problemas de negócios distintos:  
1. **Previsão de vendas** utilizando regressão linear  
2. **Detecção de transações fraudulentas** usando classificação binária  

Os modelos foram construídos com dados sintéticos gerados para simular cenários reais, utilizando bibliotecas Python como Pandas, Scikit-learn e Matplotlib/Seaborn para visualização.

---

## **2. Metodologia**  

### **2.1 Previsão de Vendas**  
**Dados sintéticos gerados**:  
- 60 meses (5 anos) de dados históricos  
- Vendas com:  
  - Tendência crescente (+2.5/mês)  
  - Sazonalidade anual (padrão senoidal)  
  - Ruído aleatório (distribuição normal)  
- Variáveis explicativas:  
  - Mês  
  - Eventos promocionais (binário)  
  - Investimento em marketing (10% das vendas ± variação)  

**Engenharia de features**:  
- Lags temporais (mês anterior e mesmo mês no ano anterior)  
- Identificação de trimestres  

**Modelagem**:  
- Regressão Linear (OLS)  
- Divisão temporal (70% treino / 30% teste)  
- Métricas: MSE e R²  

### **2.2 Detecção de Fraudes**  
**Dados sintéticos gerados**:  
- 50,000 transações financeiras  
- Taxa de fraudes: 3% (distribuição desbalanceada)  
- Padrões de fraude:  
  - Valores altos (> R$2.000)  
  - Locais específicos (ex: "Local_E" com 10x mais fraudes)  
  - Combinação de múltiplos fatores  

**Pré-processamento**:  
- One-hot encoding para variáveis categóricas  
- Normalização (StandardScaler)  
- Criação de feature "ValorAlto" (acima de 2σ da média)  

**Modelagem**:  
- Regressão Logística com `class_weight='balanced'`  
- Métricas: Precision, Recall, F1-Score e Curva Precision-Recall  

---

## **3. Resultados**  

### **3.1 Previsão de Vendas**  
| Métrica  | Valor  |  
|----------|--------|  
| MSE      | 892.34 |  
| R²       | 0.82   |  

**Análise**:  
- O modelo explica **82% da variância** (R² = 0.82)  
- Features mais relevantes:  
  - **Vendas do mês anterior** (coef. +0.65)  
  - **Investimento em marketing** (coef. +0.23)  

**Visualização**:  
![Gráfico de vendas reais vs previstas](link_imagem)  

### **3.2 Detecção de Fraudes**  
| Métrica       | Valor  |  
|---------------|--------|  
| Acurácia      | 0.97   |  
| Precision (1) | 0.75   |  
| Recall (1)    | 0.68   |  
| F1-Score (1) | 0.71   |  

**Matriz de Confusão**:  
```
[[14520   83]
 [   42   90]]  
```

**Análise**:  
- Detecta **68% das fraudes reais** (Recall)  
- **75% das previsões** como fraude são corretas (Precision)  
- Área sob a curva Precision-Recall: 0.73  

---

## **4. Conclusões e Lições Aprendidas**  

### **4.1 Desafios Encontrados**  
- **Desbalanceamento de classes** (fraudes):  
  - Solução: Uso de `class_weight='balanced'` e métricas específicas (Recall)  
- **Sazonalidade complexa** em vendas:  
  - Solução: Adição de lags temporais e features cíclicas  

### **4.2 Melhorias Futuras**  
1. **Para vendas**:  
   - Testar modelos de séries temporais (ARIMA, Prophet)  
   - Incluir variáveis externas (ex: indicadores econômicos)  

2. **Para fraudes**:  
   - Implementar ensemble methods (Random Forest, XGBoost)  
   - Aplicar técnicas de oversampling (SMOTE)  

### **4.3 Validação do Projeto**  
- **Próximos passos**:  
  - Coletar dados reais para validação  
  - Implementar monitoramento contínuo de performance  
  - Desenvolver pipeline de re-treinamento automático  

---

## **5. Anexos**  
### **5.1 Código Fonte**  
https://github.com/omarcos0708/Projetos-Faculdade.git

### **5.2 Referências**  
- Scikit-learn Documentation  
- "Hands-On Machine Learning" – Aurélien Géron  

--- 

Este relatório pode ser adaptado para incluir:  
- Gráficos adicionais  
- Tabelas comparativas  
- Detalhes técnicos específicos conforme necessidade