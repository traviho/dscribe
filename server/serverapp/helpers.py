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

from django.contrib.auth.models import User, Group
from .models import Profile, Meeting, Attendee, Sentence

def pipeline(speech_file):
    '''

    speech_client = speech.SpeechClient()
    language_client = language.LanguageServiceClient()

    ###########################
    ### read the audio file ###
    ###########################

    # speech_file = 'voice.flac'
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    ###########################################
    ### annotate sentences with punctuation ###
    ###########################################

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

    '''

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

    for name in names:  # for every owner in the meeting
        owner = name[0]
        first_name = name[1]

        profile = Profile.objects.filter(first_name=first_name)
        attendee = Attendee.objects.create(profile=profile.id,
                                           meeting=meeting.id,
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
            'num_questions': 0
        }
        attendee_sentences = filter(lambda x: x[1] == owner, labeled_sentences)
        for attendee_sentence in attendee_sentences:
            no_punc = re.sub(r'[^\w\s]','', sentence)  # strip punctuation
            num_words = len(no_punc.split(" "))
            key_words = [word for word in no_punc.split(" ") if word not in stopwords.words('english')]

            attendee_data['text'] = attendee_data['text'] + " " + attendee_sentence
            attendee_data['key_text'] = attendee_data['key_text'] + key_words

            meeting_data['text'] = meeting_data['text'] + " " + attendee_sentence
            meeting_data['key_text'] = meeting_data['key_text'] + key_words

            #####################################
            ### sentiment analysis (sentence) ###
            #####################################

            content = attendee_sentence
            if isinstance(content, six.binary_type):
                content = content.decode('utf-8')

            type_ = enums.Document.Type.PLAIN_TEXT
            document = {'type': type_, 'content': content}

            response = client.analyze_sentiment(document)
            sentiment = response.document_sentiment

            last_char = attendee_sentence[-1]
            is_question = (last_char == "?")
            if (is_question):
                attendee_data['num_questions'] += 1
                meeting_data['num_questions'] += 1

            sentence = Sentence.objects.create(attendee=attendee.id,
                                               text=attendee_sentence,
                                               key_text=' '.join(word for word in key_words),
                                               word_count=num_words,
                                               key_word_count=len(key_words),
                                               sentiment_score=sentiment.score,
                                               sentiment_magnitude=sentiment.magnitude,
                                               question=is_question)

        attendee.text = attendee_data['text']
        attendee.key_text = ' '.join(word for word in attendee_data['key_text'])
        attendee.word_count = len(re.sub(r'[^\w\s]','', attendee_data['text']))
        attendee.key_word_count = len(attendee_data['key_text'])

        #####################################
        ### sentiment analysis (attendee) ###
        #####################################

        content = attendee_data['text']
        if isinstance(content, six.binary_type):
            content = content.decode('utf-8')

        type_ = enums.Document.Type.PLAIN_TEXT
        document = {'type': type_, 'content': content}

        response = client.analyze_sentiment(document)
        attendee_sentiment = response.document_sentiment

        attendee.sentiment_score = attendee_sentiment.score
        attendee.sentiment_magnitude = attendee_sentiment.magnitude
        attendee.num_questions = attendee_data['num_questions']

        attendee.save()

        #################################
        ### topic modeling (attendee) ###
        #################################

        text = attendee_data['text']
        if isinstance(text, six.binary_type):
            text = text.decode('utf-8')

        document = types.Document(
            content=text.encode('utf-8'),
            type=enums.Document.Type.PLAIN_TEXT)

        categories = client.classify_text(document).categories

        for category in categories:
            print(u'=' * 20)
            print(u'{:<16}: {}'.format('name', category.name))
            print(u'{:<16}: {}'.format('confidence', category.confidence))

        # TODO: need to decide on whether to store topics

    meeting.text = meeting_data['text']
    meeting.key_text = ' '.join(word for word in meeting_data['key_text'])
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

    response = client.analyze_sentiment(document)
    meeting_sentiment = response.document_sentiment

    meeting.sentiment_score = meeting_sentiment.score
    meeting.sentiment_magnitude = meeting_sentiment.magnitude
    meeting.num_questions = meeting_data['num_questions']

    meeting.save()
