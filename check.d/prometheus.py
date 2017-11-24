import re

from checks import CheckException
from checks.prometheus_check import PrometheusCheck

# FIXME: Add leader election
# from utils.kubernetes import KubeUtil
# self.kubeutil.refresh_leader()

def compileRes(regexs):
    if regexs == None:
        return []
    if not isinstance(regexs, list):
        return [re.compile(regexs)]
    return list(map(lambda x: re.compile(x), regexs))

def filterMetric(metric, drops, keeps):
    keep = True
    for regex in drops:
        if regex.match(metric.name):
            keep = False
            break

    # If metric matches drop regex, allow whitelisting it.
    if not keep:
        for regex in keeps:
            if regex.match(metric.name):
                return True
   
    return keep

class GenericCheck(PrometheusCheck):
    """
    Collect optionally filtered, arbitrary Prometheus metric.
    """
    def __init__(self, name, init_config, agentConfig, instances=None):
        super(GenericCheck, self).__init__(name, init_config, agentConfig, instances)
        self.NAMESPACE = self.init_config.get('namespace', 'prometheus')

    def process(self, endpoint, send_histograms_buckets=True, instance=None,
            drops=[], keeps=[], headers={}):

        config = instance.get('config', {})
        drops = compileRes(config.get('drop'))
        keeps = compileRes(config.get('keep'))
        headers = config.get('headers', {})

        content_type, data = self.poll(endpoint, headers=headers)
        for metric in filter(
                lambda m: filterMetric(m, drops, keeps),
                self.parse_metric_family(data, content_type)):
                self._submit_metric(metric.name, metric, send_histograms_buckets,
                        custom_tags=["instance:"+endpoint])

    def check(self, instance):
        endpoint = instance.get('target')
        if endpoint is None:
            raise CheckException("Unable to find target in config file.")

        # By default we send the buckets.
        send_buckets = instance.get('send_histograms_buckets', True)
        if send_buckets is not None and str(send_buckets).lower() == 'false':
            send_buckets = False
        else:
            send_buckets = True

        self.process(endpoint, send_histograms_buckets=send_buckets,
                instance=instance)
