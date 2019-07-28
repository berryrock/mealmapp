from django.apps import AppConfig


class MapConfig(AppConfig):
	name = 'map'

	def ready(self):
		from .vector_updater import updater
		updater.start()
