from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('./claveBigQuery2.json')
project_id = 'learned-pact-312010'

client = bigquery.Client(credentials=credentials, project=project_id)

QUERY = ('SELECT * FROM ProyectoIoT.TablaProyectoIoT')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print("ChipID: "+str(row[0])+",distance: "+str(row[1])+",time: "+str(row[2])+",date: "+str(row[3]))