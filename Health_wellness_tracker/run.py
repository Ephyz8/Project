import os


if __name__ == "__main__":
    from app import create_app
    app = create_app('prod')
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
