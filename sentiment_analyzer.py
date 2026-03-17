import unicodedata
import hashlib

# Lexicon (Dicionário) conforme as especificações do desafio
POSITIVO = {"bom", "otimo", "adorei", "excelente", "top", "gostei"}
NEGATIVO = {"ruim", "pessimo", "odiei", "horrivel", "nao"}
INTENSIFICADORES = {"muito", "super", "extremamente"}
NEGACOES = {"nao", "nunca", "jamais"}

def normalizar_termo(texto: str) -> str:
    """Remove acentos e padroniza para minúsculas."""
    return "".join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c)).lower()

def analisar_sentimento_mensagem(texto: str, eh_func_mbras: bool):
    raw_tokens = texto.split()
    # Limpeza e normalização de cada palavra
    tokens = [normalizar_termo(t.strip("!?.,")) for t in raw_tokens]
    
    pontuacao_total = 0.0
    
    for i, token in enumerate(tokens):
        valor = 0
        if token in POSITIVO: valor = 1
        elif token in NEGATIVO: valor = -1
        
        if valor != 0:
            # 1. Regra de Intensificador (olha 1 palavra atrás)
            if i > 0 and tokens[i-1] in INTENSIFICADORES:
                valor *= 1.5
            
            # 2. Regra de Negação (olha até 3 palavras atrás)
            # Lógica de anulação: se houver 2 negações, elas se cancelam (fica positivo)
            contagem_negacao = 0
            for j in range(max(0, i-3), i):
                if tokens[j] in NEGACOES:
                    contagem_negacao += 1
            
            if contagem_negacao % 2 != 0:
                valor *= -1
            
            # 3. Regra MBRAS (Bônus x2 para funcionários em palavras positivas)
            if eh_func_mbras and valor > 0:
                valor *= 2
                
            pontuacao_total += valor

    # Média da pontuação pelo total de palavras
    score_final = pontuacao_total / len(tokens) if tokens else 0
    
    if score_final > 0.1: return "positivo", score_final
    if score_final < -0.1: return "negativo", score_final
    return "neutro", score_final

def obter_seguidores_deterministicos(user_id: str) -> int:
    """Gera um número de seguidores fixo para cada ID usando SHA-256."""
    hash_obj = hashlib.sha256(user_id.encode())
    return (int(hash_obj.hexdigest(), 16) % 10000) + 100