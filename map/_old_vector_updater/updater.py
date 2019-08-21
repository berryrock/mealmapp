from datetime import datetime
import os
from apscheduler.schedulers.background import BackgroundScheduler
from map.vector_updater import vector

        
def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(vector.calculate_region, 'interval', minutes=60)
	scheduler.start()
	print(datetime.now(), "/Vector scheduler started/")