import sys
import os
# Adiciona a raiz do projeto ao path para achar o sentiment_analyzer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sentiment_analyzer import analyze_message_sentiment

def test_basic_positive():
    sentiment, score = analyze_message_sentiment("bom otimo", is_mbras_emp=False)
    assert sentiment == "positive"
    assert score > 0.1

def test_double_negation():
    # "não não gostei" -> deve ser positivo (negação dupla se anula)
    sentiment, score = analyze_message_sentiment("não não gostei", is_mbras_emp=False)
    assert sentiment == "positive"

def test_mbras_bonus():
    # Funcionário MBRAS com palavra positiva ganha x2
    _, score_normal = analyze_message_sentiment("bom", is_mbras_emp=False)
    _, score_mbras = analyze_message_sentiment("bom", is_mbras_emp=True)
    assert score_mbras == score_normal * 2

def test_orphan_intensifier():
    # "muito" sozinho não tem valor positivo nem negativo
    sentiment, _ = analyze_message_sentiment("muito", is_mbras_emp=False)
    assert sentiment == "neutral"