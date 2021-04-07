from jina import Flow
from jina import Document

from tests import validate_callback


def input_function():
    with Document() as doc1:
        ev1 = doc1.evaluations.add()
        ev1.value = 1
        ev1.op_name = 'op1'
    with Document() as doc2:
        ev2 = doc2.evaluations.add()
        ev2.value = 2
        ev2.op_name = 'op2'
    return [doc1, doc2]


def test_collect_evals_driver(mocker):
    def validate(req):
        assert len(req.docs) == 2
        # each doc should now have two evaluations
        for d in req.docs:
            assert len(d.evaluations) == 2

    mock = mocker.Mock()
    # simulate two encoders
    flow = (
        Flow()
        .add(name='a')
        .add(name='b', needs='gateway')
        .join(needs=['a', 'b'], uses='- !CollectEvaluationDriver {}')
    )
    with flow:
        flow.index(inputs=input_function, on_done=mock)

    mock.assert_called_once()
    validate_callback(mock, validate)
