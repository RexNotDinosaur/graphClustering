# graphClustering
A little tool of python to divide graphs into regions through clustering.

Package requirement:
                  multiprocessing;
                  cv2;
                  threading;
                  numpy;
                  PIL if image type convertion function is used;
                  
Performance:
                  linear time to the number of points in the image;
                  employed multiprocessing;
                  performance requires more improvement:
                              i.e.: the function needs around 30 seconds to
                                    process a 353*546 image of approximately
                                    40 clusters (US map is used to conduct the
                                    test on 4-core i7 processor Mac pro 15
                                    inch);

Possible update plans:
                  faster algorithm of cluster diffusion from central point, previous
                         attemp on multiprocessing is failed due to failure to overcome
                         the performance loss of process initiating and communication;
                  providing an algorithm to compress the image data as to linearly
                         improve performance;
                  re-write some key computationally intense tasks in faster languages
                          like C, C++;
                  finding a solution to the technical flaw that the algorithm does not
                          recognize dotted lines as boundary, image may require additional
                          prior processing;
                          

Little Note: the function finding the gradient is named as fast because it has been improved 
             with multiprocessing
                
