from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig

class AgendadorConfig(AppConfig):
    name = 'agendador'

    # Inicializa o agendador quando o app Django estiver pronto.
    def ready(self):
        from monitoramento.buscador import buscar_cotacoes_e_salvar 

        scheduler = BackgroundScheduler()
        scheduler.add_job(buscar_cotacoes_e_salvar, 'interval', minutes=1)
        scheduler.start()
