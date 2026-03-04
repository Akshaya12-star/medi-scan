import cv2
from pyzbar.pyzbar import decode

def start_qr_scanner():
    # Start camera (0 = default webcam)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Scanning QR Code... Press 'q' to exit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        # Decode QR codes in frame
        qr_codes = decode(frame)

        for qr in qr_codes:
            qr_data = qr.data.decode("utf-8")
            qr_type = qr.type

            print("\nQR Code Detected!")
            print("Type:", qr_type)
            print("Data:", qr_data)

            # Draw bounding box
            x, y, w, h = qr.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display QR data on frame
            cv2.putText(frame, qr_data, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)

        cv2.imshow("MediShield QR Scanner", frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_qr_scanner()