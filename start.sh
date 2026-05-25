#!/bin/bash

# Start the Flask health check app in the background
echo "Starting Flask health check app..."
nohup python dummy.py > flask.log 2>&1 &

# Wait a moment to ensure the Flask app starts
sleep 3

# Check if Flask app is running
if ps aux | grep -v grep | grep "dummy.py" > /dev/null
then
    echo "Flask health check app successfully started."
else
    echo "WARNING: Flask health check app failed to start."
fi

echo "Starting main application..."
# Execute the main application script in the foreground to keep container alive
exec python main.py