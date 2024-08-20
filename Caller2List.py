# Mandatory Imports
import os
import vtt
import time
import warnings
from playsound import playsound
import smtplib, ssl


# Suppress FutureWarning + Email Server Setup
warnings.simplefilter(action='ignore', category=FutureWarning)
port = 465  # For SSL
context = ssl.create_default_context()
audio_file = os.path.dirname(__file__) + '\\8000.mp3'

# Email you want to send from, MUST HAVE 2-FACTOR APPS ENABLED: https://myaccount.google.com/u/1/apppasswords   --- MUST BE A GMAIL FOR THIS TO WORK
sender_email = "your_email@gmail.com"

# Email you want to recieve notifications
receiver_email = "reciever_email"

# This is the app password for your sender_email, not the password for the account but the password from here: https://myaccount.google.com/u/1/apppasswords
# Should be 16 character
password = "your_app_password"

# List of CRNs to monitor

CRNs = ['80115', '80116', '80117', '80118', '80119', '80120'] # Add your CRNs here

# Determines if an email is sent.
shouldEmail = True

# What Message do you want to send
message_template = "Subject: CRN: {} AVAILABILITY \n\n ***********AUTOMATED NOTIFICATION***********\n\n\nCRN: {} HAS SEATS AVAILABLE\n\n\n***********AUTOMATED NOTIFICATION***********"

# Runs until terminated Manually
i = 0
delay = 3
total_time = 0
hours = 0
minutes = 0
seconds = 0
while True:
    i += 1
    start_time = time.time()
    print("\n<<<{ Run " + str(i) + " --- Time: " + "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds) + "}>>>\n")
    for CRN in CRNs:
        # Gets the course to look at
        try:
            course = vtt.get_crn('2024', vtt.Semester.FALL, CRN)
        except:
            print("An Error Occured")
            continue
        # Looks for open spots
        try:
            if course.has_open_spots():
                
                if shouldEmail:
                    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                        server.login(sender_email, password)
                        message = message_template.format(CRN, CRN)
                        server.sendmail(sender_email, receiver_email, message)
                        shouldEmail = False
                playsound(audio_file)
                print("CRN: {} HAS SEATS!!!! ENROLL!!!!".format(CRN))
            else:
                print("CRN: {} HAS NO SEATS AVAILABLE".format(CRN))
            time.sleep(delay)
        except:
            print("An Error Occured")
    end_time = time.time()
    runtime = end_time - start_time
    total_time += runtime
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    seconds = int(total_time % 60)
            