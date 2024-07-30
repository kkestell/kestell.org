build:
    pdm run python src/builder/build.py -p

clean:
    rm -rf dist

deploy:
    rsync -avz dist/* kkestell_kestell@ssh.nyc1.nearlyfreespeech.net:/home/public/

watch:
    pdm run python src/builder/watch.py

default:
    just build
