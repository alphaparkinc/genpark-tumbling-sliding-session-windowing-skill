class StreamWindowManager:
    """Out-of-order stream event windowing engine."""
    def __init__(self, watermark_delay=2):
        self.watermark_delay = watermark_delay

    def compute_tumbling_windows(self, events, window_size):
        windows = {}
        for ts, v in sorted(events, key=lambda x: x[0]):
            start = (ts // window_size) * window_size
            end = start + window_size
            w_key = (start, end)
            if w_key not in windows:
                windows[w_key] = []
            windows[w_key].append(v)
        return windows

    def compute_sliding_windows(self, events, window_size, slide_step):
        windows = {}
        for ts, v in sorted(events, key=lambda x: x[0]):
            first_start = (ts // slide_step) * slide_step - window_size + slide_step
            start = first_start
            while start <= ts:
                end = start + window_size
                if start <= ts < end:
                    w_key = (start, end)
                    if w_key not in windows:
                        windows[w_key] = []
                    windows[w_key].append(v)
                start += slide_step
        return windows

    def compute_session_windows(self, events, inactivity_gap):
        sessions = []
        sorted_events = sorted(events, key=lambda x: x[0])
        if not sorted_events:
            return sessions

        curr_start = sorted_events[0][0]
        curr_end = sorted_events[0][0]
        curr_vals = [sorted_events[0][1]]

        for ts, v in sorted_events[1:]:
            if ts - curr_end > inactivity_gap:
                sessions.append({'start': curr_start, 'end': curr_end, 'values': curr_vals})
                curr_start = ts
                curr_end = ts
                curr_vals = [v]
            else:
                curr_end = ts
                curr_vals.append(v)

        sessions.append({'start': curr_start, 'end': curr_end, 'values': curr_vals})
        return sessions
