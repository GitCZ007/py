from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/send-task', methods=['POST'])
def handle_task():
    # Capture the JSON payload sent by the VM
    data = request.get_json()
    
    if not data or 'task_id' not in data:
        return jsonify({"status": "error", "message": "Missing task_id"}), 400
        
    task_id = data.get('task_id')
    payload = data.get('payload', '')
    
    # Print statement outputs to OKD container logs
    print(f"[OKD CONTAINER] Received Task ID: {task_id} with payload: {payload}", flush=True)
    
    # Process task logic here
    result = f"Task {task_id} processed successfully by container: {os.uname()[1]}"
    
    return jsonify({
        "status": "completed",
        "task_id": task_id,
        "result": result
    }), 200

if __name__ == '__main__':
    # OKD containers must run on unprivileged ports (like 8080)
    app.run(host='0.0.0.0', port=8080)
