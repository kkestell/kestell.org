import argparse
from pathlib import Path
from flask import Flask, send_from_directory, abort

def create_app(output_dir: Path) -> Flask:
    app = Flask(__name__, static_folder=output_dir)

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_file(path: str):
        requested_path = Path(app.static_folder) / path
        if requested_path.is_dir():
            path = f"{path}/index.html"
        if (Path(app.static_folder) / path).exists():
            return send_from_directory(app.static_folder, path)
        else:
            abort(404)

    return app

def start_server(app: Flask, port: int):
    app.run(port=port, use_reloader=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask Static File Server")
    parser.add_argument("-o", "--output", default="./dist/", help="Output directory path")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port to run the server on")

    args = parser.parse_args()

    output_dir = Path(args.output).resolve()

    app = create_app(output_dir)
    start_server(app, args.port)
