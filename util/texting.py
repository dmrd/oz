import shlex, subprocess
import string
import random
shu_number = "8608398690" # Shubhro's number
and_number = "5712341115" # Andrew's number
dav_number = "9014386031" # 

def send_text(verify_code, from_number = "7039400683", to_number = shu_number):

    verify_code = "31415" # HARDCODED FOR NOW

    # Use Twilio to send text message to designated number with a verification code
    command = 'curl -X POST https://api.twilio.com/2010-04-01/Accounts/ACb533b2f16cfb7175609f1652181b5261/SMS/Messages.xml \
    -d "From='+from_number+'" \
    -d "To='+to_number+'" \
    -d "Body=Here+is+the+verification+code:+' + verify_code + '" \
    -u ACb533b2f16cfb7175609f1652181b5261:e54e3b9c50f16fdd75305beec3e1ed32'

    # Segment the command and run it on terminal
    args = shlex.split(command)
    p = subprocess.Popen(args)
    
def main():

    code = ''.join(random.choice(string.digits) for x in range(5))
    print code
    send_text(code)
    
if __name__ == "__main__":
    main()