from flask import Flask, render_template, jsonify
import logging
import os
import matplotlib
matplotlib.use('Agg')  # Ensure non-interactive backend

# Import your analytics class
from code_file import TelegramAnalytics

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

# Initialize analytics
analytics = TelegramAnalytics()

@app.route('/')
def index():
    """Main dashboard route"""
    return render_template('index.html')

@app.route('/api/daily_messages')
def daily_messages():
    """API endpoint for daily messages"""
    try:
        # Get daily messages data
        result = analytics.daily_messages_sent()
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error in daily messages: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/most_active_members')
def most_active_members():
    """API endpoint for most active members"""
    try:
        # Get most active members
        result = analytics.most_active_members()
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error in most active members: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/group_growth')
def group_growth():
    """API endpoint for group growth"""
    try:
        # Get group growth data
        result = analytics.group_growth_rate()
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error in group growth: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/dashboard')
def dashboard():
    """Render dashboard template"""
    return render_template('dashboard.html')

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    logging.warning(f"Page not found: {e}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"Internal server error: {e}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    
    # Run the app
    app.run(debug=True)