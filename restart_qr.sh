/usr/bin/ps -aux | /usr/bin/grep -v 'grep' | /usr/bin/grep 'qr_server.py' > /dev/null
if [ $? -ne 0 ]; then
    /usr/bin/tmux new-session -d -s qr_server /usr/bin/env python3 /home/oac/qr/qr_server.py localhost 5000
fi
