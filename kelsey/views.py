from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants



class Q(Page):
    form_model = models.Player

    def get_form_fields(self):
        return [i['qname'] for i in Constants.questions
                if i['treatment'] == self.player.treatment]


class QResults(Page):
    def vars_for_template(self):
        curquestions = [i for i in Constants.questions
                        if i['treatment'] == self.player.treatment]
        fields_to_get = [i['qname'] for i in curquestions]
        results = [getattr(self.player, f) for f in fields_to_get]
        qtexts = [i['verbose'] for i in curquestions]
        qsolutions = [i['correct'] for i in curquestions]
        is_correct = [True if i[0] == i[1] else False for i in zip(results,
                                                                   qsolutions)]
        data = zip(qtexts, results,  qsolutions, is_correct)
        return {'data': data}


page_sequence = [
    Q,
    QResults,
]
