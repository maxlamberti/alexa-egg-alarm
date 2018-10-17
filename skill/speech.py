import logging
from random import choice
from skill.assets.corpus import german, english


logger = logging.getLogger(__name__)


class SpeechLoader:

	locale_to_language_mapping = {'de-DE': german, 'en-EN': english}

	def __init__(self, request):

		self.locale = request.get('locale', 'en-EN')

		if self.locale not in list(SpeechLoader.locale_to_language_mapping):
			logger.warning("Unrecognized locale: %s", self.locale)

		self.corpus = SpeechLoader.locale_to_language_mapping.get(self.locale, english)
		self.speechcons = self.corpus['affirmative_speechcons']

	def get_response(self, label, **kwargs):
		return self.corpus[label].format(**kwargs)

	def random_speechcon(self):
		return choice(self.speechcons)


if __name__ == '__main__':

	LanguageAssets = SpeechLoader({'locale': 'en-EN'})
	print(LanguageAssets.get_response('help'))
	print(LanguageAssets.get_response('start_timer', boiling_scale='hard'))
