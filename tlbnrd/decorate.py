import inspect
import typing

def checked(fn):
  # Make sure there are type hints.
  types = typing.get_type_hints(fn)
  if len(types) == 0:
    raise Exception(f"{fn.__name__} has no type hints")

  # Grab the list of parameter names.
  parms = inspect.getfullargspec(fn).args
  
  # Define the wrapper function.
  def wrap(*args):
    # Check that each argument is an instance of its corresponding
    # hinted type.
    for p, a in zip(parms, args):
      t = types[p]
      if (not isinstance(a, t)):
        raise Exception(f"'{type(a).__name__}' is not an instance of '{t.__name__}'")
    return fn(*args)

  return wrap
