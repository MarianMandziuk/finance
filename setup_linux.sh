echo 'Setup app'
virtualenv venv -p python3
source venv/bin/activate
git clone https://github.com/MarianMandziuk/finance.git
cd finance
pip install -r requirements.txt
cd fin
python manage.py runserver