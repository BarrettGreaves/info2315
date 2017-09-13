import _pickle as pickle
import os
save_name = "data1.b"
if os.path.exists(save_name):
			with open(save_name, "rb") as f:
				print(pickle.load(f))
