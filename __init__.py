# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from os.path import abspath, join, dirname
from random import choice

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util import wait_while_speaking

from mycroft.util.log import getLogger
LOGGER = getLogger(__name__)

__author__ = 'aussieW'

class KnockKnockJokesSkill(MycroftSkill):
    def __init__(self):
        super(KnockKnockJokesSkill, self).__init__(name="KnockKnockJokesSkill")
        self.jokes = []
        self.joke = None
        self.stage = 0
        self.path_to_joke_file = join(abspath(dirname(__file__)), 'jokes', 'jokes.txt')
		
    def initialize(self):
        # load the jokes from the jokes directory
        with open(self.path_to_joke_file) as f:
            self.jokes.append(f.readline().strip().split(':'))
        LOGGER.info('KnockKnockJokesSkill: Available jokes = ' + str(self.jokes))     

    @intent_handler(IntentBuilder('handle_tell_joke').require('knock-knock').optionally('joke'))
    def handle_tell_joke(self, message):
        LOGGER.info('KnockKnockJokesSkill: handle_tell_joke')
        self.joke = choice(self.jokes)
        self.stage = 1
        self.speak_dialog('knock-knock', expect_response=True)  # expect 'who's there'

#    @intent_handler(IntentBuilder('handle_who_is_there').require('who-is-there'))
    def handle_who_is_there(self, message):
        LOGGER.info('KnockKnockJokesSkill: handle_who_is_there')
        if self.stage == 1:
            self.speak(joke[0], expect_response=True)  # expect 'who'
            self.stage = 2

#    @intent_handler(IntentBuilder('handle_who').require('who'))
    def handle_who(self, message):
        if self.stage == 2:
            self.speak(joke[1])
            self.stage = 0
            self.joke = None

    def converse(self, utterances, lang="en-us"):
        if utterances != None:
            LOGGER.info('KnockKnockJokesSkill: utterance = ' + str(utterances))
            LOGGER.info('KnockKnockJokesSkill: joke = ' + str(self.joke))
            LOGGER.info('KnockKnockJokesSkill: stage = ' + str(self.stage))
            if self.stage == 1 and "who's there" in utterances:
                LOGGER.info('KnockKnockJokesSkill: Processing stage 1')
                self.speak(self.joke[0], expect_response=True)  # expect 'who'
                self.stage = 2
                return True
            if self.stage == 2 and 'who' in utterances[0].split(): 
                self.speak(self.joke[1])
                self.stage = 0
                self.joke = None
                return True
            else:
                return False
        else:
            LOGGER.info('KnockKnockJokesSkill: Received a NULL utterance. Why??')
            return False

    def stop(self):
        self.stage = 0
        self.joke = None

def create_skill():
    return KnockKnockJokesSkill()
