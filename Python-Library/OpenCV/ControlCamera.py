import tempfile

import cv2
import time


# 定义摄像头类
class Camera(object):

    def __init__(self, camera: int=0, img_show: bool=False):
        """

        :param camera: 系统中摄像头的序列,一般只有一个主摄像头的话序列就是0
        """

        # 获取摄像头对象，0 系统默认摄像头
        self.cap = cv2.VideoCapture(camera)
        self.img_show = img_show
        self.camera = camera
        # 判断摄像头是否打开，没有则打开
        if not self.cap.isOpened():
            self.cap.open()

    def get_frame(self):
        """
        读取当前帧
        :return: 当前帧的image对象
        """
        ret, frame = self.cap.read()
        if ret:
            if self.img_show:
                cv2.imshow("frame", frame)
            time.sleep(5)
        return frame

    def save_video(self, file_path: str=None, length: int=10, codec: str='XVID', fps: int= 20,
                   width: int=640, height: int=480):

        # 使用camera录制指定时长的视频
        # Define the codec and create VideoWriter object
        # 视频编码
        fourcc = cv2.VideoWriter_fourcc(*codec)
        if file_path is not None:
            output_path = file_path
        else:
            output_path = tempfile.NamedTemporaryFile(suffix='video', prefix='mp4')

        # 20fps ,640*480size
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        start_time = time.time()
        while self.cap.isOpened:
            ret, frame = self.cap.read()
            if ret:
                # 翻转图片
                # frame = cv2.flip(frame,0)
                # write the flipped frame
                out.write(frame)
                if self.img_show:
                    cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
            if time.time() - start_time > length:
                break
        out.release()
        cv2.destroyAllWindows()
        return output_path

    def save_snapshot(self, file_path: str=None):

        output_path = None
        if self.cap.isOpened:
            ret, frame = self.cap.read()
            if self.img_show:
                cv2.imshow('frame', frame)
            if file_path is not None:
                output_path = file_path
            else:
                output_path = tempfile.NamedTemporaryFile(suffix='snapshot', prefix='png')
            if ret:
                cv2.imwrite(output_path, frame)
            else:
                print("save snapshot fail")
        return output_path

    def release_device(self):
        # 释放设备
        self.cap.release()

    def re_open_device(self):
        if not self.cap.isOpened():
            print("re-opened device")
            self.cap = cv2.VideoCapture(self.camera)
            if not self.cap.isOpened():
                self.cap.open()


def capture_by_camera(camera: int=0, capture_file_path: str=None, adjust_setting = False, res = (0, 0), img_show: bool=False, waiting_time: int=3):
    """
    调用摄像头拍摄一张照片
    :param camera: 摄像头序列号,0表示系统默认的摄像头
    :param capture_file_path: 图片存放路径, 没有指定路径将会使用临时文件
    :param adjust_setting: 是否需要自动曝光, 这里为了不多使用一个参数, 所以如果不使用自动曝光的话, 就需要把设定的曝光值写出来
                          比如需要曝光值为-7的, 就直接在这里设置为-7 (效果好像不太好)
    :param res: 捕捉图像的分辨率, (0, 0)表示原分辨率
    :param img_show: 捕捉后需不需要显示捕捉结果
    :param waiting_time: 捕捉前的等待时间, 一般来说设置一定的时长以免摄像头启动需要时间
    :return: 如果成功返回图片存放路径, 如果失败返回None
    """

    # 读取摄像头，0表示系统默认摄像头
    if adjust_setting:
        cap = cv2.VideoCapture(camera + cv2.CAP_DSHOW) # 很多摄像头要使用direct show来驱动摄像头才能调节大部分的参数
        cap.set(cv2.CAP_PROP_SETTINGS, 1) # 弹出参数调节窗口, 因为修改的是操作系统里预定义的摄像头参数, 所以就算脚本运行完成, 参数也一直生效
    else:
        cap = cv2.VideoCapture(camera)
    # if auto_exposure is not True:
    #     # ret_val, cap_for_exposure = cap.read()
    #     cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3) # Turn on auto exposure
    #     # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) # Turn off auto exposure
    #     # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25) # Turn off auto exposure
    #     cap.set(cv2.CAP_PROP_EXPOSURE, auto_exposure)
    # else:
    #     cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75) # Turn on auto exposure
    print(cap.get(cv2.CAP_PROP_AUTO_EXPOSURE))
    print(cap.get(cv2.CAP_PROP_EXPOSURE))
    if res[0] != 0: # 图片的大小, 注意同样也是修改操作系统预定义的摄像头参数, 就算脚本运行完成后, 图片大小也不会变回来
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # cap.set(cv2.CAP_PROP_SETTINGS, 1)
    time.sleep(waiting_time)
    ret, photo = cap.read()
    # 将图像传送至窗口
    if img_show:
        cv2.imshow('The Photo You Take', photo)

    if capture_file_path:
        filename = capture_file_path
    else:
        filename = tempfile.NamedTemporaryFile(prefix='screenshot_', suffix='.png').name
    cv2.waitKey()
    cv2.imwrite(filename, photo)
    time.sleep(2)
    cap.release()
    if ret:
        return filename
    else:
        return None


if __name__ == '__main__':
    capture_by_camera(capture_file_path="Pics/not_adjust.png")
    # time.sleep(10)
