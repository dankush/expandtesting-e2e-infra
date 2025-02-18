# test_pytest_interview.py
import pytest



# -------------------------------
# Q2. What is a fixture in Pytest?
# -------------------------------
@pytest.fixture
def sample_fixture():
    """
    A fixture is a reusable component that sets up a state or resource for tests.
    This fixture simply returns a sample dictionary.
    """
    # Setup phase: define some test data
    data = {"key": "value"}
    # (No explicit teardown here)
    return data

def test_using_fixture(sample_fixture):
    """
    This test uses the 'sample_fixture' as an argument.
    Pytest automatically calls the fixture before running the test.
    """
    # Assert that the fixture returns the expected data
    assert sample_fixture == {"key": "value"}
    # Note: Fixtures improve test reusability and clarity.


# -------------------------------
# Q4. How do you parametrize tests in Pytest?
# -------------------------------
@pytest.mark.parametrize("input_val, expected", [
    (2, 3),
    (3, 4),
    (10, 11)
])
def test_parametrization(input_val, expected):
    """
    The @pytest.mark.parametrize decorator allows us to run the same test function
    with different input values.
    Here, we test that adding 1 to each input produces the expected result.
    """
    # Act & Assert
    assert input_val + 1 == expected
    # Note: This reduces redundancy by combining multiple test cases into one.



# -------------------------------
# Q7. What is monkeypatching in Pytest?
# -------------------------------
def test_monkeypatch(monkeypatch):
    """
    Monkeypatching allows you to temporarily modify or replace attributes or functions.
    In this example, we replace a simple function to simulate a mock.
    """
    # Define a fake function to replace the real one.
    def fake_function():
        return "mocked value"
    
    # Use monkeypatch to replace the built-in 'str.upper' method as a demonstration.
    # (In practice, you would patch your module's function.)
    monkeypatch.setattr(str, "upper", lambda self: "MOCKED")
    
    # When we call upper() on any string, it now returns "MOCKED"
    result = "hello".upper()
    assert result == "MOCKED"
    # Note: Monkeypatching is useful to simulate external dependencies or specific behaviors.



# -------------------------------
# Q8. How do you test for exceptions in Pytest?
# -------------------------------
def test_exception_handling():
    """
    Use pytest.raises() to verify that a function raises an expected exception.
    """
    # Define a function that raises ValueError when input is negative.
    def divide_by_number(x):
        if x < 0:
            raise ValueError("Negative numbers not allowed")
        return 10 / (x if x != 0 else 1)
    
    # Test that calling with a negative number raises ValueError.
    with pytest.raises(ValueError, match="Negative numbers not allowed"):
        divide_by_number(-5)
    
    with pytest.raises(ValueError):
        divide_by_number(5)
    # Note: pytest.raises() is used as a context manager to catch exceptions.




# -------------------------------
# Q11. What is the difference between xfail and skip in Pytest?
# -------------------------------
@pytest.mark.xfail(reason="Known bug: division by zero not handled")
def test_expected_failure():
    """
    The xfail marker is used to indicate that a test is expected to fail.
    Pytest will record the failure as an expected failure (xfail) rather than a normal failure.
    """
    # This test is expected to fail because division by zero raises an exception.
    with pytest.raises(ZeroDivisionError):
        1 / 0

@pytest.mark.skip(reason="Feature not implemented yet")
def test_skipped():
    """
    The skip marker tells Pytest to completely skip this test.
    It is reported as skipped in the test results.
    """
    # This code is never executed.
    assert 1 + 1 == 3


# -------------------------------
# Mock example:
# -------------------------------
def external_api_call():
    """
    Imagine this function makes an external API call.
    In tests, we often want to replace its behavior.
    """
    return "real result"

def test_using_mock(mocker):
    """
    This test demonstrates how to use a mock.
    Mocks are used to swap out a function with a test-specific version.
    We use the pytest-mock plugin (which wraps unittest.mock) to patch 'external_api_call'.
    """
    # Replace external_api_call with a mock that returns "mocked result"
    mocker.patch(__name__ + ".external_api_call", return_value="mocked result")
    result = external_api_call()
    # Assert that the mocked function returns the expected value.
    assert result == "mocked result"

# ---------------------------------
# Note:
# - A fixture (e.g. sample_resource) is defined with the @pytest.fixture decorator
#   to supply test-specific resources.
# - A mock is used to replace parts of your code (e.g. external_api_call) for a single test.
#   Here, we used the 'mocker' fixture from pytest-mock to create a mock.


# -------------------------------
# Mock example: What is a Pytest plugin, and how do you use it?
# -------------------------------
def external_function():
    """
    Imagine this function performs a critical external operation,
    such as calling an API. In tests, we often want to replace its behavior.
    """
    return "original result"

def test_using_pytest_plugin(mocker):
    """
    This test demonstrates using a Pytest plugin to patch behavior.
    The pytest-mock plugin provides the 'mocker' fixture, which is used to
    replace 'external_function' with a fake version.
    """
    # Patch external_function to return "mocked result" instead of "original result"
    mocker.patch(__name__ + ".external_function", return_value="mocked result")
    
    # When we call external_function(), it should now return the mocked value.
    result = external_function()
    assert result == "mocked result"

# ---------------------------------
# Notes:
# 1. A Pytest plugin is a Python package that extends Pytest's functionality.
#    For example, pytest-mock gives us the 'mocker' fixture to easily create mocks.
#
# 2. To use a plugin, install it via pip:
#      pip install pytest-mock
#
# 3. You may also modify your pytest.ini file if the plugin requires configuration.
#    For instance, if a plugin provides additional markers, you might need to register them.
#
# 4. Running this file with pytest (e.g., "pytest test_pytest_plugin.py -v")
#    will execute the test, using the plugin-provided 'mocker' fixture to replace external_function.