# 🚀 MBRAS Emotion — Sistema de Análise de Sentimentos

Este projeto é uma API de alta performance desenvolvida para o desafio técnico da **MBRAS**. O sistema realiza a análise de sentimentos em tempo real de feeds de mensagens, integrando regras de negócio específicas e detecção de influência.

## 📌 O que este projeto faz?
O objetivo é processar mensagens de redes sociais e extrair inteligência baseada em dados:
1.  **Análise de Sentimento**: Identifica se a mensagem é Positiva, Negativa ou Neutra.
2.  **Influência**: Calcula o número de seguidores de um usuário de forma fixa e determinística.
3.  **Regras de Negócio**: Aplica bônus de pontuação para funcionários da empresa e lida com negações complexas e intensificadores.

## 🛠️ Tecnologias Utilizadas
- **Python 3.12**
- **FastAPI**: Framework moderno de alta performance para construção de APIs.
- **Pydantic**: Para validação rigorosa dos tipos e dados de entrada.
- **Pytest**: Suíte de testes automatizados para garantir a integridade da lógica.
- **GitHub Actions**: Pipeline de CI configurado para rodar testes a cada push/pull request.

## ⚙️ Explicação da Lógica Técnica

### Análise de Sentimento (`sentiment_analyzer.py`)
- **Negação Dupla**: O sistema implementa uma lógica semântica onde duas negações se anulam (ex: "não não gostei" é tratado como positivo).
- **Intensificadores**: Termos como "muito" ou "extremamente" elevam o peso do sentimento detectado em 50%.
- **Normalização NFKD**: O motor de análise remove acentos e caracteres especiais para garantir o matching perfeito dos termos do léxico.

### Influência Determinística
Em vez de depender de valores aleatórios ou banco de dados externo, utilizamos o **Hash SHA-256** do ID do usuário para gerar o número de seguidores. Isso garante que o mesmo usuário sempre apresente o mesmo alcance em qualquer ambiente.

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
    ```powershell
    $env:PYTHONPATH = "."; pytest tests/test_analyzer.py -v
    ```

---

## 📬 Postman Collection (JSON)
Copie o conteúdo abaixo, salve em um arquivo `.json` e importe no seu Postman para testar os cenários de sucesso e o erro customizado 422.

<details>
<summary>Clique para expandir o JSON da Collection</summary>

```json
{
	"info": {
		"name": "MBRAS Sentiment API",
		"description": "Collection para teste da API de análise de sentimentos e influência.",
		"schema": "[https://schema.getpostman.com/json/collection/v2.1.0/collection.json](https://schema.getpostman.com/json/collection/v2.1.0/collection.json)"
	},
	"item": [
		{
			"name": "Análise de Feed - Sucesso (Misto)",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n    \"messages\": [\n        {\n            \"id\": 1,\n            \"user_id\": \"user_mbras_001\",\n            \"content\": \"O sistema está muito bom!\",\n            \"timestamp\": \"2026-03-17T20:00:00Z\",\n            \"hashtags\": [\"mbras\", \"tech\"]\n        },\n        {\n            \"id\": 2,\n            \"user_id\": \"user_regular_02\",\n            \"content\": \"Não gostei muito do atraso.\",\n            \"timestamp\": \"2026-03-17T20:05:00Z\",\n            \"hashtags\": [\"feedback\"]\n        },\n        {\n            \"id\": 3,\n            \"user_id\": \"user_mbras_dev\",\n            \"content\": \"Não não gostei, achei excelente.\",\n            \"timestamp\": \"2026-03-17T20:10:00Z\",\n            \"hashtags\": [\"test\"]\n        }\n    ],\n    \"time_window_minutes\": 60\n}"
				},
				"url": {
					"raw": "http://localhost:8000/analyze-feed",
					"protocol": "http",
					"host": ["localhost"],
					"port": "8000",
					"path": ["analyze-feed"]
				}
			}
		},
		{
			"name": "Análise de Feed - Erro 422",
			"request": {
				"method": "POST",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": "{\n    \"messages\": [],\n    \"time_window_minutes\": 123\n}"
				},
				"url": {
					"raw": "http://localhost:8000/analyze-feed",
					"protocol": "http",
					"host": ["localhost"],
					"port": "8000",
					"path": ["analyze-feed"]
				}
			}
		}
	]
}