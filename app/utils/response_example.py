from typing import Any, Dict, Optional

def make_response_example(
    success: bool,
    message: str,
    data: Optional[Any] = None,
    statusRes: int = 400
) -> Dict[int, Dict[str, Any]]:
    
    if success is None:
        success = status < 400
            
    return {
        statusRes: {
            "description": message,
            "content": {
                "application/json": {
                    "example": {
                        "success": success,
                        "message": message,
                        "data": data,
                        "status": statusRes,
                    }
                }
            }
        }
    }