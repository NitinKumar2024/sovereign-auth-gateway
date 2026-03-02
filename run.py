from app import create_app

app = create_app()

if __name__ == '__main__':
    # Runs the server on port 5000 with auto-reload enabled
    app.run(debug=True, port=5000)