Next Steps: 

cloud version:
- Frontend Web-Menu to select which patterns to track for
- SignUp, Login via AWS Cognito
- 2 Account Levels: Admin Account & User Account
    - Admin Account: can click "send anyways" for detected mesage
    - User Account: can click "approve message" by Admin
- Extension needs to know which Account & Account Level is signed in
- Database which stores the detected Information
- Do we need to store the information which goes through? -> why not, maybe we can use it later

- Host the Solution yourself: Get in Contact (Contract, no code stealing)


------

Roadmap (Order to proceed):
- create SupaBase DB
- setup Auth, SignUp, Login for Admin Account
- Admin Login -> direct to Frontend
- Landingpage: replace download link with redirect to frontend Admin SignUp/Login
- create Web Frontend [List: Message, User, TimeStamp], ["+" Button to invite Team Memebers]
- if + Button is pushed => send email to user to invite with SignUp on same Team with User Account Level [Einladungscode]

- Update Extension: Overlay/ disable Browser when nobody is signed in

- Update server_proof_data.py => store sensitive Information inside SupaBaseDB Table with team_id, user_id, mail from user, timestamp, information/message

- enable frontend to display sensitive information from supabase Table

-----

- Update Extension to recognize if user or Admin Account is signed in
- Update Extension with "send anyways" and "approve by Admin" Button
    - approve by Admin: Share a note with reason to send the information and what to work on
- enable "send anyways" button to work

- create menu with patterns to track for with admin account
- store Information inside Database per Account and connect menu to frontend

- In Admin Account: create menu for a list with messages to approve
 - with list only Admin is able to send everything and work on it
 - enable to approve to certain information for a specific user account and time span inside admin account, so user can work on it
 - why should user work with sensitive information online? -> maybe just ask him to work offline with it and more focus on detecting all information

- Menu: Ask for Individual sensitive Information to approve for

------


test-client: more tests
server_proof_data.py: more cases


add more url'S to manifest.json like chatgpt.com

update content.js to work with more url's
find HTML Element on each site of big LLM's


local version:



