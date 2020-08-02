#!/usr/bin/python
import os
#import pprint


backup_file_size_dict = {} #dictonary exam. {backup.tar.gz: size}
content_folder_size = {} #dictonary exam. {content_folder_name: size}

# adding key:value in backup_file_size_dict
for dir_path, dir_names, file_names in os.walk("."):
	for f in file_names:
		if f.endswith('tar.gz'): #or f.endswith('tar.bz2'):
			file_path = os.path.join(dir_path, f)
			backup_size = os.stat(file_path).st_size
			backup_file_size_dict[f] = backup_size

# summing sizes all files, without "virtualmin-backup" directory
for dir_path, dir_names, file_names in os.walk("."):
	for d in dir_names:
		fold_total_size = 0
		if d == 'virtualmin-backup': #detecting v_host's folder in /home
			for sub_dir_path, sub_dir_names, sub_file_names in os.walk(dir_path):
				if sub_dir_path.endswith('virtualmin-backup'): #skip "virtualmin-backup" directory
					continue
				else:
					for f in sub_file_names:
						fp = os.path.join(sub_dir_path, f)
						if not os.path.islink(fp):
							fold_total_size += os.path.getsize(fp)
			content_folder_size[os.path.basename(dir_path)] = fold_total_size


#pprint.pprint(backup_file_size_dict)
#pprint.pprint(content_folder_size)


# comparing backup file size and content folder size
for v_host in content_folder_size:
	for backup in backup_file_size_dict:
		if backup.startswith(v_host + '.') and backup_file_size_dict[backup] > content_folder_size[v_host]*80/100: # 80%
			print("\033[91m {}\033[00m".format('WARNING!!!'))
			out = (v_host, "size =", content_folder_size[v_host], "Bytes", "less than", backup, "size =",
				  backup_file_size_dict[backup], "Bytes")
			for i in out:
				print(i, end=' ')
