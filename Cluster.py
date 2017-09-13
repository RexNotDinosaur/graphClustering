from utils import add,multi
class Cluster:

    def __init__(self,pointlist:(list,set)):
        __doc__ = '''
        initializing Cluster
        :param pointlist: iterable iterating points that initially known to exist in the cluster
        '''
        self.pointset=set(pointlist)
    def addpoint(self,RowCol:tuple)->bool:
        __doc__ = '''
        adding point to the Cluster
        :param RowCol: tuple of row and column of the new added point
        :return: return true if the point is a new point and false if the point already exists in the original pointset
        '''
        previouslen=len(self.pointset)
        self.pointset.add(RowCol)
        return len(self.pointset)>previouslen
    def copy(self):
        __doc__ = '''
        copying a self
        :return: a new Cluster exactly the same as self
        '''
        return Cluster(self.pointset)

    def averagepoint(self):
        __doc__ = '''
        precondition: there is at least a point in the Cluster or ZeroDivisionError will be raised
        :return: the average position of self
        '''
        ZERO = 0.0
        avep = (ZERO, ZERO)

        for p in self.pointset:
            try:
                avep = add(avep, p)

            except OverflowError:
                sp = list(p)
                while len(sp) < 2:
                    sp.append(ZERO)
                avep = add(avep, sp)
        avep = multi(1 / len(self.pointset), avep)
        return avep

    def averagecolor(self, imgdic):
        __doc__ = '''
        :param imgdic: dictionary of image colors with position as key
        :return: the average color tuple of the Cluster in the image imgdic corresponding to
        '''
        ZERO = 0.0
        avecolor = (ZERO, ZERO, ZERO)
        for p in self.pointset:
            try:
                c = imgdic[p]
                avecolor = add(avecolor, c)
            except OverflowError:
                sc = list(c)
                while len(sc) < 3:
                    sc.append(ZERO)
                avecolor = add(avecolor, sc)
        avecolor = multi(1 / len(self.pointset), avecolor)
        return avecolor