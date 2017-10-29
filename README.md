# Generic Prometheus "Check" for DataDog Agent
This ["agent check"](https://docs.datadoghq.com/guides/agent_checks/) allows you
to pull arbitrary Prometheus metrics from your DataDog agent.

## Installation
Copy prometheus.py into your dd-agent's `checks.d` directory and create a
`prometheus.yaml` config file in `conf.d`. See the [DataDog
docs](https://docs.datadoghq.com/guides/agent_checks/#directory-structure) for
more details.

## Configuration
Since the number of available custom metrics with DataDog is very low (100-200
per host, depending on your plan), it's possible to filter what metrics to
ingest.

This config will scrape the Prometheus Node Exporter and push only `node_cpu.*`
and `node_memory.*` to DataDog:

```
init_config:

instances:
  - prometheus_endpoint: http://localhost:9100/metrics
    config:
      drop:
        - .*
      keep:
        - node_cpu.*
        - node_memory.*
```

You can also specify headers e.g for authentication. To avoid repeating the
same drops/keeps, you can use [YAML
Anchors](https://en.wikipedia.org/wiki/YAML#Advanced_components). This example
uses both to scape [Latency.at](https://latency.at) Probes and push these
metrics to DataDog:

```
init_config:
  
instances:
  - target: https://sfo1.do.mon.latency.at/probe?target=https://latency.at
    config: &config
      headers: &headers
        Authorization: "Bearer token"
      drop:
        - probe_.*
      keep:
        - probe_http_.*
  - target: https://nyc1.do.mon.latency.at/probe?target=https://latency.at
    config: *config
  - target: https://fra1.do.mon.latency.at/probe?target=https://latency.at
    config: *config
  - target: https://sgp1.do.mon.latency.at/probe?target=https://latency.at
    config: *config
```
