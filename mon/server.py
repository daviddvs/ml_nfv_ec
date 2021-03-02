from flask import render_template
import connexion
import sys, os

# Create the application instance
app = connexion.FlaskApp(__name__, specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('api.yml')

# Create a URL route in our application for "/"
@app.route('/')
def home():

    # Looks at ./templates and don't know how to change
    return render_template('home.html')

# Check models dir
def check_models_dir():
    model_dir = "models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        print("INFO: Directory "+model_dir+" created.")

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    #check_models_dir()
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)