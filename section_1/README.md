Assumption :
- Applications are dropped into a folder with name new_applications
- Applications are stored as multiple json files and the files follow the following naming convention (<YYYYmmdd_HHMMSS>_applications.json) where YYYYmmdd_HHMMSS is the datetime in UTC when the applications are batched.
- Each application will have the following fields :
    - full_name     : The full name of the user. If it is not filled by user, it will have value of an empty string ("")
    - birthday      : The birthdate of user. The assumption is that users have to key in the birthdate in the following format (YYYY-mm-dd) when signing up on the website.
    - email         : The email of the user. If it is not filled by user, it will have value of an empty string ("")
    - mobile_number : The mobile number of the user
    - created_at    : The timestamp when the application is created. The assumption is that the timestamp will be populated using current timestamp by the website in UTC timezone. The format will be (YYYY-mm-ddTHH:MM:SSZ)
- sample application
{
    "full_name"     : "sample_first_name sample_last_name",
    "birthday"      : "1990-01-01",
    "email"         : "sample_email@emailprovider.com",
    "mobile_number  : 81818181,
    "created_at"    : "2022-11-11T01:01:00Z"
}
- Applications are considered as ready to be processed by the pipeline if the json file's last modified time longer than 10 minutes ago. This is to ensure that writing on application json files is completed by upstream application..

Design :
- The pipeline will read json files from new_applications folder
- The flow of the pipeline is as follow :
    - The pipeline will check the file's last modified time whether they are longer than 10 minutes ago
    - If yes, the file will be moved into inprogress folder.
    - The pipeline will run validity checks.
        - If it passes the validty checks, it will be transformed and moved into success folder.
        - If not, it will be moved into failure folder.
    - Afterwards, the file will move into completed folder.

To set up the environment :
- pip install -r requirements.txt

To test the flow :
- copy files from sample_dataset to new_applications folder
- run the script (python main.py)
- The files will be moved into completed folder
- There will be output file in success, failure, completed, and log