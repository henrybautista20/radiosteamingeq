from flask import Flask, Response

app = Flask(__name__)

# Define the liveness probe endpoint
@app.route('/healthz', methods=['GET'])
def liveness_probe():
    """
    Dummy liveness probe endpoint.
    Always returns a 200 OK status to indicate the application is alive.
    """
    # Return a simple text response with a 200 status code
    return Response("OK", status=200, mimetype='text/plain')

# You can add other routes for your actual application logic here
# @app.route('/')
# def index():
#     return "Hello, World!"

if __name__ == '__main__':
    # Run the Flask application
    # In a production container environment, you would typically use a more robust
    # web server like Gunicorn or uWSGI. For a simple dummy, this is fine.
    # Listen on all available interfaces (0.0.0.0) and a common port (e.g., 8080)
    app.run(host='0.0.0.0', port=8080)
