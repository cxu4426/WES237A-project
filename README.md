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
### [SSH port forwarding](#ssh-port-forwarding)
Port forwarding allows the computer to connect to each and then forward the message to the board. There are three main steps to achieve a connection and test it on just one computer.
1. In your board terminal, run `nc -l <port>`
    - This sets up the client socket
    - The terminal should look "stuck". It is waiting for input/connection
2. In your local terminal, run `ssh -N -L <port>:127.0.0.1:<port> xilinx@<board_ip_addr>`
    - The terminal should look "stuck". It is creating that tunnel from the local computer to the board
    - ex: `ssh -N -L 8888:127.0.0.1:8888 xilinx@192.168.2.99`
3. In another local terminal, run `nc localhost 8888`
    - This sets up the server socket
You should now be able to send and receive messages between the server terminal (local) and the client terminal (board).
### Connecting the boards over VPN
This connection two boards connected to two computers. The computers share the same network. In this example, the hardware is split into board/computer A and board/computer B.
#### On the B side (Server Board):
Follow steps 1 and 2 of the [SSH port forwarding](#ssh-port-forwarding) section.

### On the A side (Client Board):
1. In a local terminal, run `ssh -N -L <port>:127.0.0.1:<port> user@<laptop_B_vpn_ip>`
    - This creates a tunnel from Computer A to Computer B since they share the same VPN
    - Refer to the [find ssh username](#finding-the-ssh-username) section to 

2. In the board terminal, run `nc <laptop_a_eth_ip> <port>`
    - This should connect the two boards together due to the forwarding set up and the server on the B side
    - ex: `nc 192.168.2.1 8888`

#### Test communication
- Anything typed on Board A’s terminal should appear on Board B’s terminal and vice versa.  
- The path of the connection is
```
Board A → Laptop A → VPN → Laptop B → Board B
```

### [Finding the SSH Username](#finding-the-ssh-username)
The `user` in the SSH command is the username you log into on the remote computer. Here's how to find it:

#### On macOS / Linux
1. Open a terminal.
2. Run:
```bash
whoami
```
3. The output is your username. Example:
```text
alice
```

#### On Windows
1. Open Command Prompt or PowerShell.
2. Run:
```powershell
echo %USERNAME%
```
3. The output is your username. Example:
```text
alice
```

Use this username in your SSH commands:

```bash
ssh -N -L <port>:127.0.0.1:<port> <user>@<laptop_B_vpn_ip>
```
Replace `<user>` with the name you found, and `<laptop_B_vpn_ip>` with Laptop B’s VPN IP.
## References
| Description | Link |
| ---- | --- |
Capture image from camera | https://www.youtube.com/watch?v=am3lU0ZKaI0 |
Haarcascade frontal face detection | https://docs.opencv.org/4.x/d2/d99/tutorial_js_face_detection.html |
Another face detection example | https://github.com/XS30/Face-detection-in-PYNQ/blob/main/Face%20detection%20project%20(2).ipynb |
Hair detection | https://github.com/BryanBetancur/hair-color-detector?tab=readme-ov-file |
