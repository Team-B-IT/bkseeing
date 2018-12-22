from flask import Flask, request
import subprocess
import threading
import time

# label = {'Dog': 'con chó',
# 	'Cat': 'con mèo',
# 	'Human body': 'người',
# 	'Chair': 'cái ghế',
# 	'Stool': 'cái ghế đẩu',
# 	'Table': 'cái bàn',
# 	'Desk': 'bàn làm việc',
# 	'Box': 'cái thùng',
# 	'Door': 'cái cửa',
# 	'Stairs': 'cầu thang',
# 	'Shelf': 'giá sách',
# 	'Bed': 'cái giường',
# 	'Bookcase': 'kệ sách',
# 	'Countertop': 'bàn nấu ăn',
# 	'Closet': 'cái tủ',
# 	'Couch': 'cái dài',
# 	'Refrigerator': 'tủ lạnh',
# 	'Mechanical fan': 'cái quạt',
# 	'Wardrobe': 'tủ quần áo',
# 	'Filing cabinet': 'tủ treo',
# 	'Tableware': 'đồ vật trên bàn',
# 	'Others': 'đồ vật khác'}

label = {
	'Man': 'người',
	'Woman': 'người',
	'Chair': 'cái ghế',
	'Table': 'cái bàn',
	'Box': 'cái thùng',
	'Door': 'cái cửa',
	'Stairs': 'cầu thang',
	'Others': 'vật thể'
}

cmd = "python yolo_video.py --image"
p = subprocess.Popen(cmd,
	shell=True,
	bufsize=64,
	stdin=subprocess.PIPE,
	stderr=subprocess.PIPE,
	stdout=subprocess.PIPE)

readBuffer = []

def readThread():
	print("readThread start!")
	while True:
		line = p.stdout.readline().decode("utf-8").rstrip()
		if (line != ''):
			print(line)
			readBuffer.append(line)
		else:
			pass
app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def listen():
	global readBuffer
	if request.method == 'POST':
		random = int(round(time.time() * 1000)) % 10;
		image = "img" + str(random) + ".png"
		print(image)
		f = open(image, "wb")
		f.write(request.data)
		f.close()

		p.stdin.write(bytes(image + "\n", "utf-8"))
		p.stdin.flush()
		print(image)

		result = tuple(readBuffer)
		readBuffer = []
		counter = {}
		for i in result:
			for k, v in label.items():
				if i.find(k) >= 0:
					if v in counter:
						counter[v] += 1
					else:
						counter[v] = 1
		if len(counter) == 0:
			result = "Không có đồ vật nào"
		else:
			result = ''
			for k, v in counter.items():
				result += "có " + str(v) + " " + k + ", "

		print(result)
		return result.encode("utf-8")
	else:
		return "Yêu cầu không hợp lệ".encode("utf-8")


rT = threading.Thread(target = readThread)
rT.start()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)

# while True:
# 	a = 0