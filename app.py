import os

import GuiltySpark.guiltyspark

if __name__ == '__main__':
    GuiltySpark.guiltyspark.run(os.environ.get('DISCORD_KEY'))
