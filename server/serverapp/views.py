from django.shortcuts import render
import io
import re
import operator
import six

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import numpy as np
import pandas as pd
from nltk.corpus import stopwords
import nltk

from django.contrib.auth.models import User, Group
from .models import Meeting, Attendee, Sentence, Profile

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from serverapp.serializers import UserSerializer, GroupSerializer, MeetingSerializer, AttendeeSerializer, SentenceSerializer
from rest_framework.views import APIView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse

def pipeline(speech_file):
    Meeting.objects.all().delete()
    Attendee.objects.all().delete()
    Sentence.objects.all().delete()

    speech_client = speech.SpeechClient()
    language_client = language.LanguageServiceClient()

    ###########################
    ### read the audio file ###
    ###########################

    content = speech_file.read()

    ###########################################
    ### annotate sentences with punctuation ###
    ###########################################

    nltk.download('stopwords')

    audio = speech.types.RecognitionAudio(content=content)
    punc_config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.FLAC,
        language_code='en-US',
        enable_automatic_punctuation=True)

    punc_response = speech_client.recognize(punc_config, audio)

    sentences = []
    for i, result in enumerate(punc_response.results):
        alternative = result.alternatives[0]
        sentences.append(alternative.transcript)

    ##############################################
    ### annotate words with identified speaker ###
    ##############################################

    n = 3  # number of speakers
    diar_config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.FLAC,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=n)

    diar_response = speech_client.recognize(diar_config, audio)
    result = diar_response.results[-1]
    words_info = result.alternatives[0].words

    words = []
    for word_info in words_info:
        words.append((word_info.word, word_info.speaker_tag))

    ### START DUMMY DATA ###

    sentences = ['Hello, my name is Travis.',
                 'Hello, this is Calvin.',
                 'This is Joe.',
                 'Wow, Joe.',
                 "I know my voice is so sexy, isn't it?",
                 "I have so much sex what is going on?"]
    words = [('hello', 3), ('my', 3), ('name', 3), ('is', 3), ('Travis', 1), ('hello', 1), ('this', 1), ('is', 1), ('Calvin', 1), ('this', 2), ('is', 2), ('Joe', 2), ('wow', 3), ('Joe', 3), ('I', 3), ('know', 3), ('my', 3), ('voice', 3), ('is', 3), ('so', 3), ('sexy', 3), ("isn't", 3), ('it', 3), ('I', 3), ('have', 3), ('so', 3), ('much', 3), ('sex', 3), ('what', 1), ('is', 1), ('going', 1), ('on', 1)]

    ### END DUMMY DATA ###

    start = 0
    labeled_sentences = []
    for sentence in sentences:
        no_punc = re.sub(r'[^\w\s]','', sentence)  # strip punctuation
        num_words = len(no_punc.split(" "))
        ownership = {}

        for i in range(start, start + num_words):  # loop through words of sentence
            owner = words[i][1]
            if owner in ownership.keys():
                ownership[owner] += 1
            else:
                ownership[owner] = 1
        start = start + num_words

        most_likely_owner = max(ownership.items(), key=operator.itemgetter(1))[0]  # find the most frequent owner
        labeled_sentences.append((sentence, most_likely_owner))

    #####################################
    ### find name from first sentence ###
    #####################################

    names = {}
    seen = []
    for labeled_sentence in labeled_sentences:
        text = labeled_sentence[0]
        owner = labeled_sentence[1]

        if owner in seen: continue  # only analyze first sentence
        seen.append(owner)

        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

        entities = language_client.analyze_entities(document).entities

        for entity in entities:
            entity_type = enums.Entity.Type(entity.type)

            if (entity_type.name == "PERSON"):  # entity is person's name
                names[owner] = entity.name

    ####################################
    ### begin entering into database ###
    ####################################

    meeting = Meeting.objects.create(name="Testing",
                                     description="A brief description here.",
                                     text="",
                                     key_text="",
                                     word_count=0,
                                     key_word_count=0,
                                     sentiment_score=0,
                                     sentiment_magnitude=0)
    meeting.save()

    meeting_data = {
        'text': "",
        'key_text': "",
        'num_questions': 0
    }

    ###################################
    ### matching with user profiles ###
    ###################################

    for k, v in names.items():  # for every owner in the meeting
        owner = k
        first_name = v

        profile = Profile.objects.filter(first_name=first_name)[0]
        attendee = Attendee.objects.create(user=profile.user,
                                           meeting=meeting,
                                           text="",
                                           key_text="",
                                           word_count=0,
                                           key_word_count=0,
                                           sentiment_score=0,
                                           sentiment_magnitude=0,
                                           num_questions=0)
        attendee.save()

        attendee_data = {
            'text': "",
            'key_text': "",
            'word_count': 0,
            'key_word_count': 0,
            'num_questions': 0
        }
        attendee_sentences = list(filter(lambda x: x[1] == owner, labeled_sentences))

        for attendee_sentence_i in attendee_sentences:
            attendee_sentence = attendee_sentence_i[0]
            no_punc = re.sub(r'[^\w\s]','', attendee_sentence)  # strip punctuation
            num_words = len(no_punc.split(" "))
            key_words = [word for word in no_punc.split(" ") if word not in stopwords.words('english')]

            attendee_data['text'] = attendee_data['text'] + " " + attendee_sentence
            attendee_data['key_text'] = attendee_data['key_text'] + " " + ' '.join(word for word in key_words)

            meeting_data['text'] = meeting_data['text'] + " " + attendee_sentence
            meeting_data['key_text'] = meeting_data['key_text'] + " " + ' '.join(word for word in key_words)

            #####################################
            ### sentiment analysis (sentence) ###
            #####################################

            content = attendee_sentence
            if isinstance(content, six.binary_type):
                content = content.decode('utf-8')

            type_ = enums.Document.Type.PLAIN_TEXT
            document = {'type': type_, 'content': content}

            response = language_client.analyze_sentiment(document)
            sentiment = response.document_sentiment

            last_char = attendee_sentence[-1]
            is_question = (last_char == "?")
            if (is_question):
                attendee_data['num_questions'] += 1
                meeting_data['num_questions'] += 1

            attendee_data['word_count'] += num_words
            attendee_data['key_word_count'] += len(key_words)

            sentence = Sentence.objects.create(attendee=attendee,
                                               text=attendee_sentence,
                                               key_text=' '.join(word for word in key_words),
                                               word_count=num_words,
                                               key_word_count=len(key_words),
                                               sentiment_score=sentiment.score,
                                               sentiment_magnitude=sentiment.magnitude,
                                               question=is_question,
                                               begin_offset=0)

        attendee.text = attendee_data['text']
        attendee.key_text = attendee_data['key_text']
        attendee.word_count = attendee_data['word_count']
        attendee.key_word_count = attendee_data['key_word_count']

        #####################################
        ### sentiment analysis (attendee) ###
        #####################################

        content = attendee_data['text']
        if isinstance(content, six.binary_type):
            content = content.decode('utf-8')

        type_ = enums.Document.Type.PLAIN_TEXT
        document = {'type': type_, 'content': content}

        response = language_client.analyze_sentiment(document)
        attendee_sentiment = response.document_sentiment

        attendee.sentiment_score = attendee_sentiment.score
        attendee.sentiment_magnitude = attendee_sentiment.magnitude
        attendee.num_questions = attendee_data['num_questions']

        attendee.save()

    meeting.text = meeting_data['text']
    meeting.key_text = meeting_data['key_text']
    meeting.word_count = len(re.sub(r'[^\w\s]','', meeting_data['text']))
    meeting.key_word_count = len(meeting_data['key_text'])

    ####################################
    ### sentiment analysis (meeting) ###
    ####################################

    content = meeting_data['text']
    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = language_client.analyze_sentiment(document)
    meeting_sentiment = response.document_sentiment

    meeting.sentiment_score = meeting_sentiment.score
    meeting.sentiment_magnitude = meeting_sentiment.magnitude
    meeting.num_questions = meeting_data['num_questions']

    meeting.save()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class MeetingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited

    takes in the query meetings=(ids of meetings desired)
    example: localhost:8000/meeting/?meetings=1,2,3

    The way to get the words/text specific to individual attendees given a meeting is to
    take the returned ids of attendees, and then use that to query from localhost:8000/attendee/?insertqueryhere

    A way to get the percentage of words spoken by an attendee is to divide the attendee's total text count by the
    meeting's text count

    ex: i query form localhost:8000/attendee/1,2,3,4 and get the json representing what was said by attendees 1,2,3,4
    for a given meeting

    each attendee has data for how many words they spoke, so that can just be divided by total word counts of the meeting
    """

    serializer_class = MeetingSerializer

    def get_queryset(self):
        queryset = Meeting.objects.all()
        target_meetings = self.request.query_params.get('meetings',None)

        if target_meetings is not None:
            target_meetings = target_meetings.split(',')
            queryset = queryset.filter(pk__in=target_meetings)

        return queryset

class AttendeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows attendees of a meeting to be viewed or edited

    takes in the query user= and meeting=
    example: localhost:8000/attendee/?user=1,2,3&meeting=1,2 will return
    json where foreign keys match 1,2,3 and where foreign key matches 1 and 2

    to mix meetings and different users (i.e user 1 for meeting 1 and user 2 for meeting 2),
    multiple api calls will have to be made. one call for user=1 and meeting=1 and another
    for user=2 and meeting=2


    """

    serializer_class = AttendeeSerializer

    def get_queryset(self):
        queryset = Attendee.objects.all()
        target_user = self.request.query_params.get('user', None)

        target_meeting = self.request.query_params.get('meeting', None)


        if target_user is not None:
            target_user = target_user.split(',')
            queryset = queryset.filter(user__in = target_user)

        if target_meeting is not None:
            target_meeting = target_meeting.split(',')
            queryset = queryset.filter(meeting__in = target_meeting)

        return queryset


class SentenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sentences to be viewed or changed

    queries for attendees
    example: localhost:9000/sentence/?attendee=1,2 will return json
    representing the sentences that have a foreign keys matching with attendees
    1 and 2.
    """

    serializer_class = SentenceSerializer

    def get_queryset(self):
        queryset = Sentence.objects.all()
        target_attendee = self.request.query_params.get('attendee', None)

        if target_attendee is not None:
            target_attendee = target_attendee.split(',')
            queryset = queryset.filter(attendee__in = target_attendee)

        return queryset

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        try:
            pipeline(request.FILES['audio'])
            return HttpResponse(status=204)
        except:
            return HttpResponse(status=400)
    return HttpResponse(status=204)
