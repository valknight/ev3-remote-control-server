from server.main import app, generate_code

if __name__ == "__main__":
    generate_code()
    app.run(debug=True, host="0.0.0.0", port=8000)