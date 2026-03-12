from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)
    
    # Initialize DB (if strictly needed on app start)
    from database.connection import init_db
    init_db(app.config['DATABASE_URI'])

    # Register Blueprints
    from api.voice_routes import voice_bp
    from api.transcript_routes import transcript_bp
    from api.summary_routes import summary_bp
    
    app.register_blueprint(voice_bp, url_prefix='/voice')
    app.register_blueprint(transcript_bp, url_prefix='/transcript')
    app.register_blueprint(summary_bp, url_prefix='/summary')

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "status": "Voice Agent API Running",
            "endpoints": ["/health", "/voice", "/transcript", "/summary"]
        }), 200

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001)
