In this Portfolio Project I want to demonstrate the technical experiences and capabilities, which are described in the following and referenced to specific directory/file paths.


A: INSTALLATION GUIDE:

The system was developed on MacOS. To run the software:

1. setup a .venv
2. install dependencies via requirements.txt
3. start MongoDB locally via docker-compose.yaml while Docker Desktop is running
4. start the python flask server
5. start the websockets server at the same time inside a different terminal window
6. start the frontend via npm run start in a 3rd terminal window

The python flask server is located inside /src/check_data_server/server_proof_data.py.
The websockets server is located inside /src/ws/websocket.py.


B: DEMONSTRATED TEC-SKILLS & FILE-PATHS:

- coming up with a solution for a siple business problem
- /requirements.txt: 
    - keeping track of dependencies via requirements.txt and working with python virtual environment

- /src/Browser_Extension/Google_HTML_Element_Location: 
    - Reading into a websites HTML via web console and identifying relevant elements to interact with

- /src/Browser_Extension_Setup_Folder: 
    - creating a chrome browser extension
  
- /src/check_data_server/server_proof_data.py: 
    - creating a Python Flask Server (interacting with chrome browser extension)
    - working with RegEx in Python Flask Server

- /src/check_data_server/README_build.exe.md/
    - Tranforming Python Flask Server into locally runnable File

- /src/check_data_server/test_client.py: 
    - creating tests for RegEx Patterns

- frontend/index.html: 
    - creating a simple HTML Page
    
- package.json
    - defining a run command for HTML page via package.json

- /src/ws/WS_MSG_AUTH:
- /src/ws/websocket.py:
- /frontend/index.html:
    - Creating User Sign-Up, Login, Auth via AWS Cognito
    - loading Sign-Up Page until user is logged in inside frontend
    - exchanging AWS Cognito auth_code for token via jwt
    - Setting Up Backend- and Frontend-Side of Websockets Server, managing Websockets Handshake
    - using tenant- and session_id inside Backend, Frontend and Chrome-Extension
    - communication between backend Auth-Mechanism and frontend-page via websockets

- docker-compose.yaml:
    - Setting Up MongoDB, via Docker-Compose:



