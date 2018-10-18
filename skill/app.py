# -*- coding: utf-8 -*-

import os
import logging.config
from flask import Flask
from flask_ask import Ask, statement, question, session, audio, request

from skill.audio import AudioLoader
from skill.speech import SpeechLoader
from skill.loggingconf import logging_config


env = os.environ.get('ENVIRONMENT')

logging.config.dictConfig(logging_config)
logger = logging.getLogger(env)

app = Flask(__name__)
ask = Ask(app, "/")


@app.route('/test')
def activity_test():
	return "It's an eggciting world!"


@ask.launch
def welcome_message():
	speech = SpeechLoader(request)
	response = speech.get_response('welcome')
	reprompt = speech.get_response('reprompt')
	return question(response).reprompt(reprompt)


@ask.intent('SetBoilingScaleIntent', convert={'boiling_scale': str})
def set_timer_intent(boiling_scale):

	speech = SpeechLoader(request)

	if isinstance(boiling_scale, str):
		boiling_scale = boiling_scale.lower()

	if boiling_scale not in ['soft', 'medium', 'hard', 'weich', 'mittel', 'hart']:
		response = speech.get_response('error_boiling_scale')
		reprompt = speech.get_response('reprompt')
		return question(response).reprompt(reprompt)

	session.attributes['boiling_scale'] = boiling_scale

	response = speech.get_response('start_timer', boiling_scale=boiling_scale)
	song_library = AudioLoader(request)
	song_url = song_library.get_song_url(boiling_scale)

	return audio(response).play(song_url, offset=0)


@ask.intent('AMAZON.PauseIntent')
def pause_intent():
	speech = SpeechLoader(request)
	response = speech.get_response('audio_pause')
	return audio(response).stop()


@ask.intent('AMAZON.ResumeIntent')
def resume_intent():
	speech = SpeechLoader(request)
	response = speech.get_response('audio_continue')
	return audio(response).resume()


@ask.intent('AMAZON.StopIntent')
def stop_intent():
	speech = SpeechLoader(request)
	response = speech.get_response('stop')
	return audio(response).clear_queue(stop=True)


@ask.intent('AMAZON.CancelIntent')
def cancel_intent():
	speech = SpeechLoader(request)
	response = speech.get_response('stop')
	return audio(response).clear_queue(stop=True)


@ask.intent('AMAZON.HelpIntent')
def help_intent():
	speech = SpeechLoader(request)
	response = speech.get_response('help')
	reprompt = speech.get_response('reprompt')
	return question(response).reprompt(reprompt)


@ask.intent('AMAZON.RepeatIntent')
def repeat_intent():
	speech = SpeechLoader(request)
	response = speech.get_response('restart')
	return statement(response)


@ask.intent('AMAZON.NextIntent')
def next_intent():
	speech = SpeechLoader(request)
	response = speech.get_response('audio_next')
	return audio(response).resume()


if __name__ == '__main__':
	# print(app.config)
	app.run()
