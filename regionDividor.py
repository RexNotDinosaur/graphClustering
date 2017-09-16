import cv2
import math
from Cluster import Cluster
import random
import threading
from utils import norm,innerproduct,diff,countingThreading
from fastGradient import fastGradDic,imageDic




def isboundpoint(gradDic:dict,p:tuple,decreasingcoefficient:float,displacement:int)->bool:
    __doc__ = '''
    :param gradDic: the dictionary of gradient of colors with position tuples as key
    :param p: position that is to be judeged
    :param decreasingcoefficient: decreasingcoefficient measures how loose our standard is to regard a point as boundary
                                  point, empirically, recommended to be 6-30
    :param displacement: the radius of points taking effect when calculating the gradient, used to calculated weight
    :return: Boolean whether the point is a boundary point
    '''
    threshold = 0
    for dis in range(-1 * displacement, displacement + 1):
        if dis != 0:
            threshold = threshold + abs(1 / dis)
    threshold = threshold / (2 * displacement)
    threshold = threshold * 255 *3 / decreasingcoefficient
    return norm(gradDic[p])>=threshold

def graddiffuse(imgdic: dict, gradientdic: dict, shape: tuple, leftbehindportion=0.1, displacement=3,
                decreasingcoefficient=8) -> list:
    __doc__ = '''
    :param imgdic: dictionary of image colors with position tuple as key
    :param gradientdic: dictionary of image color gradient with position tuple as key
    :param shape: tuple of rows and columns of the image
    :param leftbehindportion: portion of points that we can ignore when judging whether we have found all the clusters
    :param displacement: the radius of points taking effect when calculating the gradient, used to calculated weight
    :param decreasingcoefficient: decreasingcoefficient measures how loose our standard is to regard a point as boundary
                                  point, empirically, recommended to be 6-30
    :return: list of Clusters in the graph indicated by the imgdic
    '''

    rows,cols=shape
    totalpoints=rows*cols

    finalclusters=[]
    times=0
    while float(len(imgdic.keys()))>=leftbehindportion*totalpoints:
        finalclusters.append(
            singlediffuse(random.choice(list(imgdic.keys())), gradientdic, decreasingcoefficient, displacement))
        for p in finalclusters[len(finalclusters)-1].pointset:
            try:
                imgdic.pop(p)
            except KeyError:
                if times==0:
                    print('not necessary')
                    times+=1

    return finalclusters






def xor(b1:bool,b2:bool)->bool:
    __doc__ = '''

    :param b1: boolean one
    :param b2: boolean two
    :return: function of xor which corresponds to the table below
                b1      b2      xor(b1,b2)
                True    True    True
                True    False   False
                False   True    False
                False   False   True
    '''
    if b1 and b2:
        return True
    elif not b1 and not b2:
        return True
    else:
        return False

def singlediffuse(centralp:tuple,gradientdic:dict,decreasingcoefficient:float,displacement:int)->Cluster:
    __doc__='''

    :param centralp: the point coordinate tuple that the cluster diffusing process start from
    :param gradientdic: dictionary of gradient with key of position
    :param decreasingcoefficient: decreasingcoefficient measures how loose our standard is to regard a point as boundary
                                  point, suggested to be 6-30
    :param displacement:the radius of points taking effect when calculating the gradient, used to calculated weight
    :return: a Cluster of points of the same kind of which contains point located at centralp
    '''
    cluster=Cluster([centralp])
    pointqueue=[centralp]
    while len(pointqueue)>0:
        r,c=pointqueue.pop(0)
        for dr in range(-1,2):
            for dc in range(-1,2):
                if dr!=0 or dc!=0:
                    try:
                        if xor(isboundpoint(gradientdic, (r + dr, c + dc), decreasingcoefficient, displacement),
                               isboundpoint(gradientdic, (r, c), decreasingcoefficient, displacement)):
                            added=cluster.addpoint((r+dr,c+dc))
                            if added:
                                pointqueue.append((r+dr,c+dc))

                    except KeyError:
                        pass
    return cluster



def perpendicular(a:tuple,b:tuple,anglethreshold:float)->bool:
    __doc__ = '''
    precondition: 0<=anglethreshold<=90, the norm of a and b are not zero
    :param a: vector to be compared
    :param b: vector to be compared
    :param anglethreshold: the angle in degrees that can be accepted as a deviation from 90 degrees
    :return: whether or not the two vectors are perpendicular
    >>> perpendicular((5,5),(5,-5),5)
    True
    >>>perpendicular((1,1),(3,3),5)
    False
    '''

    x,y=a
    u,v=b
    uniformouter=(x*v-u*y)/(norm(a)*norm(b))
    return abs(uniformouter)>=math.sin(math.pi*(90-anglethreshold)/180)





if __name__=='__main__':
    # this is a demo on how to do clustering with the function provided above, you might want to change the file names
    # and paramters
    fn = '/Users/Rex/Desktop/temppic/38.png'
    leftbehindportion = 0.1
    displacement = 3
    decreasingcoefficient = 8

    continuelist = [True]
    counting=countingThreading(dt=5,continuelist=continuelist)
    counting.start()

    imgdic,rows,cols=imageDic(fn)

    print('imgdic')
    graddic=fastGradDic(imgdic,(rows,cols),displacement)
    print('graddic')

    clusters=graddiffuse(imgdic,graddic,(rows,cols),leftbehindportion,displacement,decreasingcoefficient)

    L=threading.Lock()
    L.acquire()
    continuelist[0]=False
    L.release()
    counting.join()

    img = cv2.imread(fn, cv2.IMREAD_COLOR)

    for cluster in clusters:
        color=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
        for p in cluster.pointset:
            try:
                img[p]=color
            except IndexError:
                print(p)

    cv2.imwrite('temp.png', img)


