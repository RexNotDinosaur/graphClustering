# graphClustering
A little tool of python to divide graphs into regions through clustering

tool requirement:
                  multiprocessing
                  cv2
                  threading
                  numpy
                  PIL if you want to use the image type convertion function
performance:
                  linear time to the number of points in the image
                  employed multi-processing
                  performance requires more improvement:
                              i.e.: the function needs around 30 seconds to
                                    process a 353*546 image of approximately
                                    40 clusters (US map is used to conduct the
                                    test on 4-core i7 processor Mac pro 15
                                    inch)

update in need:
                  faster algorithm of cluster diffusion from central point, attemp
                         on multi-processor is failed
                  providing an algorithm to compress the image data so to linearly
                         improve performance