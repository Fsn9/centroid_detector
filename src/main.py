import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from tkinter.simpledialog import askinteger
import csv
import datetime, time

class Centroid():
	def __init__(self, x, y, label):
		self.__x, self.__y, self.__label = x, y, label
	@property
	def x(self):
		return self.__x
	@property
	def y(self):
		return self.__y
	@property
	def label(self):
		return self.__label
	@x.setter
	def x(self, x):
		self.__x = x
	@y.setter
	def y(self, y):
		self.__y = y
	@label.setter
	def label(self, label):
		self.__label = label
	def update(self, x, y, label):
		self.__x, self.__y, self.__label = x, y, label

class App(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		# Building the GUI
		self.parent.title("dataset_generator")
		self.width, self.height = 640, 480
		self.button_height = 50
		self.parent.geometry(str(self.width)+"x"+str(self.height + self.button_height))

		# Canvas
		self.canvas = tk.Canvas(width = self.width, height = self.height)
		self.canvas.grid(row = 0, column = 0, columnspan = 1, sticky = tk.W + tk.E + tk.N + tk.S)
		self.centroid_circle_radius = 10
		self.centroid_circle_width = 5
		self.canvas_centroid_ovals = []

		## Image
		self.img = []
		self.generate_random_image()
		self.img_obj = self.canvas.create_image(0,0,anchor = tk.NW, image = self.img)
		self.canvas.bind('<Button-1>', self.cursor_callback)

		# Buttons
		## Next image
		self.button_next = tk.Button(text = "Export and Generate Next image", command = self.next_image_callback)
		self.button_next.grid(row = 1, column = 0, sticky = tk.W + tk.E + tk.N + tk.S)
		print(self.button_next.__dict__)

		# Current centroid
		self.__centroid = Centroid(0,0,0)

		# Add header to csv file
		self.__time_string = datetime.datetime.fromtimestamp(time.time()).strftime("%Y_%m_%d_%H_%M_%S")
		self.__dataset_filename = 'data-' + self.__time_string
		with open(self.__dataset_filename + '.csv', 'a') as dataset_file_obj:
			writer_obj = csv.writer(dataset_file_obj)
			writer_obj.writerow(["x", "y", "label"])


	def cursor_callback(self, e):
		print(f'x,y: {e.x},{e.y}')
		centroid_xy = e.x, e.y
		centroid_class = askinteger("Labelling the centroid class", "Enter an integer")
		if type(centroid_class) != int:
			tk.messagebox.showerror('Value Error', 'Error: Centroid class must be an integer')
		self.__centroid.update(e.x, e.y, centroid_class)
		x0 = e.x - self.centroid_circle_radius
		y0 = e.y - self.centroid_circle_radius
		x1 = e.x + self.centroid_circle_radius
		y1 = e.y + self.centroid_circle_radius
		self.canvas_centroid_ovals.append(self.canvas.create_oval(x0, y0, x1, y1, fill = "red", outline = "black", width = self.centroid_circle_width))

	def next_image_callback(self):
		for oval in self.canvas_centroid_ovals:
			self.canvas.delete(oval)
		del self.canvas_centroid_ovals[:]
		with open(self.__dataset_filename + '.csv', 'a') as dataset_file_obj:
			writer_obj = csv.writer(dataset_file_obj)
			writer_obj.writerow([self.__centroid.x, self.__centroid.y, self.__centroid.label])
		self.generate_random_image()
		self.canvas.itemconfig(self.img_obj, image = self.img)

	def generate_random_image(self):
		self.img = ImageTk.PhotoImage(Image.fromarray(np.random.randint(255, size = (self.height, self.width, 3), dtype = np.uint8)))

if __name__ == "__main__":
	root = tk.Tk()
	App(root)
	root.mainloop()
