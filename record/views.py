import datetime
import os
import random

import argparse
import ffmpeg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

import cv2
import face_recognition
# import DateTime
# Create your views here.
from Face_monitor.settings import BASE_DIR
from faces.models import Faces
from record.models import Record


def record(request):
    return render(request,'admin/record.html')

def startRecord(request):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc('U','2','6','3')
    dt=datetime.date.today()
    outfile = 'static/video/{}.mp4'.format(dt)
    out = cv2.VideoWriter('../../Envs/virtual_env/Lib/site-packages/simpleui/{}'.format(outfile),fourcc,30.0,(640,480))

    # print(ffmpegresult)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while(cap.isOpened()):
        ret,frame = cap.read()
        if ret == True:     #有视频时
            frame = cv2.flip(frame,1)
            out.write(frame)
            cv2.imshow('camera',frame)
            # return HttpResponse(frame,content_type="image/png")
            if cv2.waitKey(1) & 0xFF == ord('s'):
                faces = face_cascade.detectMultiScale(frame,1.3,2)
                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                    cv2.imshow('frame',frame)
                    face_image = frame[y:y + h, x:x + h]
                    face_readytoread_encodings = face_recognition.face_encodings(face_image)  # 新图encoding
                    faces_dbs = Faces.objects.filter(face_date=dt)

                    for face_readytoread_encoding in face_readytoread_encodings:
                        for faces_db in faces_dbs:
                            face_read = face_recognition.load_image_file('../../Envs/virtual_env/Lib/site-packages/simpleui/{}'.format(faces_db.face_url))
                            face_read_encoding = face_recognition.face_encodings(face_read)

                            res = face_recognition.compare_faces(face_read_encoding,face_readytoread_encoding,tolerance=0.6)

                            if res == [True]:
                                faces_db.delete()
                                # face_image.pop
                                break
                    else:
                        num = random.randint(0,10000)
                        face_source = "static/faces/{}_{}.png".format(dt, num)
                        cv2.imwrite('../../Envs/virtual_env/Lib/site-packages/simpleui/{}'.format(face_source),face_image)
                        faces_db = Faces(face_url=face_source,face_date=dt)
                        faces_db.save()
                if cv2.waitKey(0) & 0xFF == ord('1'):
                    break

            elif cv2.waitKey(1) & 0xFF == ord('1'):   #1退出视频
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()


    rd = Record.objects.filter(datetime=dt).first()
    print(rd)
    # print(rd)
    if rd:
        # rd.record_url = outfile
        # rd.save()
        pass
    else:
        rd = Record(record_url=outfile,datetime=dt)
        rd.save()
    return HttpResponse(request,'监控成功')



def checkRecord(request,video_id):

    videoID = video_id
    record = Record.objects.filter(id=videoID).first()
    # print(record)
    videoName = record.record_url
    # videoDate = record.datetime

    def on_change(x):
        # 设置播放的帧数
        cap.set(cv2.CAP_PROP_POS_FRAMES, x)

    # 实例化OpenCV's multi-object tracker
    cap = cv2.VideoCapture('../../Envs/virtual_env/Lib/site-packages/simpleui/{}'.format(videoName))
    cv2.namedWindow("Video", cv2.WINDOW_AUTOSIZE)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # 创建滑动条
    cv2.createTrackbar("Frame", "Video", 0, int(frame_count), on_change)
    # 获取视频的fps
    # Fps = cap.get(cv2.CAP_PROP_FPS)
    trackers = cv2.MultiTracker_create()

    # 配置参数
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-v',"--video", type=str, required=False,
                        help='path to input video file')
    parser.add_argument('-t',"--tracker", default="kcf", type=str, required=False,
                        help='OpenCV object tracker type')

    args = vars(parser.parse_args(['-t', 'kcf']))  # 至少输入一个参数

    # opencv已经实现了的追踪算法
    OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.TrackerCSRT_create,
        "kcf": cv2.TrackerKCF_create,
        "boosting": cv2.TrackerBoosting_create,
        "mil": cv2.TrackerMIL_create,
        "tld": cv2.TrackerTLD_create,
        "medianflow": cv2.TrackerMedianFlow_create,
        "mosse": cv2.TrackerMOSSE_create
    }
    # 视频流
    now = datetime.date.today()
    faces = Faces.objects.filter(face_date__lt=now).order_by('-id')

    while (True):
        framePos = cap.get(cv2.CAP_PROP_POS_FRAMES)
        cv2.setTrackbarPos("Frame", "Video", int(framePos))
        # 取当前帧
        ret, frame = cap.read()

        if ret == True:
            # cv2.putText(frame, videoDate, (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255), 2)
            # resize每一帧
            (h, w) = frame.shape[:2]
            width = 600
            r = width / float(w)
            dim = (width, int(h * r))
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

            # 追踪结果
            (success, boxes) = trackers.update(frame)


            # 绘制区域
            for box in boxes:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                face_image = frame[y:y+h,x:x+w]
                # cv2.imshow("asdf",face_image)
                # print(face_encoding)


            text = "s:stop frame and select a roi\nf:find face\nesc:quit video"
            y,dy=0,20
            for i ,line in enumerate(text.split('\n')):
                y += dy
                cv2.putText(frame,line,(10,y),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),1)
            # 显示
            cv2.imshow("Video", frame)

            key = cv2.waitKey(50) & 0xFF

            if key == ord("f"):
                face_encoding = face_recognition.face_encodings(face_image)[0]
                for face in faces:
                    face_image_db = face_recognition.load_image_file(r'../../Envs/virtual_env/Lib/site-packages/simpleui/{}'.format(face.face_url))
                    face_encoding_db = face_recognition.face_encodings(face_image_db)[0]
                    # print(face_encoding_db)
                    res = face_recognition.compare_faces([face_encoding], face_encoding_db, tolerance=0.5)
                    if res == [True]:
                        cap.release()
                        cv2.destroyAllWindows()
                        # break
                        return JsonResponse({"res": "最近该人出现在{}".format(face.face_date)})
                else:
                    cap.release()
                    cv2.destroyAllWindows()
                    return JsonResponse({"res":"最近此人没有出现"})
                # break

            elif key == ord("s"):
                # 选择一个区域，按s
                box = cv2.selectROI("Video", frame, fromCenter=False,
                                    showCrosshair=True)

                # 创建一个新的追踪器
                tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
                trackers.add(tracker, frame, box)


            # 退出
            elif key == 27:
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

    return JsonResponse({"res":"查看监控完成"})
