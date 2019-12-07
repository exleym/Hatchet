from hatchet.app import create_app

#ENV = "dev"
ENV = "dev-stable"


app = create_app(env=ENV)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)
