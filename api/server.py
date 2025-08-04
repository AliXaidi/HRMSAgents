# from fastapi import FastAPI, Request
# from agents.attendance_agent import attendance_agent

# app = FastAPI()

# @app.post("/attendance")
# async def chat(request: Request):
#     data = await request.json()
#     user_input = data.get("message")
#     print('User Input:', user_input)
#     response = attendance_agent.invoke(user_input)
#     return {"response": response}
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from agents.attendance_agent import attendance_agent

app = FastAPI()

# Serve static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/chat.html")

@app.post("/attendance")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message")    
    response = attendance_agent.invoke(user_input)
    return {"response": response}