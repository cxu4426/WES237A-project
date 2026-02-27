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
Board connection is port 9999

Computer connection is port 8888
#### Board A:
- `nc 192.168.2.1 9999`
#### Computer A:
- `mkfifo to_board from_board`
- `nc -l 9999 < to_board > from_board &`
- `nc 137.110.40.73 8888 < from_board > to_board &`
- `tee from_board`
#### Computer B:
- `ncat -l 8888 --sh-exec "ncat 192.168.2.99 9999"`
#### Board B:
- `nc -l 9999`
## References
| Description | Link |
| ---- | --- |
Capture image from camera | https://www.youtube.com/watch?v=am3lU0ZKaI0 |
Haarcascade frontal face detection | https://docs.opencv.org/4.x/d2/d99/tutorial_js_face_detection.html |
Another face detection example | https://github.com/XS30/Face-detection-in-PYNQ/blob/main/Face%20detection%20project%20(2).ipynb |
Hair detection | https://github.com/BryanBetancur/hair-color-detector?tab=readme-ov-file |
