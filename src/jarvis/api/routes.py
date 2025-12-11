"""Flask API Routes"""
from flask import jsonify, request
from datetime import datetime
from jarvis.api.gemini_client import process_prompt, is_api_configured


def register_routes(app):
    """Register all API routes with the Flask app"""
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        """Handle chat API requests"""
        try:
            data = request.json
            prompt = data.get('message', '')
            
            if not is_api_configured():
                return jsonify({
                    'success': False,
                    'error': 'API key not configured. Please set GEMINI_API_KEY environment variable.'
                }), 400
            
            if not prompt:
                return jsonify({
                    'success': False,
                    'error': 'Message cannot be empty'
                }), 400
            
            # Generate response
            response_text = process_prompt(prompt)
            
            return jsonify({
                'success': True,
                'response': response_text,
                'timestamp': datetime.now().isoformat()
            })
        
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'api_configured': is_api_configured()
        })


