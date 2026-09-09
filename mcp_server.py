import sys
import json
from client import StreamWindowManager

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    wm = StreamWindowManager()
    events = params.get("events", [])
    if method == "tumbling":
        return wm.compute_tumbling_windows(events, params.get("size", 10))
    elif method == "sliding":
        return {str(k): v for k, v in wm.compute_sliding_windows(events, params.get("size", 10), params.get("slide", 5)).items()}
    elif method == "session":
        return {"sessions": wm.compute_session_windows(events, params.get("gap", 5))}
    return {"error": "Unknown method"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_request(req)
        print(json.dumps(res))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
