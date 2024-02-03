import json
import os
import shutil
from collections import defaultdict
from itertools import product
from queue import SimpleQueue

from pipebro.elems.data_types import DTYPE, iterate_dtypes, ismultiple, DTYPES
from .Process.Concurrent import Concurrent
from .Process.Consumer import Consumer
from .Process.Producer import Producer


def debug_pipes(pipe):
    #pipe.queue_flows
    pass

def draw_pipes_network(pipe, show_queues=True, filename=None):
    pipes_json = {
        'nodes': [],
        'edges': []
    }

    whoproduces = defaultdict(list)
    queue_consumes = defaultdict(lambda: {'list': set([]), 'dtype': None})

    # add process nodes
    for process in pipe.processes:
        if isinstance(process, Producer):
            group = 'producers'
        elif isinstance(process, Consumer):
            group = 'consumers'
        elif isinstance(process, Concurrent):
            group = 'concurrent'
        else:
            group = 'processes'

        pipes_json['nodes'].append({
            'id': process.__PROCESSID__,
            'group': group
        })

        if hasattr(process, 'produces') and process.produces:
            for prod in iterate_dtypes(process.produces):
                whoproduces[prod].append(process.__PROCESSID__)

        # if hasattr(process, 'consumes') and process.consumes:
        #     whoconsumes[process.consumes].append(process.__PROCESSID__)

    skip_queues = set()

    # discover
    dtype: DTYPE; ntos: set
    for dtype, ntos in pipe.queue_flows.items():
        if dtype is None:
            continue

        assert not ismultiple(dtype), "queue_flows should only contain scalar dtype, as multiple ones should have been broken down already"

        producer_ids = whoproduces[dtype]

        if isinstance(dtype, tuple):
            dtype_cls, dtype_id = dtype
        else:
            dtype_cls = dtype
            dtype_id = ""

        # connect queue with producer
        for queue_id in ntos:
            for prod_id in producer_ids:
                # todo: maybe we need to represent multiple dtypes (= multiple edges) here?
                #       e.g. multiple DTYPES prod to multiple DTYPES cons needs multiple queues?
                #       ...although we use 1 queue per cons for now

                pipes_json['edges'].append({
                    'dtype': f'{dtype_cls.__name__}: {dtype_id}',
                    "from": str(prod_id),
                    "to": str(queue_id)
                })

    # map queue back to their consumers
    for cons in pipe.processes:
        if hasattr(cons, 'queue') and cons.queue:
            if isinstance(cons, Producer):
                skip_queues.add(cons.queue.id)
                continue

            #for _dtype in iterate_dtypes(cons.consumes):
            queue_consumes[cons.queue.id]['dtype'] = cons.consumes
            queue_consumes[cons.queue.id]['list'].add(cons.__PROCESSID__)

    # add queue nodes
    queue: SimpleQueue
    for queue_id, queue in pipe.cons_queues.items():
        if queue_id not in skip_queues:
            pipes_json['nodes'].append({
                'id': str(queue_id),
                'group': 'queues'
            })

    # connect queue node with consumer node
    for queue_id, dd in queue_consumes.items():
        if queue_id in skip_queues:
            continue

        dtype: DTYPES = dd['dtype']
        cons_ids: set[str] = dd['list']
        _dtype_repr = []

        for _dtype_scalar in iterate_dtypes(dtype):
            dtype_cls, dtype_id = _dtype_scalar
            _dtype_repr.append(f'{dtype_cls.__name__}: {dtype_id}')

        for cons_id in cons_ids:
            pipes_json['edges'].append({
                'dtype': ',\n'.join(_dtype_repr),
                "from": str(queue_id),
                "to": str(cons_id)
            })

    if not show_queues:
        trim_queue_nodes(pipes_json)

    if not filename:
        filename = 'flow'
    shutil.copy(os.path.join(os.path.dirname(__file__), 'content', 'flow.html'), filename+'.html')

    with open(filename+'.js', 'w') as fh:
        fh.write('const __FLOWS__ = ')

        json.dump(pipes_json, fh)

    with open(filename+'.html', 'r+') as f:
        text = f.read()

        text = text.replace('{__PIPENAME__}', filename)

        f.seek(0)
        f.write(text)
        f.truncate()


def trim_queue_nodes(d: dict):
    # remove nodes
    removed_nodes = set(map(lambda x: x['id'], filter(lambda x:x.get('group')=='queues', d['nodes'])))
    d['nodes'] = list(filter(lambda x: x['id'] not in removed_nodes, d['nodes']))

    new_edges = []
    # todo: maybe we need to keep nodes? not possible

    # merge edges
    prod2queu = filter(lambda x: x['to'] in removed_nodes, d['edges'])
    queu2cons = filter(lambda x: x['from'] in removed_nodes, d['edges'])

    for edge1, edge2 in product(prod2queu, queu2cons):
        if edge2['from'] != edge1['to']:
            continue

        # add merged queue
        new_edge = edge1.copy()
        new_edge['to'] = edge2['to']
        new_edge['merged'] = True

        new_edges.append(new_edge)

    d['edges'] = new_edges
    return  d
