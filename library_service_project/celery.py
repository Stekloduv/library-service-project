from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Вкажіть модуль налаштувань Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_service_project.settings')

app = Celery('library_service_project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

if __name__ == "__main__":
    app.start()
