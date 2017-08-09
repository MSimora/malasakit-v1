"""
This module defines the application's views, which are needed to render pages.

"Pages" are generated in TwiML (Twilio Markup Language) for Twilio to play
desired audio.

See https://www.twilio.com/docs/api/twiml and
https://twilio.github.io/twilio-python/6.5.0/twiml/
"""

import decorator

import random

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.urls import reverse

from twilio.twiml.voice_response import VoiceResponse
# from django_twilio.decorators import twilio_view

from pcari.models import Respondent
from pcari.models import QuantitativeQuestion, QualitativeQuestion
from pcari.models import Comment, CommentRating, QuantitativeQuestionRating
from pcari.models import get_concrete_fields


# Placeholder flow will yank content straight from v1.25 models

@csrf_exempt
def landing(request):
    res = VoiceResponse()

    # REPLACE WITH INTRO INSTRUCTIONS
    res.say("Welcome to Malasakit. Here you will be askd several questions about typhoon preparedness.")
    res.pause(1)
    # need a better way to flag down the first question in the sequence
    res.redirect(reverse('feature_phone:quantitative-questions', args=(1,)))
    return HttpResponse(res)

@csrf_exempt
def quantitative_questions(request, question_id):
    res = VoiceResponse()

    # cast to int
    question_id = int(question_id)

    try:
        # REPLACE WITH INSTRUCTIONS AND AUDIO FROM RECORDING
        question = QuantitativeQuestion.objects.get(id=question_id)
        res.say("Please rate this statement from 0 to 9.")
        res.pause(1)
        res.say(question.prompt)

        # Determine next url- another question? or next phase
        if question_id + 1 in [q.id for q in QuantitativeQuestion.objects.all()]:
            next_url = reverse('feature_phone:quantitative-questions', args=(question_id + 1,))
        else:
            next_url = reverse('feature_phone:rate-comments', args=(0,))

        res.record(max_length=3,timeout=3,action=next_url)
        return HttpResponse(res)
    except ObjectDoesNotExist:
        res.say("ERROR: Question does not exist. Restarting.")
        res.redirect(reverse('feature_phone:landing'))
        return HttpResponse(res)

@csrf_exempt
def process_recording(request, next_url):
    """
    After saving the recording, redirect to the next url.
    Probably want to pass in a newly-created Recording model, and then
    fill in the FileField here.
    """
    res = VoiceResponse()

    # SAVE AUDIO RESPONSE HERE
    res.say("Recording saved.")
    res.redirect(next_url)
    return HttpResponse(res)

@csrf_exempt
def rate_comments(request, num_rated):
    """
    Can the user keep rating? Not sure. Let's assume no for now.
    """
    # cast again
    num_rated = int(num_rated)

    NUM_COMMENTS_TO_RATE = 2

    res = VoiceResponse()

    # REPLACE WITH SAMPLING CODE
    comments = Comment.objects.all()
    comment = comments[random.randint(1, len(comments))]

    res.say("This user made a suggestion. Please rate it from 0 to 9.")
    res.pause(1)
    res.say(comment.message)

    # Determine next url- another comment? or next phase
    if num_rated + 1 == NUM_COMMENTS_TO_RATE:
        next_url = reverse('feature_phone:qualitative-questions', args=(1,))
    else:
        next_url = reverse('feature_phone:rate-comments', args=(num_rated + 1,))

    res.record(max_length=3,timeout=3,action=next_url)
    return HttpResponse(res)

@csrf_exempt
def qualitative_questions(request, question_id):
    res = VoiceResponse()

    # cast to int
    question_id = int(question_id)

    try:
        # REPLACE WITH INSTRUCTIONS AND AUDIO FROM RECORDING
        question = QualitativeQuestion.objects.get(id=question_id)
        res.say("Now it's your turn to offer feedback. Please respond to this question. ")
        res.pause(1)
        res.say(question.prompt)

        # Determine next url- another question? or next phase
        if question_id + 1 in [q.id for q in QualitativeQuestion.objects.all()]:
            next_url = reverse('feature_phone:qualitative-questions', args=(question_id + 1,))
        else:
            next_url = reverse('feature_phone:end')

        res.record(max_length=20,timeout=20,action=next_url)
        return HttpResponse(res)
    except ObjectDoesNotExist:
        res.say("ERROR: Question does not exist. Restarting.")
        res.redirect(reverse('feature_phone:landing'))
        return HttpResponse(res)

@csrf_exempt
def end(request):
    res = VoiceResponse()
    res.say('Thanks for particpating in Malasakit.')
    return HttpResponse(res)
