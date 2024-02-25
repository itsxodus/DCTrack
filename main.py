import cv2
from PIL import Image
import pytesseract
import re
import CamData
import time
import Mapper

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

vids = [
    "D:/DCIM/Movie/20240130145043_000909.MP4",
    "D:/DCIM/Movie/20240130145543_000910.MP4",
    "D:/DCIM/Movie/20240130150043_000911.MP4",
    "D:/DCIM/Movie/20240130150543_000912.MP4",
    "D:/DCIM/Movie/20240130151043_000913.MP4",
    "D:/DCIM/Movie/20240130151543_000914.MP4",
    "D:/DCIM/Movie/20240130152043_000915.MP4",
    "D:/DCIM/Movie/20240130152543_000916.MP4",
    "D:/DCIM/Movie/20240130153042_000917.MP4",
    "D:/DCIM/Movie/20240130153542_000918.MP4",
    "D:/DCIM/Movie/20240130154042_000919.MP4",
    "D:/DCIM/Movie/20240130154543_000920.MP4",
    "D:/DCIM/Movie/20240130155042_000921.MP4",
    "D:/DCIM/Movie/20240130155542_000922.MP4",
    "D:/DCIM/Movie/20240130160042_000923.MP4",
    "D:/DCIM/Movie/20240130161059_000924.MP4",
    "D:/DCIM/Movie/20240130161559_000925.MP4",
    "D:/DCIM/Movie/20240130162059_000926.MP4",
    "D:/DCIM/Movie/20240130162559_000927.MP4",
    "D:/DCIM/Movie/20240130165212_000928.MP4",
    "D:/DCIM/Movie/20240130165713_000929.MP4",
    "D:/DCIM/Movie/20240130170213_000930.MP4",
    "D:/DCIM/Movie/20240130170713_000931.MP4",
    "D:/DCIM/Movie/20240130171213_000932.MP4",
    "D:/DCIM/Movie/20240130171713_000933.MP4",
    "D:/DCIM/Movie/20240130172213_000934.MP4",
    "D:/DCIM/Movie/20240130172713_000935.MP4",
    "D:/DCIM/Movie/20240130173213_000936.MP4",
    "D:/DCIM/Movie/20240130173713_000937.MP4",
    "D:/DCIM/Movie/20240130174213_000938.MP4",
    "D:/DCIM/Movie/20240130174713_000939.MP4",
    "D:/DCIM/Movie/20240130175213_000940.MP4",
]
caps = [cv2.VideoCapture(vid) for vid in vids]

roi_x, roi_y, roi_width, roi_height = 130, 1390, 390, 30
secondDelay = 122


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
    text = pytesseract.image_to_string(pil_roi, config='--psm 13')

    allowed_chars = r'[0-9.NW]'
    alphanumeric_text = re.sub(fr'[^{allowed_chars}]', '', text)

    return alphanumeric_text.strip().replace('/', '')


@timer
def start():
    CamDataArray = []
    secondCounter = 0
    for cap in caps:
        while cap.isOpened():

            cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) + 1000 * secondDelay)

            ret, frame = cap.read()
            secondCounter += secondDelay

            if not ret:
                break

            extractedText = extractText(frame)
            try:
                extractedLat, extractedLon = extractedText.split(sep=" ")
                CamDataArray.append(CamData.CamData(secondCounter, extractedLat, extractedLon))
            except ValueError:
                continue

        cap.release()
        cv2.destroyAllWindows()

    FormattedCamDataArray = []
    for data in CamDataArray:
        if data.getLoc() is not None:
            FormattedCamDataArray.append(data.getLoc())
        else:
            pass

    CamDataArray.clear()

    newMapper = Mapper.Mapper("testmap", FormattedCamDataArray)
    newMapper.createMap()
    newMapper.openMapInBrowser()


if __name__ == "__main__":
    start()
