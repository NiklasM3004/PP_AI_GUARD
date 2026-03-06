
MVP - Files and there functions in a flow

manifesto.json
- definiert rechte der extension

Browser_Extension.js (is installed via chrome://extensions/ )
- EventListener -> Send-Button clicked -> Send to python server

check_data_server.py
- can be started manually
- proof_data(proofes if data is consisting expressions via regex which seeme sensitive - returns just true or false
- sends back true or false to frontend

Browser_Extension.js

- receives true or false
- if true: prints alert and cancel the data to send
- if no: executes to send the data

test_check_data_server.py:
- can send multiple tests with test_prompts to the check_data_server.py







main.py
- 
Browser_Extension.py
- get_Event_Data () Event-Input
- Stop_to_send_to_backend
- send_data
- cancel_to_send_data