from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django import forms
import csv
from .renderers import MyCustomRenderer

author = 'Philipp Chapkovski, UZH'

doc = """
    Kelsey-Oliva lottery game
"""


class Constants(BaseConstants):
    name_in_url = 'kelsey'
    players_per_group = None
    num_rounds = 1

    q_parameters = {'initial_cost': 9,
                    'final_cost': 15,
                    'high_payoff': 40,
                    'low_payoff': 8,
                    'PT0ExampleHigh': 16,
                    'PT0ExampleLow': -16,
                    }
    with open('kelsey/qs_to_add.csv') as f:
        questions = list(csv.DictReader(f))
    for q in questions:
        q['verbose'] = q['verbose'].format(
         initial=q_parameters['initial_cost'],
         final=q_parameters['final_cost'],
         hpayoff=q_parameters['high_payoff'],
         lpayoff=q_parameters['low_payoff'],
        )


class Subsession(BaseSubsession):
    def before_session_starts(self):
        self.player_set.update(treatment=self.session.config.get('treatment','T0'))


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.CharField()

for i in Constants.questions:
    Player.add_to_class(i['qname'],
                        models.CharField(verbose_name=i['verbose'],
                        widget=forms.RadioSelect(renderer=MyCustomRenderer,
                        attrs={ 'required': 'true'}),
                        choices=[i['option1'], i['option2']],
                        null=False, blank=False, default=''))
