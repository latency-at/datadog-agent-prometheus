import re
from prometheus import filterMetric, compileRes

class metric:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def toMetrics(samples):
    return list(map(lambda x: { "name": x }, samples))

def test_filter():
    for tc in [
        [ "node_network_receive_multicast", [ ".*" ], [ "foobar" ], False ],
        [ "node_network_receive_multicast", [], [ "foobar" ], True ],
        [ "node_network_receive_multicast", [ ".*" ], [ "node_.*" ], True ],
        [ "node_network_receive_multicast", [ ".*" ], [ "network.*" ], False ],
    ]:
        drops = compileRes(tc[1])
        keeps = compileRes(tc[2])
        assert filterMetric(metric(name=tc[0]), drops, keeps) == tc[3]
