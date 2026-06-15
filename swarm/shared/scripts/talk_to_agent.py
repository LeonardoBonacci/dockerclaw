#!/usr/bin/env python3
"""Send a message to an OpenClaw agent via its WebSocket API and print the response."""

import json
import sys
import time
import websocket

def send_message(port: int, message: str, agent_name: str):
    """Connect to OpenClaw webchat WebSocket and send a message."""
    ws_url = f"ws://localhost:{port}/ws"
    
    print(f"\n{'='*60}")
    print(f"📨 Sending to {agent_name} (port {port}):")
    print(f"   \"{message}\"")
    print(f"{'='*60}")
    
    ws = websocket.WebSocket()
    try:
        ws.connect(ws_url, header=["Cookie: openclaw_password=openclaw"])
    except Exception as e:
        # Try alternative auth
        try:
            ws.connect(ws_url, header=["Authorization: Bearer openclaw"])
        except Exception as e2:
            print(f"❌ Could not connect to {agent_name}: {e2}")
            return None
    
    # Send auth/init
    init_msg = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "auth",
        "params": {"password": "openclaw"}
    })
    ws.send(init_msg)
    
    # Wait for auth response
    ws.settimeout(5)
    try:
        auth_resp = ws.recv()
        print(f"   Auth: {auth_resp[:100]}...")
    except:
        pass
    
    # Send the chat message
    chat_msg = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "chat.send",
        "params": {"text": message}
    })
    ws.send(chat_msg)
    
    # Collect response chunks
    full_response = []
    ws.settimeout(90)  # LLM can take time
    start = time.time()
    
    while time.time() - start < 90:
        try:
            data = ws.recv()
            if not data:
                break
            try:
                parsed = json.loads(data)
                # Look for assistant text content
                if "params" in parsed:
                    params = parsed["params"]
                    if "text" in params:
                        full_response.append(params["text"])
                    elif "content" in params:
                        full_response.append(str(params["content"]))
                    elif "delta" in params:
                        full_response.append(params["delta"])
                elif "result" in parsed:
                    result = parsed["result"]
                    if isinstance(result, dict) and "text" in result:
                        full_response.append(result["text"])
                    elif isinstance(result, str):
                        full_response.append(result)
            except json.JSONDecodeError:
                full_response.append(data)
        except websocket.WebSocketTimeoutException:
            break
        except Exception as e:
            print(f"   Error receiving: {e}")
            break
    
    ws.close()
    
    response_text = "".join(full_response) if full_response else "(no text response captured)"
    print(f"\n🤖 {agent_name} responds:")
    print(f"{'─'*60}")
    print(response_text[:2000])
    print(f"{'─'*60}")
    return response_text


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18800
    message = sys.argv[2] if len(sys.argv) > 2 else "Check your inbox"
    name = sys.argv[3] if len(sys.argv) > 3 else "Agent"
    send_message(port, message, name)
