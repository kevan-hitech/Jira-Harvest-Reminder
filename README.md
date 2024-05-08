# Installation Guide

## Generate Google Credentials

Follow these steps [insert link or detailed steps here].

## Download Repository from Github

## Install Additional Python Libraries

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip install fastapi
pip install uvicorn
```

## Create Credentials Folder
```mkdir credentials```
## Create a folder named credentials in your project directory.
Place credentials.json and token.json files inside the credentials folder.
# Starting the Server
## Run the Server Temporarily
```python3 main.py```
## Run the Server Continuously
```nohup python3 main.py &```
Stopping the Server
Create a Script to Stop the Server
Open a terminal and create a script file:
```nano kill_server.sh```
Copy and paste the following into the script file:
```
#!/bin/bash
# Find the PID of the process using port 8080
PID=$(lsof -ti:8080)

# Check if any PID was found
if [ -z "$PID" ]; then
  echo "No process is using port 8080."
else
  # Kill the process
  kill $PID
  if [ $? -eq 0 ]; then
    echo "Process using port 8080 has been terminated."
  else
    echo "Failed to terminate the process using port 8080. You might need to run the script as superuser."
  fi
fi
```
