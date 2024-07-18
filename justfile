build:
    python main.py

dist:
    rm -rf dist
    python main.py -f -p

watch:
    python watch.py

default:
    just build
