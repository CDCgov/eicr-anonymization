import functools
import hashlib
import inspect
import pickle
import random
from contextlib import contextmanager


@contextmanager
def isolated_random(seed_value):
    """Context manager that temporarily replaces global random with seeded instance."""
    func_random = random.Random(seed_value)

    # Store original functions we're replacing
    original_funcs = {
        "random": random.random,
        "randint": random.randint,
        "choice": random.choice,
        "choices": random.choices,
        "shuffle": random.shuffle,
    }

    # Replace with our seeded instance
    random.random = func_random.random
    random.randint = func_random.randint
    random.choice = func_random.choice
    random.choices = func_random.choices
    random.shuffle = func_random.shuffle

    try:
        yield
    finally:
        # Restore original functions
        for name, func in original_funcs.items():
            setattr(random, name, func)


def deterministic(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, "is_deterministic") and self.is_deterministic:
            signature = inspect.signature(func)
            bound_args = signature.bind(self, *args, **kwargs)
            bound_args.apply_defaults()
            params_dict = dict(
                sorted((k, v) for k, v in bound_args.arguments.items() if k != "self")
            )
            seed = hash_params_to_seed(params_dict, self.seed)
            with isolated_random(seed):
                return func(*args, **kwargs)
            random.seed(seed)
        return func(self, *args, **kwargs)

    return wrapper


def hash_params_to_seed(params, global_seed):
    """
    Convert function parameters to a deterministic integer seed.

    Args:
        params (dict): Dictionary of parameter names and values

    Returns:
        int: Deterministic seed value
    """
    try:
        # Use pickle to serialize the parameters (handles most Python objects)
        serialized = pickle.dumps(params, protocol=pickle.HIGHEST_PROTOCOL)

        # Create SHA-256 hash
        hash_obj = hashlib.sha256(serialized)
        if global_seed:
            hash_obj.update(str(global_seed).encode())
        hash_hex = hash_obj.hexdigest()

        # Convert to integer seed (Python's random module expects int)
        # Take first 8 hex chars to avoid extremely large numbers
        seed = int(hash_hex[:8], 16)

        return seed
    except (pickle.PicklingError, TypeError) as e:
        # Fallback: convert to string and hash
        params_str = str(sorted(params.items()))
        hash_obj = hashlib.sha256(params_str.encode("utf-8"))
        if global_seed:
            hash_obj.update(str(global_seed).encode())
        seed = int(hash_obj.hexdigest()[:8], 16)
        return seed