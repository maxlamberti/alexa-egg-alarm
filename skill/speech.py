import logging
from skill.assets.corpus import locale_to_corpus_mapping


logger = logging.getLogger(__name__)


class InteractionModel:

	def __init__(self):

		self.corpus = locale_to_corpus_mapping

	def get_response(self, label, locale, **kwargs):
		logger.info("Fetching sentence for label='%s', locale=%s", label, locale)
		return self.corpus[locale][label].format(**kwargs)
