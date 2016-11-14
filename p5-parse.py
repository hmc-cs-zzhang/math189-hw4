import os
import shutil

dirname = "reuters21578"
filenames = sorted([os.path.join(dirname, fn) for fn in os.listdir(dirname) if fn.endswith(".sgm")])
output_dir = "samples"

count = 0

def save_content(content):
	global count
	name = os.path.join(output_dir, "samples-" + str(count) + ".txt")
	count += 1
	with open(name, 'w') as fn:
		fn.write(content)

def parse_file(content):
	i = 0
	ans = []
	while i < len(content):
		j = i
		while j < len(content) and content[j] != '<':
			j += 1
		if j + 6 <= len(content) and content[j:j + 6] == "<BODY>":
			k = j + 6
			while k < len(content) and content[k] != '<':
				k += 1
			if k + 7 <= len(content) and content[k:k + 7] == "</BODY>":
				# Get rid of "\n&#3;"
				e = k - 5
				# Get rid of "\n Reuter"				
				if content[e - 6:e].lower() == "reuter":
					e -= 8
				save_content(content[j + 6:e])
			j = k + 7
		i = j + 1

# Create output directory
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for fn in filenames:
	with open(fn) as fd:
		parse_file(fd.read())
