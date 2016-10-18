# hybridjango
Lag et python virtuelt miljø (virtualenv), med navn venv og plassert i prosjektmappen.

Prosjektet krever for øyeblikket libjpeg-dev installert. (```sudo apt install libjpeg-dev``` **i ubuntu**).

Naviger til prosjektmappen og kjør
```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
Hvis du vil kjøre serveren fra kommandolinjen kan du bruke
```python manage.py runserver```
mens venv er aktivt (skal stå (venv) til venstre) og du er i mappen.
```source venv/bin/activate ``` brukes til å aktivere venv.
