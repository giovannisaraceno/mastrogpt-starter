import sys
from unittest.mock import Mock, patch
import pytest

# Add the package path to sys.path so that the loader_img module can be found
sys.path.append("packages/gsaraceno/loader_img")
import loader_img

def test_loader_img_initial_state():
    """
    Tests the initial response of the loader_img function when no input is provided.
    It should return the usage instructions and the form definition.
    """
    args = {}
    result = loader_img.loader_img(args)

    # Assert that the output is the default usage message
    assert result['output'] == loader_img.USAGE
    # Assert that the form structure is correctly returned
    assert result['form'] == loader_img.FORM
    # Assert that no html is returned in the initial state
    assert 'html' not in result

@patch('loader_img.vdb.VectorDB')
@patch('loader_img.vision.Vision')
def test_loader_img_with_form_submission(mock_vision, mock_vdb):
    """
    Tests the loader_img function when a form with an image is submitted.
    It should process the image, get a description, insert it into the vector database,
    and return the description, the generated IDs, the form, and an HTML img tag.
    """
    # Mock the Vision and VDB components
    mock_vision_instance = Mock()
    mock_vision.return_value = mock_vision_instance
    mock_vision_instance.decode.return_value = "A beautiful cat"

    mock_vdb_instance = Mock()
    mock_vdb.return_value = mock_vdb_instance
    mock_vdb_instance.insert.return_value = {"ids": ["id123"]}

    # Prepare the arguments for the function call
    fake_image_data = "fake_base64_encoded_image_data"
    args = {
        "input": {
            "form": {
                "pic": fake_image_data
            }
        }
    }

    # Call the function
    result = loader_img.loader_img(args)

    # Assertions
    # Check if Vision and VDB were initialized correctly
    mock_vision.assert_called_once_with(args)
    mock_vdb.assert_called_once_with(args, "cats")

    # Check if the correct methods were called on the instances
    mock_vision_instance.decode.assert_called_once_with(fake_image_data)
    mock_vdb_instance.insert.assert_called_once_with("A beautiful cat")

    # Check the output string
    expected_output = "A beautiful catid123\n"
    assert result['output'] == expected_output

    # Check the returned HTML
    expected_html = f'<img src="data:image/png;base64,{fake_image_data}">'
    assert result['html'] == expected_html

    # Check that the form is still part of the response
    assert result['form'] == loader_img.FORM

@patch('loader_img.vdb.VectorDB')
@patch('loader_img.vision.Vision')
def test_loader_img_with_empty_image(mock_vision, mock_vdb):
    """
    Tests the function's behavior with an empty image string in the form submission.
    It should still go through the processing steps, but with empty data.
    """
    # Mock the Vision and VDB components
    mock_vision_instance = Mock()
    mock_vision.return_value = mock_vision_instance
    mock_vision_instance.decode.return_value = "No image found"

    mock_vdb_instance = Mock()
    mock_vdb.return_value = mock_vdb_instance
    mock_vdb_instance.insert.return_value = {"ids": []}

    # Prepare the arguments with an empty picture
    args = {
        "input": {
            "form": {
                "pic": ""
            }
        }
    }

    # Call the function
    result = loader_img.loader_img(args)

    # Assertions
    mock_vision.assert_called_once_with(args)
    mock_vdb.assert_called_once_with(args, "cats")
    mock_vision_instance.decode.assert_called_once_with("")
    mock_vdb_instance.insert.assert_called_once_with("No image found")

    # Check the output string
    expected_output = "No image found\n"
    assert result['output'] == expected_output

    # Check the returned HTML for an empty image
    expected_html = '<img src="data:image/png;base64,">'
    assert result['html'] == expected_html
    assert result['form'] == loader_img.FORM

def test_loader_img_with_non_dict_input():
    """
    Tests the function's behavior when the 'input' is not a dictionary.
    It should gracefully handle this and return the default USAGE message.
    """
    args = {"input": "just a string"}
    result = loader_img.loader_img(args)

    assert result['output'] == loader_img.USAGE
    assert result['form'] == loader_img.FORM
    assert 'html' not in result

def test_loader_img_with_no_form_key():
    """
    Tests the function's behavior when the 'input' dictionary is missing the 'form' key.
    It should return the default USAGE message.
    """
    args = {"input": {"not_a_form": "some_value"}}
    result = loader_img.loader_img(args)

    assert result['output'] == loader_img.USAGE
    assert result['form'] == loader_img.FORM
    assert 'html' not in result