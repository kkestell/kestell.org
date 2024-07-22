build:
    python main.py

clean:
    rm -rf dist

dist:
    just clean
    python src/builder/build.py -p

watch:
    python src/builder/watch.py

default:
    just build
