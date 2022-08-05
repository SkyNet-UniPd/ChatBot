import imp
import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ListTrainer
from chatterbot.conversation import Statement
from chatterbot.trainers import ChatterBotCorpusTrainer

from chat.settings import BASE_DIR

import logging

logging.basicConfig(level=logging.CRITICAL)


def ChatterBotTraining(self):
    """
    Provide training for ChatterBot.
    """
    
    trainer = ListTrainer(self)
    trainer.train('chatterbot.corpus.italian')

    #UC1
    trainer.train([
        "Ciao, sono -nome- ed è il mio primo giorno di lavoro",
        "Ciao, piacere di conoscerti! Potrei sembrare indiscreto, mi daresti la tua email?",
        "-email-",
        "Grazie, procedo subito con il login!",
    ])

    #UC1
    trainer.train([
        "Ciao",
        "Benvenuto, chi sei?",
        "Sono -nome-, di Imola informatica",
        "è un piacere conoscerti -nome-!",
        "Il piacere è mio",
        "Potresti gentilmente fornirmi la tua email così faccio il login?",
        "Certo, -email-",
        "Ottimo, sono ufficialmente il tuo assistente!",
    ])

    #UC2    
    trainer.train([
        "Ciao, sono arrivato in sede",
        "Ciao, in quale sede ti trovi?",
        "Mi trovo nella sede di Imola",
        "Check in effettuato nella sede di Imola. Buon lavoro!",
        "Grazie",
    ])

    #UC2
    trainer.train([
        "Ciao, sono arrivato in sede",
        "Ciao, in quale sede ti trovi?",
        "Mi trovo nella sede di Bologna",
        "Check in effettuato nella sede di Bologna. Buon lavoro!",
        "Grazie",
    ])
    
    #UC2
    trainer.train([
        "Ciao, vorrei effettuare il check in",
        "Ciao, in quale sede desideri fare il check in?",
        "Desidero fare il check in nella sede di Bologna, grazie",
        "Check in effettuato nella sede di Bologna. Buon lavoro!",
        "Grazie!",
    ])

    #UC2
    trainer.train([
        "Ciao, vorrei effettuare il check in",
        "Ciao, in quale sede desideri fare il check in?",
        "Desidero fare il check in nella sede di Imola, grazie",
        "Check in effettuato nella sede di Imola. Buon lavoro!",
        "Grazie!",
    ])

    #UC2
    trainer.train([
        "Ciao, sto andando via",
        "Ciao, da quale sede te ne stai andando?",
        "Sto andando via dalla sede di Imola",
        "Check out effettuato per la sede di Imola. Buona Giornata!",
        "Grazie!",
    ])

    #UC2
    trainer.train([
        "Ciao, sto andando via",
        "Ciao, da quale sede te ne stai andando?",
        "Sto andando via dalla sede di Bologna",
        "Check out effettuato per la sede di Bologna. Buona Giornata!",
        "Grazie!",
    ])

    #UC2
    trainer.train([
        "Ciao, vorrei fare il check out",
        "Ciao, per quale sede vuoi fare il check out?",
        "Voglio fare il check out per la sede di Imola",
        "Check out effettuato per la sede di Imola. Buona Giornata!",
        "Grazie!",
    ])

    #UC2
    trainer.train([
        "Ciao, vorrei fare il check out",
        "Ciao, per quale sede vuoi fare il check out?",
        "Voglio fare il check out per la sede di Bologna",
        "Check out effettuato per la sede di Bologna. Buona Giornata!",
        "Grazie!",
    ])

    #UC3
    with open(BASE_DIR / "chat/Dataset_attivita.txt") as f:
        conversation = f.readlines()
        trainer.train(conversation)

    #UC4
    trainer.train([
        "Ciao, vorrei aprire il cancello",
        "Ciao, per quale sede vuoi aprire il cancello?",
        "Voglio aprire il cancello della sede di Bologna",
        "Cancello aperto. Benvenuto!",
    ])

    #UC4
    trainer.train([
        "Ciao, vorrei aprire il cancello",
        "Ciao, per quale sede vuoi aprire il cancello?",
        "Voglio aprire il cancello della sede di Imola",
        "Cancello aperto. Benvenuto!",
    ])
    
    #UC5
    trainer.train([
        "Ciao, voglio creare una nuova riunione su Zoom",
        "Ciao, per che giorno vuoi creare la riunione?",
        "Voglio creare la riunione per mercoledì 2 aprile",
        "Per che ora vuoi che inizi la riunione?",
        "Voglio iniziare la riunione alle 16",
        "A che ora vuoi che finisca la riunione?",
        "Voglio finire la riunione alle 17",
        "Ho creato una nuova riunione per mercoledì 2 aprile dalle 16 alle 17, ecco il link Zoom",
    ])

    #UC5
    trainer.train([
        "Hola",
        "Hei, che piacere risentirti! In cosa posso rendermi utile?",
        "Mi fissi una riunione?",
        "Certo, chi posso invitare?",
        "Il gruppo universitario SkyNet",
        "Per che ora la fisso?",
        "Per domani alle 16:00",
        "La farete in sede oppure online?",
        "In sede",
        "Ottimo, ho inviato la riunione!",
        "Grazie mille",
        "Grazie a te!",
    ])

    #UC6
    trainer.train([
        "Ciao, mi servirebbe un documento",
        "Ciao, indicami cosa stai cercando",
        "Vorrei l'analisi dei requisiti di skynet",
        "Provo a cercarlo subito!",
    ])

    #UC7
    trainer.train([
        "Ciao, non mi funziona lo schermo",
        "Ciao, se vuoi posso procedere con l'apertura di un ticket",
        "Si grazie",
        "Ok, ho inviato la segnalazione",
    ])

    #UC7
    trainer.train([
        "Ciao, ho problemi con il telefono",
        "Ciao, se vuoi posso procedere con l'apertura di un ticket",
        "Si grazie",
        "Ok, ho inviato la segnalazione",
    ])

    #UC8
    trainer.train([
        "Ciao, vorrei eseguire il logout",
        "Ciao, -nome- mi dispiace te ne vada! \
        Ho provveduto a fare il logout, ti auguro il meglio e spero di rivederti presto, è stato un piacere lavorare con te!",
    ])

    # #UC9
    # with open(BASE_DIR / "chat/Dataset_misto.txt") as f:
    #     conversation = f.readlines()
    #     trainer.train(conversation)
