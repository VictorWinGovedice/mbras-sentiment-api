import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# IMPORTAÇÃO CORRIGIDA: usando o nome em português conforme seu arquivo original
from sentiment_analyzer import analisar_sentimento_mensagem

def test_basic_positive():
    # PARÂMETROS CORRIGIDOS: eh_func_mbras e retorno "positivo"
    sentiment, score = analisar_sentimento_mensagem("bom otimo", eh_func_mbras=False)
    assert sentiment == "positivo"
    assert score > 0.1

def test_double_negation():
    # "não não gostei" -> deve ser positivo (negação dupla se anula)
    sentiment, score = analisar_sentimento_mensagem("não não gostei", eh_func_mbras=False)
    assert sentiment == "positivo"

def test_mbras_bonus():
    # Funcionário MBRAS com palavra positiva ganha x2
    _, score_normal = analisar_sentimento_mensagem("bom", eh_func_mbras=False)
    _, score_mbras = analisar_sentimento_mensagem("bom", eh_func_mbras=True)
    assert score_mbras == score_normal * 2

def test_orphan_intensifier():
    # "muito" sozinho não tem valor positivo nem negativo
    sentiment, _ = analisar_sentimento_mensagem("muito", eh_func_mbras=False)
    assert sentiment == "neutro"