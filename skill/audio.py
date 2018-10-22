from random import choice
from skill.assets.media import egg_timer_tunes


class AudioLoader:

	song_library = egg_timer_tunes
	scale_to_time_mapping = {'hard': 11, 'medium': 7, 'soft': 6}

	def __init__(self, locale):
		self.locale = locale

	def get_song_url(self, boiling_scale):
		if self.locale == 'de-DE':
			boiling_scale = self.translate(boiling_scale)
		boiling_time = AudioLoader.scale_to_time_mapping.get(boiling_scale, 7)
		return choice(AudioLoader.song_library[boiling_time])

	@staticmethod
	def translate(boiling_scale):
		language_mapping = {'weich': 'soft', 'mittel': 'medium', 'hart': 'hard'}
		return language_mapping[boiling_scale]
