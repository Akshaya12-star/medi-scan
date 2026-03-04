import cv2
import numpy as np
from pyzbar.pyzbar import decode

def start_scanner():
    cap = cv2.VideoCapture(0)

    # Increase camera resolution
    cap.set(3, 1280)  # Width
    cap.set(4, 720)   # Height

    print("Scanning... Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to access camera")
            break

        # Resize for better detection
        frame = cv2.resize(frame, None, fx=1.2, fy=1.2)

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Improve contrast
        gray = cv2.equalizeHist(gray)

        # Sharpen image
        kernel = np.array([[0, -1, 0],
                           [-1, 5,-1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(gray, -1, kernel)

        # Adaptive threshold
        thresh = cv2.adaptiveThreshold(
            sharpened,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2
        )

        # Try decoding step by step
        codes = decode(frame)

        if not codes:
            codes = decode(gray)

        if not codes:
            codes = decode(sharpened)

        if not codes:
            codes = decode(thresh)

        # Draw results
        for code in codes:
            data = code.data.decode("utf-8")
            code_type = code.type

            print("Detected:", code_type, data)

            x, y, w, h = code.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame,
                        f"{code_type}: {data}",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2)

        cv2.imshow("MediShield Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

start_scanner()