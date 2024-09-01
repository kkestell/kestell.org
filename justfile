build:
    pdm run python src/builder/build.py

rebuild:
    pdm run python src/builder/build.py -f

clean:
    rm -rf dist

deploy:
    just clean
    just build
    rsync -avz dist/* kkestell_kestell@ssh.nyc1.nearlyfreespeech.net:/home/public/

serve:
    pdm run python src/builder/serve.py

watch:
    pdm run python src/builder/watch.py

default:
    just build
