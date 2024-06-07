import rclpy
from rclpy.node import Node
import socket

from yolov8_msgs.msg import DetectionArray
# Nesne sınıfları sözlüğü
object_classes = {
    0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat',
    9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat',
    16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack',
    25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball',
    33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle',
    40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich',
    49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch',
    58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote',
    66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book',
    74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'
}

class YOLOListener(Node):
    def __init__(self):
        super().__init__('yolo_listener')
        self.subscription = self.create_subscription(
            DetectionArray,
            '/yolo/detections',
            self.detection_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.udp_ip = "127.0.0.1"
        self.udp_port = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def detection_callback(self, data):
        # Başlangıçta tüm bitler sıfır
        bits = [0] * 80

        detected_classes = []

        # Algılanan nesnelere göre bitleri ayarla
        for detection in data.detections:
            class_id = detection.class_id
            if class_id in object_classes:
                bits[class_id] = 1
                detected_classes.append(object_classes[class_id])

        # Bitleri string olarak oluştur ve UDP üzerinden gönder
        message_str = "".join(map(str, bits))
        self.sock.sendto(message_str.encode(), (self.udp_ip, self.udp_port))

        # Tespit edilen nesne sınıflarını terminale yazdır
        if detected_classes:
            self.get_logger().info(f"Detected classes: {', '.join(detected_classes)}")

def main(args=None):
    rclpy.init(args=args)
    yolo_listener = YOLOListener()
    rclpy.spin(yolo_listener)
    yolo_listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

