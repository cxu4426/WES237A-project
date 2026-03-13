#!/bin/bash
# Usage: ./board_connect.sh <REMOTE_IP>

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <REMOTE_IP>"
    exit 1
fi

REMOTE_IP=$1
LOCAL_PORT=9999
REMOTE_PORT=8888

# Clean up old FIFOs and create new ones
rm -f to_board from_board
mkfifo to_board from_board

# Open file descriptors
exec 3<>to_board
exec 4<>from_board

echo "[INFO] Listening on local port $LOCAL_PORT and connecting to $REMOTE_IP:$REMOTE_PORT"

# Connect to remote
nc $REMOTE_IP $REMOTE_PORT <&4 >&3 &
NC_REMOTE_PID=$!

# Start listener in background
nc -l $LOCAL_PORT <&3 >&4
echo "local port disconnected"

kill $NC_REMOTE_PID 2>/dev/null
echo "remote port disconnected"