from flask import Flask, render_template

from backend.routes.regioes import bp as regioes_bp
from backend.routes.simulacoes import bp as simulacoes_bp


def create_app(config=None):
    app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
    app.config.update(JSON_SORT_KEYS=False)
    if config:
        app.config.update(config)

    app.register_blueprint(regioes_bp)
    app.register_blueprint(simulacoes_bp)

    @app.get("/")
    def inicio():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
