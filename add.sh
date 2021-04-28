set -e

cd $(dirname "$0")

if [ ! -d 'py.ve' ] ; then
    python3 -m venv py.ve

    source py.ve/bin/activate

    pip install -r requirements.txt
fi

source py.ve/bin/activate

python app.py add_entry

echo "Entry added"

deactivate

cd -
