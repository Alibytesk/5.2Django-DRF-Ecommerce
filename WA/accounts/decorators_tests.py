from unittest.mock import patch, MagicMock
from functools import wraps
from types import FunctionType

def mock_post(main: FunctionType) -> FunctionType:
    @wraps(main)
    @patch('accounts.views.requests.post')
    def wrapper(self, mock_post, *args, **kwargs):
        def side_effect(url, headers=None, json=None):
            mock_response = MagicMock()
            if 'check_authenticate' in url:
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'response': 'is_Authenticated',
                }
            elif 'change-password' in url:
                current_password = json.get('current_password')
                password1 = json.get('password1')
                if current_password != 'Django12345!@#$%':
                    mock_response.status_code = 406
                    mock_response.json.return_value = {
                        'response': 'your current password is wrong'
                    }
                elif current_password == password1:
                    mock_response.status_code = 406
                    mock_response.json.return_value = {
                        'response': 'new password can not be your current password'
                    }
                elif current_password == 'Django12345!@#$%' and current_password != password1:
                    mock_response.status_code = 200
                    mock_response.json.return_value = {
                        'response': 'password successfully updated'
                    }
            return mock_response
        mock_post.side_effect = side_effect
        return main(self, *args, **kwargs)
    return wrapper
