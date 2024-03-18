import cv2
import mediapipe as mp
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

for x in range(0, len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

cap = cv2.VideoCapture(1)
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def angle_stepperx(angle):

    if angle<-50:
        prov=1
        command = 'L'
        serialInst.write(command.encode('utf-8'))
        print("LEFT")


    elif angle>50:
        prov=2
        command = 'R'
        serialInst.write(command.encode('utf-8'))
        print("RIGHT")

    elif -50 < angle < 50:
        command = 'C'
        serialInst.write(command.encode('utf-8'))
        print("Stop")

with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.5) as face_detection:
  while cap.isOpened():
    success, image = cap.read()

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    H = image.shape[0]
    W = image.shape[1]
    start_point =  (int(W//2),0)
    end_point = (int(W//2),int(H))
    start_point1 = (0, int(H//2))
    end_point1 = (int(W), int(H//2))
    ceny, cenx = int(H//2), int(W//2)
    cv2.line(image, start_point, end_point, (0,255,0), 1) 
    cv2.line(image, start_point1, end_point1, (0,255,0), 1) 
    
    image.flags.writeable = False
    results = face_detection.process(image)
    for i in results.detections:
        print(i.location_data.relative_keypoints[0])

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.detections:
      for detection in results.detections:
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = image.shape
        x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                     int(bboxC.width * iw), int(bboxC.height * ih)
        Xpos = x+(w/2)
        Ypos = y+(h/2)
        distx = (Xpos - cenx)
        # print(distx)
        # Draw bounding box
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.line(image, (cenx, ceny), (int(Xpos),int(Ypos)), (255,255,255), 2) 
        # angle_stepperx(distx)
    
    cv2.imshow('MediaPipe Face Detection', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
cv2.destroyAllWindows()

        