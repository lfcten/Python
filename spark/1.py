from pyspark.ml.linalg import Vector, Vectors
from pyspark.ml.feature import HashingTF,Tokenizer

from pyspark.sql import Row

from pyspark import SparkContext
sc = SparkContext("local", "Simple App")
def f(x):
    rel = {}
    rel['features']  = Vectors.dense(float(x[0]),float(x[1]),float(x[2]),float(x[3]))
    rel['label'] = str(x[4])
    return rel


data = sc.textFile(name='iris.csv').map(lambda line: line.split(',')).map(lambda p: Row(**f(p))).toDF()