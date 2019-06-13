#exports test data for prometheus

import json
from minerator_metrics  import MetricExporter

with open('test_input.json', 'r') as f:
    test_data = json.load(f)


def get_data():
    return test_data

m = MetricExporter(port=9091, export_python_metrics=True)
m.parser.get_data = get_data
m.start()



