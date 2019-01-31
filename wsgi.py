from hatchet.app import create_app


app = create_app(env='test')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
