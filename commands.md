

manage.py spectacular --file schema.yml 
pip install -r requirements.txt
pip freeze > requirements.txt
pip install flake8
pip install black
pip install django-mptt
pytest
coverage run -m pytest <!-- pip install coverage -->
coverage html
pytest --cov  <!-- pip install pytest-cov -->
pip install pytest-factoryboy
pip install sqlparse
pip install Pygments
pip install pillow