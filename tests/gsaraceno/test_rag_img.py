import sys
from unittest.mock import patch, Mock, MagicMock
import json
import socket

# Add the package path to sys.path so that the rag_img module can be found
sys.path.append("packages/gsaraceno/rag_img")
sys.path.append("packages/vdb/load")
import rag_img

def test_rag_img_initial_state():
    """
    Tests the initial state of rag_img with no input.
    It should return the default usage message.
    """
    args = {}
    result = rag_img.rag_img(args)
    assert result["output"] == "Your query is then passed to the LLM with the sentences for an answer."
    assert result["streaming"] is True

@patch('rag_img.llm')
@patch('rag_img.vdb.VectorDB')
def test_rag_img_with_input(mock_vdb, mock_llm):
    """
    Tests the main RAG logic when input is provided.
    It should perform a vector search, construct a prompt, and call the LLM.
    """
    # Arrange
    args = {"input": "what is in the image?"}
    mock_db_instance = Mock()
    mock_db_instance.vector_search.return_value = [
        (0.9, "A cat is sleeping."),
        (0.8, "The sun is shining.")
    ]
    mock_vdb.return_value = mock_db_instance
    mock_llm.return_value = "The image contains a sleeping cat under the sun."

    # Act
    result = rag_img.rag_img(args)

    # Assert
    mock_vdb.assert_called_once_with(args, rag_img.COLLECTION)
    mock_db_instance.vector_search.assert_called_once_with("what is in the image?", limit=rag_img.SIZE)
    
    expected_prompt = (
        "Consider the following text:\n"
        "A cat is sleeping.\n"
        "The sun is shining.\n"
        "Answer to the following prompt:\n"
        "what is in the image?"
    )
    mock_llm.assert_called_once_with(args, rag_img.MODEL, expected_prompt)
    
    assert result["output"] == "The image contains a sleeping cat under the sun."
    assert result["streaming"] is True

@patch('rag_img.stream')
@patch('rag_img.req.post')
def test_llm(mock_post, mock_stream):
    """
    Tests the llm function to ensure it calls the request API and streams the response.
    """
    # Arrange
    args = {"OLLAMA_HOST": "ollama.test", "AUTH": "user:pass"}
    mock_response = Mock()
    mock_response.iter_lines.return_value = [b'line1', b'line2']
    mock_post.return_value = mock_response
    mock_stream.return_value = "streamed response"

    # Act
    response = rag_img.llm(args, "test-model", "test-prompt")

    # Assert
    expected_url = "https://user:pass@ollama.test/api/generate"
    expected_payload = {
        "model": "test-model",
        "prompt": "test-prompt",
        "stream": True
    }
    mock_post.assert_called_once_with(expected_url, json=expected_payload, stream=True)
    mock_stream.assert_called_once_with(args, [b'line1', b'line2'])
    assert response == "streamed response"

@patch('socket.socket')
def test_stream(mock_socket):
    """
    Tests the stream function to ensure it correctly processes and sends data over a socket.
    """
    # Arrange
    args = {"STREAM_HOST": "localhost", "STREAM_PORT": "9999"}
    mock_sock_instance = MagicMock()
    mock_socket.return_value.__enter__.return_value = mock_sock_instance
    
    lines = [
        json.dumps({"response": "Hello"}).encode('utf-8'),
        json.dumps({"response": " World"}).encode('utf-8')
    ]

    # Act
    result = rag_img.stream(args, lines)

    # Assert
    mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
    mock_sock_instance.connect.assert_called_once_with(("localhost", 9999))
    
    assert mock_sock_instance.sendall.call_count == 2
    call1_args = mock_sock_instance.sendall.call_args_list[0].args[0]
    call2_args = mock_sock_instance.sendall.call_args_list[1].args[0]
    assert json.loads(call1_args.decode('utf-8')) == {"output": "Hello"}
    assert json.loads(call2_args.decode('utf-8')) == {"output": " World"}
    
    mock_sock_instance.close.assert_called_once()
    assert result == "Hello World"

@patch('socket.socket')
def test_streamlines(mock_socket):
    """
    Tests the streamlines function for plain text streaming over a socket.
    """
    # Arrange
    args = {"STREAM_HOST": "localhost", "STREAM_PORT": "9999"}
    mock_sock_instance = MagicMock()
    mock_socket.return_value.__enter__.return_value = mock_sock_instance
    
    lines = ["Hello", " World"]

    # Act
    with patch('time.sleep', return_value=None): # Mock sleep to speed up test
        result = rag_img.streamlines(args, lines)

    # Assert
    mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
    mock_sock_instance.connect.assert_called_once_with(("localhost", 9999))
    
    assert mock_sock_instance.sendall.call_count == 2
    call1_args = mock_sock_instance.sendall.call_args_list[0].args[0]
    call2_args = mock_sock_instance.sendall.call_args_list[1].args[0]
    assert json.loads(call1_args.decode('utf-8')) == {"output": "Hello"}
    assert json.loads(call2_args.decode('utf-8')) == {"output": " World"}
    
    mock_sock_instance.close.assert_called_once()
    assert result == "Hello World"