from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('./claveBigQuery.json')
project_id = 'learned-pact-312010'

client = bigquery.Client(credentials=credentials, project=project_id)

def get_last_registry(chip_id):

    QUERY = ('SELECT distancia, tiempo, date FROM `learned-pact-312010.ProyectoIoT.TablaProyectoIoT` WHERE chipID='+chip_id+' ORDER BY date DESC LIMIT 1')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        datos=row
    
    return datos