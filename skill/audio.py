import logging
from skill.assets.media import timer_sounds


logger = logging.getLogger(__name__)


class AudioLoader:

	song_library = timer_sounds
	scale_to_time_mapping = {'hard': 11, 'medium': 7, 'soft': 6}

	def __init__(self):
		return

	def get_song_url(self, boiling_scale, region, locale):

		url = ""
		if locale == 'de-DE':
			boiling_scale = self.translate(boiling_scale)
		boiling_time = AudioLoader.scale_to_time_mapping.get(boiling_scale, 7)
		logger.info("Getting url for boiling_time=%s, region=%s, locale=%s", boiling_time, region, locale)

		try:
			url = AudioLoader.song_library.get(region, 'eu-west-1')[boiling_time]
		except KeyError:
			logger.error("Invalid key when trying to fetch song url.", exc_info=True)

		return url

	@staticmethod
	def translate(boiling_scale):
		language_mapping = {'weich': 'soft', 'mittel': 'medium', 'hart': 'hard'}
		return language_mapping[boiling_scale]
