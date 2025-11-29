from flask import Flask, request, Response
import json
from . import config
from .task_queue import queue

app = Flask(__name__)
app.logger.setLevel('INFO')
app.count = 0

@app.route(f'/webhook/{config.webhook_secret}', methods=['POST'])
def receive_webhook():
    raw = request.get_data(as_text=True)
    payload = json.loads(raw) if raw else None
    
    if not payload: return Response(status=200)

    queue.send_task(config.task_name, args=[payload])
    app.count += 1
    app.logger.info(f"Event {payload.get('event')} received and queued. Total Processed: {app.count}")

    return Response(status=200)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3535)