import pytest
import json


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    x = yield
    x._result.max_score = getattr(item._obj, 'max_score', 0)
    x._result.visibility = getattr(item._obj, 'visibility', 'visible')

def pytest_terminal_summary(terminalreporter, exitstatus):
    json_results = {'tests': []}

    all_tests = []
    if ('passed' in terminalreporter.stats):
        all_tests = all_tests + terminalreporter.stats['passed']
    if ('failed' in terminalreporter.stats):
        all_tests = all_tests + terminalreporter.stats['failed']

    for s in all_tests:
        output = ''
        score = s.max_score
        if (s.outcome == 'failed'):
            score = 0
            output = str(s.longrepr.chain[0][0].reprentries[0])

        json_results["tests"].append(
            {
                'score': score,
                'max_score': s.max_score,
                'name': s.location[2],
                'output': output,
                'visibility': s.visibility
            }
        )
        json_results.append({"stdout_visibility": "hidden"})

    with open('results.json', 'w') as results:
        results.write(json.dumps(json_results, indent=4))