import os

from GuiltySpark.guiltyspark import GuiltySpark

if __name__ == '__main__':
    client = GuiltySpark()

    client.run(os.environ.get('DISCORD_KEY'))
