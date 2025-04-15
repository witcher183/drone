import cv2
from ultralytics import YOLO
import threading
import pygame

is_run = False

yolo = YOLO('runs/detect/train/weights/best.pt')

videoCap = cv2.VideoCapture('video_bpla/5.mp4')

def voice():
    global is_run
    if not is_run:
        is_run = True
        pygame.init()
        song = pygame.mixer.Sound('voice/speech-1744662701-6786.mp3')
        clock = pygame.time.Clock()
        song.play()
        while pygame.mixer.get_busy():  # Пока звук играет
            clock.tick(10)
        pygame.quit()
        is_run = False

# Function to get class colors
def getColours(cls_num):
    base_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    color_index = cls_num % len(base_colors)
    increments = [(1, -2, 1), (-2, 1, -1), (1, -1, 2)]
    color = [base_colors[color_index][i] + increments[color_index][i] *
             (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)

counter = 1

while True:
    ret, frame = videoCap.read()
    if not ret:
        continue
    results = yolo.track(frame, stream=True)

    thread = threading.Thread(target=voice)

    for result in results:
        classes_names = result.names
        if len(result.boxes) > 0:
            thread.start()
            print(is_run)
            cv2.imwrite(f'detected_bpla/{counter}.jpg', frame)
            counter += 1
        for box in result.boxes:
            if box.conf[0] > 0.4:
                [x1, y1, x2, y2] = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cls = int(box.cls[0])
                class_name = classes_names[cls]
                colour = getColours(cls)
                cv2.rectangle(frame, (x1, y1), (x2, y2), colour, 2)
                cv2.putText(frame, f'{classes_names[int(box.cls[0])]} {box.conf[0]:.2f}', (x1, y1),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, colour, 2)


    cv2.imshow('frame', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

videoCap.release()
cv2.destroyAllWindows()