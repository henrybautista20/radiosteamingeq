    #!/bin/bash

    # Start the Flask health check app in the background
    # We use nohup and & to ensure it runs even if the script is interrupted
    # Redirect stdout/stderr to files or /dev/null as needed
    echo "Starting Flask health check app..."
    nohup python /app/dummy.py > /dev/null 2>&1 &

    # Wait a moment to ensure the Flask app starts
    sleep 5

    echo "Starting main application..."
    # Execute your main application script
    # This command will run in the foreground, keeping the container alive
    exec python /app/main.py

    # The script will exit when main.py finishes
    