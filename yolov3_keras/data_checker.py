from PIL import Image

def check():
	error_list = []
	with open("train.txt") as f:
		for line in f:
			# print(line)
			line = line.split()
			image = 0
			try:
				image = Image.open(line[0])
			except:
				continue
			w, h = image.size
			for t in line[1:]:
				t = t.split(",")
				# print(t)
				box = []
				for i in t:
					i = int(i)
					# print(i)
					box.append(i)
				# print(box)
				if (box[0]+box[2]>=2*w or box[2]+box[4]>=2*h):
					error_list.append(line[0])
					print(line[0] + " Error!")
					break
	return error_list