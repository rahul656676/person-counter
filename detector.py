from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

# Store unique entered IDs
entered_ids = set()

# Counting line
line_y = 250


def generate_frames(video_path):

    cap = cv2.VideoCapture(video_path)

    while True:

        success, frame = cap.read()

        if not success:
            break

        results = model.track(
            frame,
            persist=True,
            classes=[0]
        )

        current_count = 0

        # Draw counting line
        cv2.line(
            frame,
            (0, line_y),
            (frame.shape[1], line_y),
            (0, 0, 255),
            3
        )

        if results[0].boxes.id is not None:

            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids = results[0].boxes.id.cpu().numpy()

            current_count = len(ids)

            for box, track_id in zip(boxes, ids):

                x1, y1, x2, y2 = map(int, box)

                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)

                track_id = int(track_id)

                # Draw person box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # Show tracking ID
                cv2.putText(
                    frame,
                    f"ID {track_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 0),
                    2
                )

                # Center point
                cv2.circle(
                    frame,
                    (cx, cy),
                    5,
                    (0, 0, 255),
                    -1
                )

                # Count unique entries
                if cy > line_y:
                    entered_ids.add(track_id)

        # Right-side dashboard
        cv2.rectangle(
            frame,
            (frame.shape[1] - 260, 0),
            (frame.shape[1], 140),
            (40, 40, 40),
            -1
        )

        cv2.putText(
            frame,
            f"Current: {current_count}",
            (frame.shape[1] - 240, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Total Count: {len(entered_ids)}",
            (frame.shape[1] - 240, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )

        ret, buffer = cv2.imencode(".jpg", frame)

        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" +
            frame +
            b"\r\n"
        )