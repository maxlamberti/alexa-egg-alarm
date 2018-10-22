import logging
from random import choice
from skill.assets.corpus import locale_to_corpus_mapping


logger = logging.getLogger(__name__)


class InteractionModel:

	def __init__(self):

		self.corpus = locale_to_corpus_mapping

	def get_response(self, label, locale, **kwargs):
		return self.corpus[locale].get_response(label, **kwargs)
