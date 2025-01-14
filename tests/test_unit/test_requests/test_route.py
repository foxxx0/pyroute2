from socket import AF_INET, AF_INET6

import pytest
from common import Request, Result, run_test
from pr2modules.requests.route import RouteFieldFilter, RouteIPRouteFilter

config = {
    'filters': (
        {'class': RouteFieldFilter, 'argv': []},
        {'class': RouteIPRouteFilter, 'argv': ['add']},
    )
}


result = Result({'oif': 1, 'iif': 2})


@pytest.mark.parametrize(
    'spec,result',
    (
        (Request({'oif': 1, 'iif': 2}), result),
        (Request({'oif': [1], 'iif': [2]}), result),
        (Request({'oif': (1,), 'iif': (2,)}), result),
    ),
    ids=['int', 'list', 'tuple'],
)
def test_index(spec, result):
    return run_test(config, spec, result)


result_dst_ipv4 = Result(
    {
        'dst': '10.0.0.0',
        'dst_len': 24,
        'family': AF_INET,
        'gateway': '10.1.0.1',
    }
)
result_dst_ipv6 = Result(
    {
        'dst': 'fc01:1100::',
        'dst_len': 48,
        'family': AF_INET6,
        'gateway': 'fc00::1',
    }
)


@pytest.mark.parametrize(
    'spec,result',
    (
        (
            Request({'dst': 'default', 'gateway': '10.0.0.1'}),
            Result({'gateway': '10.0.0.1', 'family': AF_INET}),
        ),
        (
            Request({'dst': 'default', 'gateway': 'fc00::1'}),
            Result({'gateway': 'fc00::1', 'family': AF_INET6}),
        ),
        (
            Request({'dst': '10.0.0.0/24', 'gateway': '10.1.0.1'}),
            result_dst_ipv4,
        ),
        (
            Request({'dst': '10.0.0.0/255.255.255.0', 'gateway': '10.1.0.1'}),
            result_dst_ipv4,
        ),
        (
            Request({'dst': '10.0.0.0', 'dst_len': 24, 'gateway': '10.1.0.1'}),
            result_dst_ipv4,
        ),
        (
            Request({'dst': 'fc01:1100::/48', 'gateway': 'fc00::1'}),
            result_dst_ipv6,
        ),
        (
            Request(
                {'dst': 'fc01:1100::', 'dst_len': 48, 'gateway': 'fc00::1'}
            ),
            result_dst_ipv6,
        ),
    ),
    ids=[
        'default-ipv4',
        'default-ipv6',
        'split-ipv4-int',
        'split-ipv4-dqn',
        'explicit-ipv4-int',
        'split-ipv6-int',
        'explicit-ipv6-int',
    ],
)
def test_dst(spec, result):
    return run_test(config, spec, result)
