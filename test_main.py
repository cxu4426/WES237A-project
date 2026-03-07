if __name__ == "__main__":
    # thread set up
    shared = {
        "face_count": 0,
        "capture_request": False,
        "capture_done": False,   # NEW: handshake
        "captured_frame": None
    }

    lock = threading.Lock()

    t_face = threading.Thread(target=face_thread)
    t_led = threading.Thread(target=led_thread)

    t_face.start()
    t_led.start()

    t_led.join()
    t_face.join()

    print("[MAIN] Threads joined")

# process captured frame
frame = shared.get("captured_frame", None)

if frame is not None:
    # color correction part
    # color correction -> everything is an average gray
    b, g, r = cv2.split(frame)
    b_avg, g_avg, r_avg = np.mean(b), np.mean(g), np.mean(r)
    k = (r_avg + g_avg + b_avg) / 3.0
    r = np.clip(r * k/r_avg, 0, 255).astype(np.uint8)
    g = np.clip(g * k/g_avg, 0, 255).astype(np.uint8)
    b = np.clip(b * k/b_avg, 0, 255).astype(np.uint8)
    frame_wb = cv2.merge((b, g, r))

    # --- 2. LAB color normalization (brightness/contrast) ---
    lab = cv2.cvtColor(frame_wb, cv2.COLOR_BGR2LAB)
    l, a, b_lab = cv2.split(lab)
    l_norm = cv2.normalize(l, None, 0, 255, cv2.NORM_MINMAX)
    lab_norm = cv2.merge((l_norm, a, b_lab))
    frame_corrected = cv2.cvtColor(lab_norm, cv2.COLOR_LAB2BGR)

    # --- 3. Save the corrected image ---
    frame = frame_corrected
    cv2.imwrite("captured_corrected.jpg", frame)
    print("[MAIN] Captured image color-corrected and saved as 'captured_corrected.jpg'")

    # ------------------------------------------------------------------
    # processing part

    print("[MAIN] Processing captured frame...")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        x, y, w, h = faces[0]

        # --- Skin region (cheek area) ---
        cheek_region = frame[
            y + h//3 : y + h//2,
            x + w//4 : x + 3*w//4
        ]

        # --- Improved Hair Region (centered above forehead) ---
        hair_top = max(0, y - int(0.25 * h))
        hair_bottom = y - int(0.05 * h)
        hair_left = x + int(0.25 * w)
        hair_right = x + int(0.75 * w)

        hair_region = frame[
            hair_top:hair_bottom,
            hair_left:hair_right
        ]

        # --- Remove skin pixels from hair region ---
        hsv_hair = cv2.cvtColor(hair_region, cv2.COLOR_BGR2HSV)

        lower_skin = (0, 30, 60)
        upper_skin = (20, 150, 255)

        skin_mask = cv2.inRange(hsv_hair, lower_skin, upper_skin)
        hair_mask = cv2.bitwise_not(skin_mask)

        hair_only = cv2.bitwise_and(hair_region, hair_region, mask=hair_mask)

        # --- Eye region ---
        eye_region = frame[
            y + h//5 : y + 2*h//5,
            x + w//10 : x + w//2
        ]

        # Convert to HSV and mask dark colors (iris)
        hsv_eye = cv2.cvtColor(eye_region, cv2.COLOR_BGR2HSV)
        lower_eye = (0, 0, 0)
        upper_eye = (180, 255, 60)  # dark pixels, likely iris/pupil
        mask_eye = cv2.inRange(hsv_eye, lower_eye, upper_eye)
        eye_dark = cv2.bitwise_and(eye_region, eye_region, mask=mask_eye)

        # --- Save debug crops ---
        cv2.imwrite("debug_skin.jpg", cheek_region)
        cv2.imwrite("debug_eye.jpg", eye_dark)
        cv2.imwrite("debug_hair.jpg", hair_only)

        print("Skin Color:", get_color(cheek_region))
        print("Hair Color:", get_color(hair_only))
        print("Eye Color:", get_color(eye_dark))

        # --- Draw bounding boxes ---
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Face
        cv2.rectangle(frame, (x + w//4, y + h//3), (x + 3*w//4, y + h//2), (255, 0, 0), 2)  # Cheek
        cv2.rectangle(frame,(hair_left, hair_top),(hair_right, hair_bottom),(0, 0, 255),2)  # hair
        cv2.rectangle(frame,(x + w//10, y + h//5),(x + w//2, y + 2*h//5),(255, 255, 0),2)   # eye
        
        
        cv2.imwrite("captured_with_boxes.jpg", frame)
        print("[MAIN] Image saved as captured_with_boxes.jpg")

    else:
        print("[MAIN] No face found in captured frame")

else:
    print("[MAIN] No frame captured")

print("Done.")