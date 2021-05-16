from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('./claveBigQuery.json')
project_id = 'learned-pact-312010'

client = bigquery.Client(credentials=credentials, project=project_id)
chip_id = 418957

QUERY = ('SELECT distancia, tiempo, date FROM `learned-pact-312010.ProyectoIoT.TablaProyectoIoT` WHERE chipID='+str(chip_id)+' ORDER BY date DESC LIMIT 1')
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

print(rows.values)

#print("distance: "+str(rows[0][0])+",time: "+str(rows[0][1])+",date: "+str(rows[0][2]))