import requests
from threading import Thread
import time

# image_id = ".jpg"
# image_url = "https://scontent.fhan2-2.fna.fbcdn.net/v/t1.0-9/45433161_554499801676304_8102724591547318272_n.jpg?_nc_cat=111&_nc_ht=scontent.fhan2-2.fna&oh=89bc0c31bcb8b7a87c82dbc3a3ba574a&oe=5C7C04DA"

def DownloadFile(image_id, image_url):
	local_filename = image_id
	r = requests.get(image_url)
	f = open(local_filename, 'wb')
	for chunk in r.iter_content(chunk_size=512 * 1024):
		if (chunk):
			f.write(chunk)
	f.close()
	print("Download", local_filename, "successful!")
	return

with open("ei.csv") as file:
	file.readline()
	for line in file:
		ii = line.split(',')
		print(ii)
		if ii[1][0] != 'h':
			continue
		image_id = './images/' + ii[0] + ".jpg"
		image_url = ii[1]
		# DownloadFile(image_id, image_url)
		my_thread = Thread(target = DownloadFile, args = (image_id, image_url))
		my_thread.start()
		# my_thread.join()
