from fastapi import FastAPI, Form, Response
from prometheus_client import Counter, Summary, generate_latest, CONTENT_TYPE_LATEST
from main import chain
import mlflow
import uvicorn
import time

app = FastAPI()

REQUEST_COUNT = Counter('request_count', 'Total API Requests', ['endpoint'])
REQUEST_LATENCY = Summary('request_latency_seconds', 'API Request latency', ['endpoint'])

@app.post("/summarize")
def summarize(text: str = Form(..., min_length=200)):
    start = time.time()
    # MLflow log
    with mlflow.start_run():
        mlflow.log_param("input_length", len(text))
        try: 
            summary = chain.invoke(text)
        except Exception as e: 
            mlflow.log_param("error", str(e))
            return {"error": str(e)}
        
        mlflow.log_metric("summary_length", len(summary))
    
    latency = time.time() - start
    REQUEST_COUNT.labels(endpoint="/summarize").inc()
    REQUEST_LATENCY.labels(endpoint="/summarize").observe(latency)
    
    return {"summary": summary}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
def read_root():
    return {"message": "check /metrics for Prometheus metrics and check /docs for API usage"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
