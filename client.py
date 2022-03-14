import requests
import jwt
 
login = input("Do you have a token? (y/n)")
 
if(login == 'y'):
        token = input("Enter your token: ")
        
        try:
                
                payload = jwt.decode(token, verify=False)
                print("Access granted {}".format(payload['account_number']))
                print("You're token: ", token)
        except:
                print("Something is wrong with token")
        r = requests.get("http://127.0.0.1:8000/", params={'token': token})
        
        print("Request method: GET, Response status_code: {}, Response data: {}".format(r.status_code, r.text))
 
elif(login == 'n'):
        account_number = input("Enter your account number: ")
        password = input("Enter your client password: ")
    
        r = requests.post("http://127.0.0.1:8000/", params = {'account_number': account_number, 'password': password})
        print("Request method: POST, Response status_code: {}, Response data: {}".format(r.status_code, r.text))
        print("Copy and save your token!")
else:
        print("Wrong action")
