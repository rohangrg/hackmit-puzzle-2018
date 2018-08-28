from hackgps import app
from hackgps.values import ProductionConfig as config

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=config.PORT,
        debug=config.DEBUG
    )