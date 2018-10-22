import logging
from random import choice
from skill.assets.corpus import german, english


logger = logging.getLogger(__name__)


class SpeechLoader:

	language_to_corpus_mapping = {'de': german, 'en': english}

	def __init__(self, language):

		self.language = language
		self.corpus = SpeechLoader.language_to_corpus_mapping.get(language, english)
		self.speechcons = self.corpus['affirmative_speechcons']

	def get_response(self, label, **kwargs):
		return self.corpus[label].format(**kwargs)

	def random_speechcon(self):
		return choice(self.speechcons)


class InteractionModel:

	available_languages = ['de', 'en']

	def __init__(self):

		self.speech = {}
		for lang in InteractionModel.available_languages:
			self.speech[lang] = SpeechLoader(lang)

	def start_up_response(self, new_user, default, last_boiling_scale, locale, session):

		lang = self.get_language(locale)

		if new_user:
			response = self.speech[lang].get_response('ask_scale')
		elif default:
			response = self.speech[lang].get_response('start_default')
		else:
			response = self.speech[lang].get_response('ask_scale_and_default', boiling_scale=last_boiling_scale)
			session.attributes['state'] = 'might_set_default'

		return response

	def get_response(self, label, locale, **kwargs):
		lang = self.get_language(locale)
		return self.speech[lang].get_response(label, **kwargs)

	@staticmethod
	def get_language(locale):
		try:
			lang = locale[:2]
		except TypeError:
			lang = 'en'
			logger.error("Failed getting language for locale=%s", locale, exc_info=True)
		return lang


if __name__ == '__main__':

	LanguageAssets = SpeechLoader({'locale': 'en-EN'})
	print(LanguageAssets.get_response('help'))
	print(LanguageAssets.get_response('start_timer', boiling_scale='hard'))
