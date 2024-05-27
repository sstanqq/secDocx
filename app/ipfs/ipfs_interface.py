import requests
from dotenv import load_dotenv
import os

load_dotenv()
JWT_TOKEN = os.getenv('PINATA_JWT_TOKEN') 

def check_pinata_connection(jwt_token=JWT_TOKEN):
    url = "https://api.pinata.cloud/data/testAuthentication"

    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        return True 
    
    return False

def upload_file_to_pinata(filepath, jwt_token=JWT_TOKEN):
    url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
    headers = {
        "Authorization": f"Bearer {jwt_token}"
    } 

    with open(filepath, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files, headers=headers)

    if response.ok:
        return response.json()
    else:
        try:
            error_json = response.json() 

            return error_json
        except ValueError:  
            print("Произошла ошибка при загрузке файла в IPFS:", response.text)
        
        return None


def download_file_from_pinata(filepath, ipfs_hash, jwt_token=JWT_TOKEN):
    url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"

    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"Файл успешно скачан из IPFS и сохранен по пути: {filepath}")
        return True
    else:
        try:
            error_json = response.json()
            return error_json
        except ValueError:
            print("Произошла ошибка при скачивании файла из IPFS:", response.text) 

        return None 

def delete_file_from_pinate(ipfs_hash, jwt_token=JWT_TOKEN):
    url = f"https://api.pinata.cloud/pinning/unpin/{ipfs_hash}"
    headers = {
        "Authorization": f"Bearer {jwt_token}"
    } 

    response = requests.delete(url, headers=headers)

    if response.ok:
            return response
    else:
        try:
            error_json = response.json() 
            print("Произошла ошибка при удалении файла в IPFS:")
            return error_json
        except ValueError:  
            print("Произошла ошибка при удалении файла в IPFS:", response.text)
        return None

def test():
    file_path = 'temp/av.jpg'
    download_path = 'temp/test.png'
    jwt_token = os.getenv('PINATA_JWT_TOKEN') 

    if not check_pinata_connection(jwt_token):
        return False 
    
    # response = upload_file_to_pinata(file_path, jwt_token)
    # print(response)
    # response = download_file_from_pinata(download_path, 'QmQn6aeaMy5ueUNeyon8pUpFJJoaKfzxbAKjkUzC4r1dt7', jwt_token)
    # print(response)
    # response = delete_file_from_pinate('QmNuxts58UqMFdhYBia4GY3WZknT3Tf3FzydLbXkKvqzpu', jwt_token)
    # print(response)


# test()