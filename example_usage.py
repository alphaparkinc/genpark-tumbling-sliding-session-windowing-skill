from client import StreamWindowManager

def main():
    print("=== Testing Stream Window Manager ===")
    wm = StreamWindowManager()
    events = [(1, 10), (3, 20), (5, 30), (7, 40), (12, 50)]

    tumbling = wm.compute_tumbling_windows(events, 5)
    print("Tumbling (size=5):", tumbling)
    assert len(tumbling) == 3

    sliding = wm.compute_sliding_windows(events, 6, 3)
    print("Sliding (size=6, slide=3):", sliding)
    assert len(sliding) >= 3

    session = wm.compute_session_windows(events, 4)
    print("Session (gap=4):", session)
    assert len(session) == 2

    print("Stream Window Manager verified successfully!")

if __name__ == '__main__':
    main()
