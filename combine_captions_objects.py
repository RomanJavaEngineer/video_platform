# Combine the captions with the object detections

import csv
from utils import returnVideoFolderName,OBJECTS_CSV,CAPTIONS_CSV,CAPTIONS_AND_OBJECTS_CSV

def combine_captions_objects(video_id):
	"""
	Outputs a csv file combining the columns of the object and caption csv files
	"""
	objcsvpath = returnVideoFolderName(video_id)+'/'+OBJECTS_CSV
	with open(objcsvpath, newline='', encoding='utf-8') as objcsvfile:
		reader = csv.reader(objcsvfile)
		objheader = next(reader) # skip header
		objrows = [row for row in reader]
	
	captcsvpath = returnVideoFolderName(video_id)+'/'+CAPTIONS_CSV
	with open(captcsvpath, newline='', encoding='utf-8') as captcsvfile:
		reader = csv.reader(captcsvfile)
		captheader = next(reader) # skip header
		captrows = [row for row in reader]
	
	outcsvpath = returnVideoFolderName(video_id)+'/'+CAPTIONS_AND_OBJECTS_CSV
	with open(outcsvpath, 'w', newline='', encoding='utf-8') as outcsvfile:
		writer = csv.writer(outcsvfile)
		header = captheader + objheader[1:]
		writer.writerow(header)
		for index in range(len(objrows)):
			new_row = captrows[index] + objrows[index][1:]
			print(captrows[index])
			writer.writerow(new_row)

if __name__ == "__main__":
	# video_name = 'A dog collapses and faints right in front of us I have never seen anything like it'
	# combine_captions_objects(video_name)
	# video_name = 'Good Samaritans knew that this puppy needed extra help'
	# combine_captions_objects(video_name)
	# video_name = 'Hope For Paws Stray dog walks into a yard and then collapses'
	# combine_captions_objects(video_name)
	# video_name = 'This rescue was amazing - Im so happy I caught it on camera!!!'
	# combine_captions_objects(video_name)
	# video_name = 'Oh wow this rescue turned to be INTENSE as the dog was fighting for her life!!!'
	# combine_captions_objects(video_name)
	# video_name = 'Hope For Paws_ A homeless dog living in a trash pile gets rescued, and then does something amazing!'
	# combine_captions_objects(video_name)
	video_name = 'Homeless German Shepherd cries like a human!  I have never heard anything like this!!!'
	combine_captions_objects(video_name)