from flask import Flask

app = Flask(__name__)

# Define routes here
@app.route('/')
def home():
    
    
    
    return "Hellontuklsjlkgjslkdjglkdfjglkdjflgkjdflkgjfekl', World!"

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)