from random import seed

import pytest


@pytest.fixture
def set_random_seed(request):
    """Set up a random seed for reproducibility.

    This fixture ensures that the random seed is set to a fixed value for the first iteration of
    each test function. This ensures that we get deterministic results regardless of the order
    in which the tests are run.
    """
    callspec = getattr(request.node, "callspec", None)
    repeat_iteration = callspec.params.get("__pytest_repeat_step_number", 0) if callspec else 0
    seed(repeat_iteration)
