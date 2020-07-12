from flask import jsonify


def get_response(data, success=True, error=0):
    return jsonify({
        "success": success,
        "error": error,
        "message": data
    })
