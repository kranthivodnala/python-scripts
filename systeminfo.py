# System Info Script: Automate fetching CPU, RAM, and Disk usage

# Get the system info and save it to a file

import os
import json
import psutil
import time
import datetime
import logging

# Log the system basic info
logging.basicConfig(filename='systemlog.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def system_get_metrics():
# Fetch the System Metrics
    metrics = {
        "CPU_Usage(%)": psutil.cpu_percent(interval=1),
        "Memory_Usage(%)": psutil.virtual_memory().percent,
        "Disk_Usage(%)": psutil.disk_usage('/').percent
    }
    return metrics

def main():
# Main Logic to monitor and display system Metrics
    print("Starting System Resource Monitoring...\n")
    
    while True:
        data = system_get_metrics()
 #Print to console       
        print(json.dumps(data, indent=4))
        
        logging.info(json.dumps(data)) #Logs metrics to file
        
        time.sleep(10) # Wait for 10secs for next check
        
if __name__ == "__main__":
    main()
