# -*- coding: utf-8 -*-

import os
import logging.config
from flask import Flask
from flask_ask import Ask, statement, question, session, audio, request

from skill.audio import AudioLoader
from skill.speech import InteractionModel
from skill.loggingconf import logging_config
from skill.database import DatabaseConnector


env = os.environ.get('ENVIRONMENT')
default_locale = os.environ.get('DEFAULT_LOCALE')
region = os.environ.get('REGION')

logging.config.dictConfig(logging_config)
logger = logging.getLogger(env)

db = DatabaseConnector(region)

interaction_model = InteractionModel()
media = AudioLoader()

app = Flask(__name__)
ask = Ask(app, "/")


def get_locale(default=default_locale):
	return request.get('locale', default)


@app.route('/test')
def activity_test():
	return "It's an eggciting world!"


@ask.launch
def welcome_message():

	alexa_id = session.user.userId
	locale = get_locale()
	user_data = db.get_user(alexa_id)
	default_boiling_scale = user_data.get('default_boiling_scale', '')
	block_preference = user_data.get('block_preference', False)
	last_boiling_scale = user_data.get('last_boiling_scale', '')
	num_visits = user_data.get('num_visits', 1)
	reprompt = interaction_model.get_response('reprompt', locale)

	if user_data:
		db.update_visit(alexa_id)

	if not user_data:  # first time user
		user_data = db.initialize_user(alexa_id, locale)
		response = interaction_model.get_response('ask_scale', locale)
	elif default_boiling_scale:  # returning user with a set default
		response = interaction_model.get_response('start_default', locale, boiling_scale=default_boiling_scale)
		if num_visits % 3 == 0:  # add info message on how to reset default
			response += interaction_model.get_response('reset_info', locale)
		song_url = media.get_song_url(default_boiling_scale, region, locale)
		return audio(response).play(song_url, offset=0)
	elif last_boiling_scale and not block_preference:  # returning user with no set default
		response = interaction_model.get_response('ask_scale_and_default', locale, boiling_scale=last_boiling_scale)
		session.attributes['state'] = 'might_set_default'
	else:
		response = interaction_model.get_response('ask_scale', locale)

	session.attributes['user_data'] = user_data

	return question(response).reprompt(reprompt)


@ask.intent('SetBoilingScaleIntent', convert={'boiling_scale': str})
def set_timer_intent(boiling_scale):

	alexa_id = session.user.userId
	locale = get_locale()
	if isinstance(boiling_scale, str):
		boiling_scale = boiling_scale.lower()

	if boiling_scale not in ['soft', 'medium', 'hard', 'weich', 'mittel', 'hart']:
		response = interaction_model.get_response('error', locale)
		reprompt = interaction_model.get_response('reprompt', locale)
		return question(response).reprompt(reprompt)

	response = interaction_model.get_response('start_timer', locale, boiling_scale=boiling_scale)
	db.set_last_boiling_scale(alexa_id, boiling_scale)

	song_url = media.get_song_url(boiling_scale, region, locale)

	return audio(response).play(song_url, offset=0)


@ask.intent('DeletePreference')
def delete_preference():
	locale = get_locale()
	alexa_id = session.user.userId
	response = interaction_model.get_response('delete_preferences', locale)
	db.remove_preferences(alexa_id)
	logger.info("Deleting preferences for alexa_id=%s", alexa_id)
	return question(response)


@ask.intent('AMAZON.YesIntent')
def yes_intent():

	locale = get_locale()
	state = session.attributes.get('state', '')
	reprompt = interaction_model.get_response('reprompt', locale)

	if state == 'might_set_default':
		alexa_id = session.user.userId
		boiling_scale = session.attributes['user_data'].get('last_boiling_scale', '')
		db.set_boiling_scale_preference(alexa_id, boiling_scale)
		response = interaction_model.get_response('set_default', locale, boiling_scale=boiling_scale)
		song_url = media.get_song_url(boiling_scale, region, locale)
		return audio(response).play(song_url, offset=0)
	else:  # user shouldn't be here, something went wrong
		response = interaction_model.get_response('error', locale)

	return question(response).reprompt(reprompt)


@ask.intent('AMAZON.NoIntent')
def no_intent():

	locale = get_locale()
	alexa_id = session.user.userId
	state = session.attributes.get('state', '')
	reprompt = interaction_model.get_response('reprompt', locale)

	if state == 'might_set_default':
		db.set_block_preference(alexa_id)
		response = interaction_model.get_response('dont_set_default', locale)
	else:  # something went wrong, ask for boiling scale again
		logger.warning("User is not where he should be. alexa_id=%s", alexa_id)
		response = interaction_model.get_response('error', locale)

	return question(response).reprompt(reprompt)


@ask.intent('AMAZON.PauseIntent')
def pause_intent():
	response = interaction_model.get_response('audio_pause', locale=get_locale())
	return audio(response).stop()


@ask.intent('AMAZON.ResumeIntent')
def resume_intent():
	response = interaction_model.get_response('audio_continue', locale=get_locale())
	return audio(response).resume()


@ask.intent('AMAZON.StopIntent')
def stop_intent():
	response = interaction_model.get_response('stop', locale=get_locale())
	return audio(response).clear_queue(stop=True)


@ask.intent('AMAZON.CancelIntent')
def cancel_intent():
	response = interaction_model.get_response('stop', locale=get_locale())
	return audio(response).clear_queue(stop=True)


@ask.intent('AMAZON.HelpIntent')
def help_intent():
	locale = get_locale()
	response = interaction_model.get_response('help', locale)
	reprompt = interaction_model.get_response('reprompt', locale)
	return question(response).reprompt(reprompt)


@ask.intent('AMAZON.RepeatIntent')
def repeat_intent():
	response = interaction_model.get_response('restart', locale=get_locale())
	return statement(response)


@ask.intent('AMAZON.NextIntent')
def next_intent():
	response = interaction_model.get_response('audio_next', locale=get_locale())
	return audio(response).resume()


if __name__ == '__main__':
	# print(app.config)
	app.run()
