

from flask import jsonify

class CommonResponse:

    def create_response(resp_type, message="", data=None, error=None, status_code=200):
        """Standardized JSON response format"""
        response = {
            "resp_type": resp_type,
            "message": message,
            "data": data,
            "error": error
        }
        return jsonify(response), status_code
