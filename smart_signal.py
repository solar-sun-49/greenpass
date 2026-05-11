from ultralytics import YOLO

model = YOLO("UVH-26/weights/YOLOv11-S/UVH-26-MV-YOLOv11-S.pt")

class_names = open("UVH-26/uvh_classes.txt").read().splitlines()

# ✅ Categorize vehicles
def classify_vehicle(name):
    if name in ["Two-wheeler", "Bicycle"]:
        return "two"
    elif name in ["Three-wheeler"]:
        return "three"
    elif name in ["Hatchback", "Sedan", "SUV", "MUV", "Van"]:
        return "four"
    else:
        return "heavy"


PCU = {
    "two": 0.5,
    "three": 1.2,
    "four": 1.0,
    "heavy": 3.5
}

def process_lane(image_path):
    results = model(image_path)

    counts = {"two":0, "three":0, "four":0, "heavy":0}

    for r in results:
        for box in r.boxes:
            cls = int(box.cls)
            name = class_names[cls]
            category = classify_vehicle(name)
            counts[category] += 1

    total_vehicles = sum(counts.values())
    lane_weight = sum(counts[k] * PCU[k] for k in counts)

    if total_vehicles > 20:
        lane_weight *= 1.3
    elif total_vehicles > 10:
        lane_weight *= 1.1

    return counts, lane_weight

lanes = [
    "test_images/input/lane1.jpg",
    "test_images/input/lane2.jpg",
    "test_images/input/lane3.jpg",
    "test_images/input/lane4.jpg"
]

lane_data = []
total_weight = 0

for lane in lanes:
    counts, weight = process_lane(lane)
    lane_data.append((counts, weight))
    total_weight += weight

TOTAL_CYCLE = 120

print("\n=== TRAFFIC ANALYSIS ===")

final_times = []

for i, (counts, weight) in enumerate(lane_data):

    if total_weight == 0:
        time = TOTAL_CYCLE // 4
    else:
        time = int((weight / total_weight) * TOTAL_CYCLE)

    # 🔥 Realistic constraints
    time = max(15, min(time, 60))

    final_times.append(time)

    print(f"\nLane {i+1}")
    print("Counts:", counts)
    print("Weight:", round(weight, 2))
    print("Green Time:", time, "sec")

print("\n=== FINAL SIGNAL PLAN ===")

for i, t in enumerate(final_times):
    print(f"Lane {i+1}: {t} sec GREEN")

print(f"\nTotal Cycle Time: {sum(final_times)} sec")