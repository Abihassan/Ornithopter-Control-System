import streamlit as st
import cv2
import cvzone
import math
from ultralytics import YOLO
import numpy as np
from PIL import Image

model = YOLO("C:/Users/abiha/OneDrive/Desktop/fire.pt")
classnames = ['fire']

st.set_page_config(
    page_title="🔥 Fire Detection App",
    page_icon=":fire:",
    layout="wide",  
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
        .stApp {
            background-color: #f5f5f5;
        }
        .big-title {
            font-size: 35px;
            color: #ff4b4b;
        }
        .small-title {
            font-size: 18px;
            color: #333;
        }
        .header-icon {
            color: #ff4b4b;
            font-size: 50px;
        }
        .important {
            font-size: 22px;
            font-weight: bold;
            color: #ff4b4b;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='header-icon'>🔥</div>", unsafe_allow_html=True)
st.markdown("<h1 class='big-title'>Fire Detection in Video using AI</h1>", unsafe_allow_html=True)

st.write("Upload a video and see if fire is detected. The AI-powered app will analyze the frames and display results based on fire detection in real-time.")

uploaded_file = st.file_uploader("Upload a video (MP4 format)", type=["mp4"])

if uploaded_file is not None:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.read())

    cap = cv2.VideoCapture("temp_video.mp4")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    st.markdown(f"<p class='small-title'>Total Frames in Video: {total_frames}</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    stframe1 = col1.empty()  
    stframe2 = col2.empty() 

    consecutive_fire_frames = 0  
    fire_detected_threshold = 5  
    fire_detected_continuous = False  

    fire_frames_count = 0  
    frame_count = 0 

    progress_bar = st.progress(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (640, 480))

        original_frame = frame.copy()

        result = model(frame, stream=True)

        fire_detected = False  

        for info in result:
            boxes = info.boxes
            for box in boxes:
                confidence = box.conf[0]
                confidence = math.ceil(confidence * 100)
                Class = int(box.cls[0])
                if confidence > 50:
                    fire_detected = True  
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                  
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                    cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', [x1 + 8, y1 + 100],
                                       scale=1.5, thickness=2)

        if fire_detected:
            consecutive_fire_frames += 1
        else:
            consecutive_fire_frames = 0  

        if consecutive_fire_frames >= fire_detected_threshold:
            fire_detected_continuous = True
            fire_frames_count += 1  
        else:
            fire_detected_continuous = False

        stframe1.image(original_frame, channels="BGR", use_column_width=True, caption="Original Video")
        stframe2.image(frame, channels="BGR", use_column_width=True, caption="Fire Detection")

        frame_count += 1  

        progress = int((frame_count / total_frames) * 100)
        progress_bar.progress(progress)

    cap.release()

    fire_detection_percentage = (fire_frames_count / total_frames) * 100

    st.markdown(f"<p class='important'>Fire detected in {fire_detection_percentage:.2f}% of the video frames.</p>", unsafe_allow_html=True)

    if fire_detection_percentage > 20:
        st.error("🔥 Fire detected in the video!")
    else:
        st.success("✅ No significant fire detected (below 20%) in the video.")
else:
    st.info("Please upload a video to begin fire detection.")
