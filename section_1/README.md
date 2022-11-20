Assumption :
- Applications are dropped into a folder with name new_applications
- Applications are stored as 1 json file and the file follows the following naming convention (<YYYYmmdd_HHMMSS>_applications.json) where YYYYmmdd_HHMMSS is the datetime in UTC when the applications are batched.
- Each application will have the following fields :
    - full_name     : The full name of the user. If it is not filled by user, it will have value of an empty string ("")
    - first_name    : The first name of the user. If it is not filled by user, it will have value of an empty string ("")
    - last_name     : The last name of the user. If it is not filled by user, it will have value of an empty string (""). This field can be ignored by user with only single name.
    - birthdate      : The birthdate of user. The assumption is that users have to key in the birthdate in the following format (YYYY-mm-dd) when signing up on the website.
    - email         : The email of the user. If it is not filled by user, it will have value of an empty string ("")
    - created_at    : The timestamp when the application is created. The assumption is that the timestamp will be populated using current timestamp by the website in UTC timezone. The format will be (YYYY-mm-ddTHH:MM:SSZ)
- sample application
{
    "full_name"     : "sample_first_name sample_last_name"
    "first_name"    : "sample_first_name",
    "last_name"     : "sample_last_name",
    "birthday"      : "1990-01-01",
    "email"         : "sample_email@emailprovider.com",
    "created_at"    : "2022-11-11T01:01:00Z"
}
- Applications are considered as ready to be processed by the pipeline if the json file's last modified time or created time longer than 10 minutes ago. This is to ensure that writing on application json files is completed by upstream application.
- The SLA to process the pipeline is more than 2 hours from the time the json file is dropped in the new_applications folder.
- The number of applications is less than what the pipeline can process within 1 hour. If not, update the SLA to a longer time and timeout of pipeline.

Design :
- The pipeline will read json files from new_applications folder
- The pipeline will create 4 folders if they do not exist (inprogress, success, failure, logs)
- The flow of the pipeline is as follow :
    - The pipeline will check the file's created time or last modified time whether they are longer than 10 minutes ago
    - If yes, the file will be moved into inprogress folder.
    - The pipeline will run validity checks and clean the data. If the file is successfully ingested, it will be moved into success folder. If the file fails to be ingested, it will be moved into failure folder. At any point 