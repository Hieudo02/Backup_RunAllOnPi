#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from PIL import Image
import os
import rospy
import threading
import signal
from std_msgs.msg import String
import subprocess
from actionlib_msgs.msg import GoalStatusArray

# Assuming your script is located in /home/hieudo/datn_navbot/src/navstack_pub/webServer/RobotControl
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
IMAGE_FOLDER = os.path.join(BASE_DIR, 'maps')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pgm'}

v_r = 1.0
v_l = 1.0
MAX_SPEED = 0.3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_pgm(image_path):
    with Image.open(image_path) as img:
        gray_img = img.convert('L')
        binary_img = gray_img.point(lambda p: p > 128 and 255)
        pgm_path = image_path.rsplit('.', 1)[0] + '.pgm'
        binary_img.save(pgm_path)
    return pgm_path

def convert_pgm_to_png(pgm_path):
    with Image.open(pgm_path) as img:
        png_path = pgm_path.rsplit('.', 1)[0] + '.png'
        img.save(png_path)
    return png_path

goalReachFlag = False
def goalStatusCallback(msg):
    global goalReachFlag
    for status in msg.status_list:
        if status.status == 3:  # 3 corresponds to 'Goal reached' in actionlib_msgs/GoalStatus
            rospy.loginfo("Goal reached!")

            goalReachFlag = True



@app.route('/', methods=['GET', 'POST'])
def index():
    global v_r
    global v_l 
    global MAX_SPEED
    resolution = 0.05
    if request.method == 'POST':
        if 'file' in request.files and 'resolution' in request.form:
            file = request.files['file']
            uploadImgResolution = request.form['uploadResolution']
            if file.filename != '' and allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filename)
                
                pgm_filename = convert_to_pgm(filename)

                points = []
                for key in request.form:
                    if key.startswith('points'):
                        index = key[key.find('[')+1:key.find(']')]
                        if key.endswith('[x]'):
                            if len(points) <= int(index):
                                points.append({})
                            points[int(index)]['x'] = request.form[key]
                        elif key.endswith('[y]'):
                            if len(points) <= int(index):
                                points.append({})
                            points[int(index)]['y'] = request.form[key]

                print('Uploaded file:', pgm_filename)
                print('Resolution:', uploadImgResolution)
                print('Points:', points)
                return jsonify({'url': url_for('uploaded_file', filename=os.path.basename(filename))})
        
        if request.json:
            data = request.json
            if 'direction' in data:
                direction = data['direction'] 
                print('Received direction:', direction)
                if direction == 'w':
                    message = f"{v_r * MAX_SPEED},{v_l * MAX_SPEED}"
                    pub.publish(message)
                elif direction == 'a':
                    message = f"{v_r * MAX_SPEED},{v_l * (-1.0) * MAX_SPEED}"
                    pub.publish(message)
                elif direction == 'x':
                    message = f"{v_r * (-1.0) * MAX_SPEED},{v_l * (-1.0) * MAX_SPEED}"
                    pub.publish(message)
                elif direction == 'd':
                    message = f"{v_r * (-1.0) * MAX_SPEED},{v_l * MAX_SPEED}"
                    pub.publish(message)
                elif direction == 's':
                    pub.publish("0,0")

                # increase    
                elif direction == 'e':
                    MAX_SPEED *= 1.1
                    print("Currently speed: ", MAX_SPEED)
                # decrease
                elif direction == 'r':
                    MAX_SPEED *= 0.9
                    print("Currently speed: ", MAX_SPEED)

                return jsonify({'status': 'success'})
            if 'selected_image' in data:
                selected_map = data['selected_image']
                selectImgResolution = float(data['resolution'])
                print('Selected image:', selected_map)
                print('Received resolution:', selectImgResolution)

                map_name = selected_map.split('.')[0] + ".yaml"
                print('map name:', map_name)
                try:
                    pass
                    subprocess.run(["/home/pi/datn.sh", map_name], check=True)
                    # subprocess.run(["/home/pi/test.sh", map_name], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error occurred while executing script: {e}")
                
                return jsonify({'status': 'success', 'selected_image': selected_map , 'resolution': selectImgResolution})
        
            if 'command' in data and data['command'] == 'g':
                print('Command:', data['command'])
                
                points = data['points']
                print('Points:', points)

                # point_extract = points[0]
                # print('Point extracted:', point_extract)

                # point_x = points[0]['x']
                # print('Point x:', point_x)
                # point_y = points[0]['y']
                # print('Point y:', point_y)

                # num = 0
                # for point in points:
                #     x_value = point['x']
                #     y_value = point['y']
                #     print(f"x{num}: {x_value}, y{num}: {y_value}")

                #     try:
                #         subprocess.run(["/home/pi/sendGoal.sh", x_value, y_value], check=True)
                #     except subprocess.CalledProcessError as e:
                #         print(f"Error occurred while executing script: {e}")

                #     num += 1


                num = 0
                global goalReachFlag
                point_x = points[num]['x']
                point_y = points[num]['y']
                print(f"x{num}: {point_x}, y{num}: {point_y}")
                try:
                    subprocess.run(["/home/pi/sendGoal.sh", point_x, point_y], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error occurred while executing script: {e}")
                if (goalReachFlag == True):
                    num += 1
                    goalReachFlag = False

                return jsonify({'status': 'success', 'command': data['command'], 'points': points})
            return jsonify({'status': 'success'})
        return jsonify({'status': 'failure'})
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/list_images')
def list_images():
    images = [f for f in os.listdir(app.config['IMAGE_FOLDER']) if f.endswith('.pgm')]
    # print("Images found:", images)
    return jsonify(images)

@app.route('/maps/<filename>')
def get_image(filename):
    if filename.endswith('.pgm'):
        png_filename = convert_pgm_to_png(os.path.join(app.config['IMAGE_FOLDER'], filename))
        filename = os.path.basename(png_filename)
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

@app.route('/coordinates', methods=['POST'])
def receive_coordinates():
    data = request.json
    print('Received coordinates:', data)
    return jsonify({'status': 'success', 'received_coordinates': data})

def flask_thread():
    app.run(host='0.0.0.0', port=5000)

def signal_handler(sig, frame):
    print("Shutting down...")
    os._exit(0)

def main():
    global pub
    signal.signal(signal.SIGINT, signal_handler)

    rospy.init_node('web_server_control', anonymous=True)
    rospy.Subscriber('/move_base/status', GoalStatusArray, goalStatusCallback)
    pub = rospy.Publisher('manual_control', String, queue_size=10)

    flask_thread_instance = threading.Thread(target=flask_thread)
    flask_thread_instance.start()

    rospy.spin()
    flask_thread_instance.join()

if __name__ == '__main__':
    main()
