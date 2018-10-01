from hatchet.app import create_app


app = create_app(env='dev')
app.run(host='0.0.0.0')
