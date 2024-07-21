build:
    python main.py

clean:
    rm -rf dist

dist:
    python src/builder/build.py -p

watch:
    python watch.py

default:
    just build
