# WES237A-project
## Project description
### `take_pic.ipynb`
Code to use camera to take a picture and store it into a specified file
## How To's
### VPN Connection
- Make sure firewall is disabled
- In your `ifconfig`, look for 137 ip address. This is the UCSD VPN's address
- Test connection with other computer by pinging their ip address
    - `ping <ip_address>`
- If that works, one computer can run `nc -l <port_number>`
- The other computer run `nc <first_computer_ip_addr> <port_number>`
- The boards should be able to talk to each other
### Connecting the two boards
- Board connection is port 9999, 5555
- Computer connection is port 8888, 4444
- A is on MacOS, B is on Windows.
#### Board A is Client, Board B is Server
##### Board A:
- `nc 192.168.2.1 9999`
##### Computer A:
- `rm -f to_board from_board`
- `mkfifo to_board from_board`
- `exec 3<>to_board`
- `exec 4<>from_board`
- `nc -l 9999 <&3 >&4`
- `nc 137.110.40.73 8888 <&4 >&3`
##### Computer B:
- `ncat -l 8888 --sh-exec "ncat 192.168.2.99 9999"`
##### Board B:
- `nc -l 9999`

#### Board A is Server, Board B is Client
##### Board A:
`nc -l 5555`
##### Computer A:
- `rm -f to_board2 from_board2`
- `mkfifo to_board2 from_board2`
- `exec 5<> to_board2`
- `exec 6<> from_board2`
- `nc 192.168.2.99 5555 <&5 >&6`
- `nc -l 4444 <&6 >&5`
##### Computer B:
- `ncat 137.110.33.167 4444 --ssh-exec "ncat -l 5555`
##### Board B:
- `nc 192.168.2.1 5555`
## References
| Description | Link |
| ---- | --- |
Capture image from camera | https://www.youtube.com/watch?v=am3lU0ZKaI0 |
Haarcascade frontal face detection | https://docs.opencv.org/4.x/d2/d99/tutorial_js_face_detection.html |
Another face detection example | https://github.com/XS30/Face-detection-in-PYNQ/blob/main/Face%20detection%20project%20(2).ipynb |
Hair detection | https://github.com/BryanBetancur/hair-color-detector?tab=readme-ov-file |
