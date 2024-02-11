import cv2
from PIL import Image
import pytesseract
import re
import CamData

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

video_path = 'vid/20240130162559_000927.MP4'
cap = cv2.VideoCapture(video_path)

roi_x, roi_y, roi_width, roi_height = 130, 1390, 390, 30
secondDelay = 5

CamDataArray = []

def extract_text(video_frame):
    roi = video_frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
    pil_roi = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(pil_roi, config='--psm 6')

    allowed_chars = r'[0-9.NW]'
    alphanumeric_text = re.sub(fr'[^{allowed_chars}]', '', text)

    return alphanumeric_text.strip().replace('/', '')


secondCounter = 0
while cap.isOpened():

    cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) + 1000 * secondDelay)

    ret, frame = cap.read()
    secondCounter += secondDelay

    if not ret:
        break

    extracted_text = extract_text(frame)
    extracted_lat, extracted_lon = extracted_text.split(sep=" ")
    CamDataArray.append(CamData.CamData(secondCounter, extracted_lat, extracted_lon))

cap.release()
cv2.destroyAllWindows()

for data in CamDataArray:
    print(data.printData())
