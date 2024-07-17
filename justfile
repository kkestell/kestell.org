build:
    python main.py

dist:
    rm -rf dist
    python main.py -f -p

serve:
    python -m http.server --directory dist &

watch:
    python watch.py

default:
    just build
