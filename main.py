from fastapi import FastAPI
import services.sharleyai as genai
from schema.request_schema import RequestBody

app = FastAPI()

# Routes
@app.get('/')
def home():
    return genai.health_check()

@app.post('/chat')
def chat(request: RequestBody):
    return genai.send_message(request.prompt, request.sessionid)
