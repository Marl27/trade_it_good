[ -d "venv" ] && rm -rf venv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
