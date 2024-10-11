from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import requests
import os

app = FastAPI()

# Game state variables
pong_time_ms = 1000  # Default value for the delay in milliseconds
game_running = False
game_paused = False

# Define a Pydantic model for the start request body
class StartGameModel(BaseModel):
    ping_delay: int

# Function to send ping to the other server
async def send_ping_to_other_server(current_port):
    other_server_port = 8001 if current_port == 8000 else 8000
    try:
        print(f"Sending ping from server on port {current_port} to server on port {other_server_port}")
        response = requests.post(f"http://localhost:{other_server_port}/ping")
        print(f"Ping sent successfully to server on port {other_server_port}, response: {response.status_code}")
    except Exception as e:
        print(f"Failed to send ping from server on port {current_port} to server on port {other_server_port}: {e}")
        raise HTTPException(status_code=500, detail="Error sending ping to other server")

# Function to handle continuous pinging
async def continuous_pinging(current_port):
    global pong_time_ms, game_running, game_paused
    while game_running and not game_paused:
        await asyncio.sleep(pong_time_ms / 1000)  # Wait for pong_time_ms
        await send_ping_to_other_server(current_port)

@app.post("/ping")
async def ping():
    current_port = int(os.getenv("PORT", 8000))
    print(f"Received ping on server running on port {current_port}")
    
    # Automatically continue pinging the other server after receiving a ping
    if game_running and not game_paused:
        await continuous_pinging(current_port)
    
    return {"message": "pong"}

@app.post("/start")
async def start_game(start_game: StartGameModel):
    global pong_time_ms, game_running, game_paused
    try:
        pong_time_ms = start_game.ping_delay
        game_running = True
        game_paused = False
        current_port = int(os.getenv("PORT", 8000))  # Fetch the current port from the environment variable
        print(f"Game started with pong_time_ms: {pong_time_ms}")
        
        # Start by sending the first ping to the other server
        await send_ping_to_other_server(current_port)
        await continuous_pinging(current_port)  # Begin continuous pinging
        return {"message": "Game started"}
    except Exception as e:
        print(f"Error in /start endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error starting the game")

@app.post("/pause")
async def pause_game():
    global game_paused
    try:
        game_paused = True
        print("Game paused")
        return {"message": "Game paused"}
    except Exception as e:
        print(f"Error in /pause endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error pausing the game")

@app.post("/resume")
async def resume_game():
    global game_paused
    try:
        game_paused = False
        print("Game resumed")
        current_port = int(os.getenv("PORT", 8000))  # Fetch the current port
        await continuous_pinging(current_port)  # Restart the ping-pong loop
        return {"message": "Game resumed"}
    except Exception as e:
        print(f"Error in /resume endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error resuming the game")

@app.post("/stop")
async def stop_game():
    global game_running, game_paused
    try:
        game_running = False
        game_paused = True
        print("Game stopped")
        return {"message": "Game stopped"}
    except Exception as e:
        print(f"Error in /stop endpoint: {e}")
        raise HTTPException(status_code=500, detail="Error stopping the game")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Use the environment variable to determine the port
    uvicorn.run(app, host="0.0.0.0", port=port)
