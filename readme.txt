python -m venv venv  
.\venv\Scripts\activate     
pip3 freeze 
venv --version
pip3 install "fastapi[all]"

uvicorn main:app 
uvicorn app.main:app --reload

pip3 install psycopg2  
pip install sqlalchemy

pip install "passlib[bcrypt]"  

pip install "python-jose[cryptography]"      


-- install db integration tool
pip install alembic

alembic init alembic 
alembic revision --autogenerate -m "auto"
alembic history 
alembic upgrade head

alembic revision --autogenerate -m "auto - votes"

pip freeze > requirement.txt
