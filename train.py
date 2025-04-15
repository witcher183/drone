from ultralytics import YOLO


model = YOLO("model/yolo11m.pt")


model.train(data="data/data.yaml", epochs=30, imgsz=640, batch=4)