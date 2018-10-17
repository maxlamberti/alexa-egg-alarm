from skill.assets.media import egg_timer_tunes


class AudioLoader:

	song_library = egg_timer_tunes
	scale_to_time_mapping = {'hard': 11, 'medium': 7, 'soft': 6}

	def __init__(self, request):
		self.locale = request.get('locale', 'en-EN')

	def get_song_url(self, boiling_scale):
		if self.locale == 'de-DE':
			boiling_scale = self.translate(boiling_scale)
		boiling_time = AudioLoader.scale_to_time_mapping.get(boiling_scale, 7)
		return AudioLoader.song_library[boiling_time]

	@staticmethod
	def translate(boiling_scale):
		language_mapping = {'weich': 'soft', 'mittel': 'medium', 'hart': 'hard'}
		return language_mapping[boiling_scale]