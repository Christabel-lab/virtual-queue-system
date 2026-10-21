from flask import Flask, render_template, request, jsonify
from collections import deque

app = Flask(__name__)

# The Queue data structure holding active customer tickets
ticket_queue = deque()
ticket_counter = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/queue', methods=['GET'])
def get_queue():
    """Returns the current queue state as JSON."""
    return jsonify({
        "queue": list(ticket_queue),
        "total_waiting": len(ticket_queue)
    })

@app.route('/api/join', methods=['POST'])
def join_queue():
    """Customer joins the back of the queue (Enqueue)."""
    global ticket_counter
    data = request.json
    customer_name = data.get("name", "Anonymous")
    service_type = data.get("service", "General")

    ticket = {
        "id": ticket_counter,
        "name": customer_name,
        "service": service_type
    }
    
    ticket_queue.append(ticket) # Push to back of queue
    ticket_counter += 1
    
    return jsonify({"success": True, "assigned_ticket": ticket})

@app.route('/api/next', methods=['POST'])
def serve_next():
    """Staff calls the next customer from the front of the queue (Dequeue)."""
    if not ticket_queue:
        return jsonify({"success": False, "message": "Queue is empty!"}), 400
    
    served_customer = ticket_queue.popleft() # Pop from front of queue (FIFO)
    return jsonify({"success": True, "served": served_customer})

if __name__ == '__main__':
    app.run(debug=True, port=5000)