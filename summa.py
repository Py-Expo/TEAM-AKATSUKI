import cv2
import numpy as np

class LaneDetect:
    def __init__(self, start_frame):
        self.curr_frame = cv2.resize(start_frame, (480, 320))  # Resize the input frame
        self.temp = np.zeros_like(self.curr_frame)
        self.temp2 = np.zeros_like(self.curr_frame)
        self.vanishing_pt = self.curr_frame.shape[0] // 2
        self.roi_rows = self.curr_frame.shape[0] - self.vanishing_pt
        self.min_size = int(0.00015 * (self.curr_frame.shape[0] * self.curr_frame.shape[1]))
        self.max_lane_width = int(0.025 * self.curr_frame.shape[1])
        self.small_lane_area = 7 * self.min_size
        self.long_lane = int(0.3 * self.curr_frame.shape[0])
        self.ratio = 4
        self.vertical_left = 2 * self.curr_frame.shape[1] // 5
        self.vertical_right = 3 * self.curr_frame.shape[1] // 5
        self.vertical_top = 2 * self.curr_frame.shape[0] // 3

    def update_sensitivity(self):
        pass  # Add your implementation here

    def get_lane(self):
        self.mark_lane()
        self.blob_removal()

    def mark_lane(self):
        for i in range(self.vanishing_pt, self.curr_frame.shape[0]):
            lane_width = 5 + self.max_lane_width * (i - self.vanishing_pt) / self.roi_rows
            for j in range(lane_width, self.curr_frame.shape[1] - lane_width):
                diff_l = self.curr_frame[i, j] - self.curr_frame[i, j - lane_width]
                diff_r = self.curr_frame[i, j] - self.curr_frame[i, j + lane_width]
                diff = diff_l + diff_r - abs(diff_l - diff_r)
                diff_thresh_low = self.curr_frame[i, j] >> 1

                if diff_l > 0 and diff_r > 0 and diff > 5:
                    if diff >= diff_thresh_low:
                        self.temp[i, j] = 255

    def blob_removal(self):
        self.mark_lane()

        contours, _ = cv2.findContours(self.temp, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            contour_area = cv2.contourArea(contour)
            if contour_area > self.min_size:
                rotated_rect = cv2.minAreaRect(contour)
                sz = rotated_rect[1]
                bounding_width = sz[0]
                bounding_length = sz[1]
                blob_angle_deg = rotated_rect[2]

                if bounding_width < bounding_length:
                    blob_angle_deg = 90 + blob_angle_deg

                if (bounding_length > self.long_lane or bounding_width > self.long_lane or
                        (self.vertical_top < self.vertical_top and
                         self.vertical_left < rotated_rect[0][0] < self.vertical_right)):
                    cv2.drawContours(self.curr_frame, [contour], 0, 255, -1)
                    cv2.drawContours(self.temp2, [contour], 0, 255, -1)
                elif (-10 < blob_angle_deg < 10 or
                        (blob_angle_deg > -70 and blob_angle_deg < 70)):
                    if (bounding_length / bounding_width >= self.ratio or
                            bounding_width / bounding_length >= self.ratio or
                            (contour_area < self.small_lane_area and
                             ((contour_area / (bounding_width * bounding_length)) > 0.75) and
                             ((bounding_length / bounding_width) >= 2 or
                              (bounding_width / bounding_length) >= 2))):
                        cv2.drawContours(self.curr_frame, [contour], 0, 255, -1)
                        cv2.drawContours(self.temp2, [contour], 0, 255, -1)

    def next_frame(self, nxt):
        self.curr_frame = cv2.resize(nxt, (480, 320))
        self.get_lane()

def make_from_vid(path):
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        print("Cannot open the video file")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Input video's Frame per seconds :", fps)

    _, frame = cap.read()
    detect = LaneDetect(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot read the frame from video file")
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detect.next_frame(gray_frame)

        cv2.imshow("lane", detect.curr_frame)
        cv2.imshow("midstep", detect.temp)
        cv2.imshow("laneBlobs", detect.temp2)

        if cv2.waitKey(10) == 27:
            print("Video paused! Press 'q' to quit, any other key to continue")
            if cv2.waitKey(0) == ord('q'):
                print("Terminated by user")
                break

    cap.release()
    cv2.destroyAllWindows()

def main():
    make_from_vid("/home/yash/opencv-2.4.10/programs/output.avi")

if __name__ == "__main__":
    main()
