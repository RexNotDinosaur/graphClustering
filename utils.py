from numpy import ndarray
import math
import time
import threading
import os
from PIL import Image
import random

def countingThreading(dt,continuelist):
    __doc__ = '''
    :param dt: the time unit of measuring time
    :param continuelist: a list that indicates whether to continue, can be modified from outside to force a quit, has
                         only one bool element with True to continue and False to stop
                         (this probably is not a good idea as queue, it will be updated later to use queue instead)
    :return: thread counting down time separately as the program proceeds
    '''
    def counting(dt,continuelist):
        start=time.time()
        lastspan=0
        while continuelist[0]:
            time.sleep(dt)
            now=time.time()
            if float(now-start)>lastspan:
                lastspan=float(now-start)
                print(lastspan)
        print('final time',time.time()-start)
    return threading.Thread(target=counting,args=(dt,continuelist),daemon=True)


def uniform(u):
    __doc__ = '''
    :param u: any vector expressed in the form of iterable with inner product and scalar multiplication defined
    :return: the uniform vector of the direction of u
    '''
    return multi(1/norm(u),u)

def diff(a,b):
    __doc__ = '''
    precondition: a, b has same length, or OVerflowError will be raised
    :param a: a vector expressed in the form of iterable
    :param b: another vector expressed in the form of iterable
    :return: the vector difference a-b expressed in tuple
    '''
    if not isinstance(a,(set,list,ndarray,tuple)):
        return float(a)-float(b)
    else:
        if len(a)!=len(b):
            print(a)
            print(b)
            raise OverflowError('two vectors performing difference not in same dimension')
        else:
            result=[]
            for i in range(0,len(a)):
                result.append(diff(a[i],b[i]))
            return tuple(result)
def multi(c,V):
    __doc__ = '''
    :param c: scalar
    :param V: vector expressed in form of iterable
    :return: result of scalar multiplication expressed in tuple
    '''
    if not isinstance(V,(list,set,ndarray,tuple)):
        try:
            return float(c)*float(V)
        except Exception as e:
            print(type(c),type(V))
            raise e
    else:
        result = []
        for i in range(0, len(V)):
            result.append(multi(c,V[i]))
        return tuple(result)
def add(a,b):
    __doc__ = '''
    precondition: a, b has same length, or OVerflowError will be raised
    :param a: a vector expressed in the form of iterable
    :param b: another vector expressed in the form of iterable
    :return: the vector addition result expressed in the form of tuple
    '''
    return diff(a,multi(-1,b))

def innerproduct(a,b):
    __doc__ = '''
    precondition: a, b has same length, or OVerflowError will be raised
    :param a: a vector expressed in the form of iterable
    :param b: another vector expressed in the form of iterable
    :return: the inner product of a and b, if defined
    '''
    if not isinstance(a,(list,set,ndarray,tuple)):

        return float(a)*float(b)


    else:
        if len(a)!=len(b):
            raise OverflowError('two vectors performing inner product not in same dimension')
        inner=0
        for i in range(0,len(a)):
            inner+=innerproduct(a[i],b[i])
        return inner
def norm(a):
    __doc__ = '''
    :param a: vector expressed in the form of iterable
    :return: the norm of a
    '''
    return math.sqrt(innerproduct(a,a))

def linearcombination(a,b,ca=1,cb=1):
    __doc__ = '''
    precondition: a, b has same length, or OVerflowError will be raised
    :param a: vector expressed in the form of iterable
    :param b: vector expressed in the form of iterable
    :param ca: coefficient on vector a
    :param cb: coefficient on vector b
    :return: the linear combination of a,b with corresponding coefficients in the form of tuple
    '''
    return add(multi(ca,a),multi(cb,b))

def crudeImageDicCompression(imgdic:dict,*args,compressionfactor:int):
    __doc__ = '''
    a crude way of compressing image dictionary, suited for very simple images
    :param imgdic: the original image dictionary
    :param args: need to be exactly two piece of data, tuple and unpacked data accepted,
                    i.e you can input rows,cols or (rows,cols) for args as you like
    :param compressionfactor: a factor of compressing the image, note that the image gets
                                smaller in a square factor of compressionfactor
    :return: the compressed image data as a dictionary with position as key
    '''
    try:
        rows,cols=args
    except ValueError:
        shape,=args
        rows,cols=shape
    compresseddic={}
    for r in range(0,rows//compressionfactor,1):
        for c in range(0,cols//compressionfactor,1):
            compresseddic[(r,c)]=imgdic[(r*compressionfactor,c*compressionfactor)]
    return compresseddic,rows//compressionfactor,cols//compressionfactor

def portionImageDicCompression(imgdic:dict,*args,points:int,outof:int)->tuple:
    __doc__ = '''
    :param imgdic: the original image dictionary
    :param args: need to be exactly two piece of data, tuple and unpacked data accepted,
                    i.e you can input rows,cols or (rows,cols) for args as you like
    :param points: how many points you take every a certain number of points, determined by the parameter outof
    :param outof: form the fraction along with points: points/outof
    :return: tuple compressed image dictionary,rows,columns
    '''
    try:
        rows,cols=args
    except ValueError:
        shape,=args
        rows,cols=shape
    if points>outof:
        raise ValueError('Numerator larger than Denominator')
    rowstopick=picknumbers(rows,points,outof)
    colstopick=picknumbers(cols,points,outof)
    rowstopick.sort()
    colstopick.sort()
    compressed={}

    for r in range(0,len(rowstopick)):
        for c in range(0,len(colstopick)):
            compressed[(r,c)]=imgdic[(rowstopick[r],colstopick[c])]
    return compressed,len(rowstopick),len(colstopick)

def picknumbers(upto:int,numerator:int,denominator:int)->list:
    __doc__ = '''
    picking numbers in range(0,upto) following the rule of picking the number of numerator for every the number of 
    denominator of points
    :param upto: upper bound of the number to pick
    :param numerator: the numerator of the fraction
    :param denominator: denominator of the fraction
    :return: list of picked numbers
    '''
    resultlist=[]


    start=0
    while start<upto:
        end=min(start+denominator,upto)

        pointnum=end-start
        if pointnum<=numerator:
            resultlist.extend(range(start,end))
        else:
            resultlist.extend(random.sample(list(range(start,end)),numerator))
        start+=denominator
    return resultlist


# the files have already been converted and the function is not needed for now
def convertGifToPng(path:str):
    __doc__ = '''
    primarily used for test cases, converting all the gif images into Png under the directory of the path
    :param path: the string form of the directory
    '''
    namelist=os.listdir(path)
    for name in namelist:
        if name.endswith('.gif'):
            if path.endswith('/'):
                filename=path+name
            else:
                filename=path+'/'+name
            img = Image.open(filename)
            newname = filename[:filename.index('.')] + '.png'
            img.save(newname)
            os.remove(filename)
