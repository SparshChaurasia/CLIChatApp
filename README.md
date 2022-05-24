# Command Line Chat App
A command line interface chat app built with pyhton - socket and multithreading

## Running 
#### Make sure to get python 3.9 or higher
This runtime is required to run the bot

#### Setup a virtual environment
1. Install the virtual environment maker tool
    ```bash
    pip install virtualenv
    ```

2. Create a virtual environment (you could name the environment anything)
    ```bash
    virtualenv venv
    ```

3. Activate virtual environment 
    (for linux and mac)
    ```bash
    source ./venv/Scripts/activate
    ```
    (for windows)
    ```powershell
    ./venv/Scripts/activate
    ```

#### Install required packages
```bash
pip install -r requirements.txt
```

#### Setup a server
Clone the repository and run the server.py file on localhost or your public ip

#### Join the chat!
Anyone could join the chat using the client.py file given, the ip and the port number

## Screenshots
![chat-preview](/images/chat-preview.png)
![terminal-server-preview](/images/terminal-server-preview.JPG)

## Documentation
- [socket documentation — Low-level networking interface](https://docs.python.org/3/library/socket.html)
- [threading documentation — Thread-based parallelism](https://docs.python.org/3/library/threading.html/)
- [rich documentation](https://rich.readthedocs.io/en/stable/introduction.html)

## Acknowledgements
 - [Simple chat app python](https://www.neuralnine.com/tcp-chat-in-python/)