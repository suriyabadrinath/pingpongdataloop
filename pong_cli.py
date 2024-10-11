import sys
import requests

server_url = "http://localhost:8000"  # Server 1 URL by default

def start_game(pong_time_ms):
    # Send ping_delay as JSON in the request body
    response = requests.post(f"{server_url}/start", json={"ping_delay": pong_time_ms})
    
    if response.status_code == 200:
        try:
            print(response.json())
        except ValueError:
            print(f"Failed to parse JSON, raw response: {response.text}")
    else:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response content: {response.text}")

def pause_game():
    response = requests.post(f"{server_url}/pause")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response content: {response.text}")

def resume_game():
    response = requests.post(f"{server_url}/resume")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response content: {response.text}")

def stop_game():
    response = requests.post(f"{server_url}/stop")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response content: {response.text}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pong_cli.py <command> <param>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start":
        if len(sys.argv) != 3:
            print("Usage: python pong_cli.py start <pong_time_ms>")
            sys.exit(1)
        pong_time_ms = int(sys.argv[2])
        start_game(pong_time_ms)
    elif command == "pause":
        pause_game()
    elif command == "resume":
        resume_game()
    elif command == "stop":
        stop_game()
    else:
        print("Unknown command. Use start, pause, resume, or stop.")
