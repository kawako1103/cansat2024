import pynmea2 

def extract_substring(line):
	start_index = 1
	end_index = line.find(",")
	if end_index != -1:
		substring = line[start_index:end_index]
		return substring
	else:
		return None
			

with open("log_rawstring.txt", "r") as file:
	for line in file:
		msg_code = extract_substring(line)
		if msg_code == "GNGGA":
			msg = pynmea2.parse(line)
			print(msg.lat,end=", ")
			print(msg.lon)
		else:
			print(".",end="")

