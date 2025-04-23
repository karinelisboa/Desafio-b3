import os
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig

class AgendadorConfig(AppConfig):
    name = 'agendador'

    def ready(self):
        # Evita que o scheduler rode duas vezes (por causa do autoreload do runserver)
        if os.environ.get('RUN_MAIN', None) != 'true':
            return

        from monitoramento.buscador import buscar_cotacoes_e_salvar 

        scheduler = BackgroundScheduler()
        scheduler.add_job(buscar_cotacoes_e_salvar, 'interval', minutes=1)
        scheduler.start()
