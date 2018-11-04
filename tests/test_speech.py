import pytest
from itertools import product
from skill.speech import InteractionModel
from skill.assets.corpus import german, english_1, english_2


ALL_RESPONSES = set(german).union(set(english_1)).union(set(english_2))
ALL_RESPONSES.remove('affirmative_speechcons')
LOCALES = ['de-DE', 'en-CA', 'en-GB', 'en-US', 'en-AU', 'en-IN']
speech_loader_params = product(ALL_RESPONSES, LOCALES)


@pytest.fixture()
def interaction_model():
	"""Returns an InteractionModel instance.
	"""
	return InteractionModel()


def test_corpus_for_response_completeness():
	errors = []
	if not set(german) == set(english_1):
		set_diff = set(german).symmetric_difference(set(english_1))
		error_message = "german and english_1 have difference: {}".format(set_diff)
		errors.append(error_message)
	if not set(german) == set(english_2):
		set_diff = set(german).symmetric_difference(set(english_2))
		error_message = "german and english_2 have difference: {}".format(set_diff)
		errors.append(error_message)
	assert not errors, "errors occurred:\n{}".format("\n".join(errors))


@pytest.mark.parametrize("label,locale", speech_loader_params)
def test_interaction_model_responses(interaction_model, label, locale):
	assert isinstance(interaction_model.get_response(label, locale, boiling_scale='hard'), str)
