import psutil
import time
import pyodbc
from datetime import datetime

#SQL Server Database connection parameters
server = 'NAVEENGUPTA'
database = 'systemperformance'
driver = '{ODBC Driver 17 for SQL Server}'

# Database connection using trusted authentication
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;')
cursor = conn.cursor()

def data_extraction():
    while True:
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        cpu_interrupts = psutil.cpu_stats()[1]
        cpu_calls = psutil.cpu_stats()[3]
        memory_used = psutil.virtual_memory()[3]
        memory_free = psutil.virtual_memory()[4]
        bytes_sent = psutil.net_io_counters()[0]
        bytes_received = psutil.net_io_counters()[1]

        # Unix timestamp to datetime format conversion
        current_datetime = datetime.fromtimestamp(time.time())
        cursor.execute("INSERT INTO system_metric (datetime, cpu_percent,memory_percent,disk_percent,cpu_interrupts,cpu_calls,memory_used,memory_free,bytes_sent,bytes_received) VALUES (?,?,?,?,?,?,?,?,?,?)",
                       (current_datetime, cpu_percent,memory_percent,disk_percent,cpu_interrupts,cpu_calls,memory_used,memory_free,bytes_sent,bytes_received))
        conn.commit()
        print('Data Inserted Successfully')
        time.sleep(1)

#Main function to start data extraction function
def main():
    data_extraction()

# Main function Execution
if __name__ == "__main__":
    main()
