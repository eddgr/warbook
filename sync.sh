set -e

cd $(dirname "$0")

if [ ! -d 'py.ve' ]; then
    python3 -m venv py.ve

    source py.ve/bin/activate

    pip install -r requirements.txt
fi

source py.ve/bin/activate

source env_vars.sh

python app.py sync_s3 rawbook.csv

python app.py sync_s3 warbook.md

echo "Warbook synced"

deactivate
