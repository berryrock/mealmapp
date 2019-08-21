from datetime import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
from map.run_vectors import vectors

        
def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(vector.calculate_region, 'interval', minutes=60)
	scheduler.start()
	print(datetime.now(), "/Vector scheduler started/")