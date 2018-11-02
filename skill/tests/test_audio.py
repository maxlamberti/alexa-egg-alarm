import pytest
from itertools import product
from skill.audio import AudioLoader


@pytest.fixture()
def audio_loader():
	"""Returns an AudioLoader instance.
	"""
	return AudioLoader()


BOILING_SCALES = ['hard', 'medium', 'soft']
AWS_REGIONS = ['eu-west-1', 'ap-southeast-2', 'us-east-2']
LOCALE = ['en-UK']
audio_loader_parameters = product(BOILING_SCALES, AWS_REGIONS, LOCALE)

@pytest.mark.parametrize("boiling_scale,region,locale", audio_loader_parameters)
def test_audio_loader_for_valid_urls(audio_loader, boiling_scale, region, locale):
	url = audio_loader.get_song_url(boiling_scale, region, locale)
	assert url[:5] == 'https' and url[-3:] == 'mp3'
