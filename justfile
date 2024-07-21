build:
    python main.py

clean:
    rm -rf dist

dist:
    python main.py -p

watch:
    python watch.py

default:
    just build
