
 
import datetime
import uuid
from flask import jsonify

class CommonJsonResponse:

    def common_response(status="success", message="", data=None, error=None, pagination=None,status_code = None):
        """
        Standardized API response format with omitted null values"
        """
            
        response = {
            "status": status,
            "message": message,
            "meta": {
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "request_id": str(uuid.uuid4())
            }
            }

        if data is not None:
            response["data"] = data
        
        if error is not None:
            response["error"] = error

        if pagination:
            response["meta"]["pagination"] = pagination

        if status_code:
            response['status_code'] = status_code
        

        return jsonify(response)

