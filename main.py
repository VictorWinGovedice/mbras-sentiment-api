from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List
import time
from sentiment_analyzer import analisar_sentimento_mensagem, obter_seguidores_deterministicos

app = FastAPI(title="API MBRAS Emotion")

# Requisito 2A: Tratamento customizado para erro 422
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    for error in errors:
        if "time_window_minutes" in str(error.get("loc")) and error.get("input") == 123:
            return JSONResponse(
                status_code=422,
                content={"code": "UNSUPPORTED_TIME_WINDOW"}
            )
    return JSONResponse(status_code=400, content={"detail": errors})

class Mensagem(BaseModel):
    id: int
    user_id: str = Field(pattern=r"^user_[a-z0-9_]{3,}$") # Validação por Regex
    content: str = Field(max_length=280)
    timestamp: str 
    hashtags: List[str]

class FeedRequest(BaseModel):
    messages: List[Mensagem]
    time_window_minutes: int

@app.post("/analyze-feed")
async def analisar_feed(data: FeedRequest):
    # Regra de negócio manual para erro 422
    if data.time_window_minutes == 123:
        raise HTTPException(status_code=422, detail={"code": "UNSUPPORTED_TIME_WINDOW"})
        
    inicio = time.perf_counter()
    resultados = []
    
    for msg in data.messages:
        # Verifica se é funcionário (ignora maiúsculas/minúsculas)
        eh_mbras = "mbras" in msg.user_id.lower()
        
        sentimento, score = analisar_sentimento_mensagem(msg.content, eh_mbras)
        seguidores = obter_seguidores_deterministicos(msg.user_id)
        
        resultados.append({
            "mensagem_id": msg.id,
            "user_id": msg.user_id,
            "sentimento": sentimento,
            "funcionario_mbras": eh_mbras,
            "seguidores": seguidores,
            "pontuacao": round(score, 4)
        })

    tempo_ms = (time.perf_counter() - inicio) * 1000
    
    return {
        "tempo_execucao_ms": round(tempo_ms, 2),
        "total_processado": len(resultados),
        "resultados": resultados
    }