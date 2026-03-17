# 🚀 MBRAS Emotion — Sistema de Análise de Sentimentos

Este projeto é uma API de alta performance desenvolvida para o desafio técnico da **MBRAS**. O sistema realiza a análise de sentimentos em tempo real de feeds de mensagens, integrando regras de negócio específicas e detecção de influência.

## 📌 O que este projeto faz?
O objetivo é processar mensagens de redes sociais e extrair inteligência:
1.  **Análise de Sentimento**: Identifica se a mensagem é Positiva, Negativa ou Neutra.
2.  **Influência**: Calcula o número de seguidores de um usuário de forma fixa (determinística).
3.  **Regras de Negócio**: Aplica bônus de pontuação para funcionários da empresa e lida com negações complexas no texto.

## 🛠️ Tecnologias Utilizadas
- **Python 3.12**
- **FastAPI**: Framework moderno para APIs rápidas.
- **Pydantic**: Para validação rigorosa dos dados de entrada.
- **Pytest**: Para garantir que a lógica nunca quebre (Testes Automatizados).
- **GitHub Actions**: Automação que roda os testes a cada "Push".

## ⚙️ Explicação da Lógica Técnica

### Análise de Sentimento (`sentiment_analyzer.py`)
- **Negação Dupla**: O sistema entende que "não não gostei" é algo positivo (as negações se anulam).
- **Intensificadores**: Palavras como "muito" ou "extremamente" aumentam o peso do sentimento em 50%.
- **Normalização**: O código ignora acentos (ex: "Ótimo" e "otimo" são a mesma coisa).

### Influência Determinística
Em vez de usar números aleatórios, usamos um **Hash SHA-256** do ID do usuário. Isso garante que o `user_123` sempre tenha o mesmo número de seguidores em qualquer teste, sem precisar de banco de dados.

## 🚀 Como Rodar o Projeto

1.  **Instalar dependências**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Rodar a API**:
    ```bash
    fastapi dev main.py
    ```
3.  **Rodar os Testes**:
    ```bash
    $env:PYTHONPATH = "."; pytest tests/test_analyzer.py -v
    ```

---
**Desenvolvido por Victor Hugo Almeida da Silva Govedice**
*Engenheiro de Software Full-Stack Sênior*