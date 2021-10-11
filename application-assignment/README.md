# application-assignment

**Note**: 
----------
For the assignment purpose only, in order to make it easy to run the consumer over and over using hte same data

All exist table data, is been truncated at the beginning of the consumer service - Of course this is not for production use, only for the sake of this assignment.**

**Note2:**
------
For executing the consumer service, I've used the postgres and rabbitmq docker-compose ymls, which are located at the 'docker-compose-dependencies' folder.
I've faced following issue while trying to start the main docker-compose.yaml (for both publisher and consumer):
TypeError: main() missing 1 required positional argument: 'loop'

Therefore, I've added the postgres and rabbitmq docker-compose.yaml file into the 'docker-compose-dependencies' folder, and started each of them using docker compose.
Then, I've triggered each of the 'publisher' & 'consumer' services using Intellij - And then all worked! 


Consumer APIs:
==============
1) Get patient medications period by patient id and medication name 
    
   1) Description: This API returns all patient's medication closed periods (i.e: medication has valid, non-null start date time and end date time)
       - URL: /getPatientMedsPeriods
       - request parameters:
      
           - p_id
           - med
       

         Request example:
           - request example: http://localhost:5000/getPatientMedsPeriods?p_id=1&med=X
         Responses:
           200 - response example: 
             [
                {
                "medication_name": "X",
                "medication_period_end": "Wed, 06 Oct 2021 01:00:00 GMT",
                "medication_period_start": "Fri, 01 Jan 2021 00:00:00 GMT",
                "p_id": 1
                },
                {
                "medication_name": "X",
                "medication_period_end": "Wed, 06 Oct 2021 01:00:00 GMT",
                "medication_period_start": "Fri, 01 Oct 2021 00:00:00 GMT",
                "p_id": 1
                }
             ]
         400 (NOT_FOUND):
             Request example:
           - request example: http://localhost:5000/getPatientMedsPeriods?p_id=1&med=Y
             response: 'No medication periods has been found for patient 1 with medication: Y'
2) Get all patient medications period by patient id
   1) Description: This API returns all patient's medication periods (i.e: non-null start date time and, end date time might be null - so period is still open for patient medication)
      - URL: /getPatientAllMedsPeriods
      - request parameters:

         - p_id


         Request example:
           - request example: http://localhost:5000/getPatientAllMedsPeriods?p_id=1
         Responses:
           200 - response example: 
             [
               {
                  "medication_name": "X",
                  "medication_period_end": "Fri, 01 Jan 2021 01:00:00 GMT",
                  "medication_period_start": "Fri, 01 Jan 2021 00:00:00 GMT",
                  "p_id": 1
               },
               {
                  "medication_name": "X",
                  "medication_period_end": "Wed, 06 Oct 2021 01:00:00 GMT",
                  "medication_period_start": "Fri, 01 Oct 2021 00:00:00 GMT",
                  "p_id": 1
               },
               {
                  "medication_name": "X",
                  "medication_period_end": null,
                  "medication_period_start": "Thu, 07 Oct 2021 00:00:00 GMT",
                  "p_id": 1
               },
               {
                  "medication_name": "Y",
                  "medication_period_end": null,
                  "medication_period_start": "Sat, 09 Oct 2021 12:30:00 GMT",
                  "p_id": 1
               }
            ]
         400 (NOT_FOUND):
            request: http://localhost:5000/getPatientAllMedsPeriods?p_id=13
            response: 'No medication periods has been found for patient:13'
       