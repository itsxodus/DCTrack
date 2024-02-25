import cv2
from PIL import Image
import pytesseract
import re
import CamData
import time
import Mapper

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
video_path = 'vid/20240130162559_000927.MP4'
cap = cv2.VideoCapture(video_path)

roi_x, roi_y, roi_width, roi_height = 130, 1390, 390, 30
secondDelay = 10


def timer(func):
    def wrapper(*args, **kwargs):
        print("Please wait... extracting text...")
        startTime = time.time()
        result = func(*args, **kwargs)
        endTime = time.time()
        print(f"Text extraction process took {endTime - startTime:.2f} seconds.")
        return result

    return wrapper


def extractText(video_frame):
    roi = video_frame[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
    pil_roi = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(pil_roi, config='--psm 6')

    allowed_chars = r'[0-9.NW]'
    alphanumeric_text = re.sub(fr'[^{allowed_chars}]', '', text)

    return alphanumeric_text.strip().replace('/', '')


@timer
def start():
    CamDataArray = []
    secondCounter = 0
    while cap.isOpened():

        cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) + 1000 * secondDelay)

        ret, frame = cap.read()
        secondCounter += secondDelay

        if not ret:
            break

        extractedText = extractText(frame)
        extractedLat, extractedLon = extractedText.split(sep=" ")
        CamDataArray.append(CamData.CamData(secondCounter, extractedLat, extractedLon))

    cap.release()
    cv2.destroyAllWindows()

    FormattedCamDataArray = []
    for data in CamDataArray:
        FormattedCamDataArray.append(data.getLoc())

    CamDataArray.clear()

    newMapper = Mapper.Mapper("testmap", FormattedCamDataArray)
    newMapper.createMap()
    newMapper.openMapInBrowser()


if __name__ == "__main__":
    start()
