import requests

BASE_URL = "http://127.0.0.1:8000/api"

def register():
    print('--- Register ---')
    username = input('Username: ')
    password = input('Password: ')
    email = input('Email: ')
    
    data = {
        'username': username,
        'password': password,
        'email': email
    }
    
    response = requests.post(f"{BASE_URL}/register/", data=data)
    
    if response.status_code == 201:
        print('Registration successful')
    else:
        print('Registration failed:', response.json())

def login():
    print('--- Login ---')
    username = input('Username: ')
    password = input('Password: ')
    
    data = {
        'username': username,
        'password': password
    }
    
    response = requests.post(f"{BASE_URL}/login/", data=data)
    
    if response.status_code == 200:
        print('Login successful')
        token = response.json().get('token')
        return token
    else:
        print('Login failed:', response.json())
        return None

def favlinks():
    print('---- Welcome to FavLinks App ----')
    print('- Please choose option below -')
    print('[1] Register')
    print('[2] Login')
    
    choice = input('Enter choice: ')
    
    if choice == '1':
        register()
    elif choice == '2':
        token = login()
        if token:
            while True:
                print('---- FavLinks Menu ----')
                print('[1] List Favorite URLs')
                print('[2] Create Favorite URL')
                print('[3] Filter Favorite URLs by Category')
                print('[4] Filter Favorite URLs by Tags')
                print('[5] Logout')
                
                sub_choice = input('Enter choice: ')
                
                if sub_choice == '1':
                    list_favorite_urls(token)
                elif sub_choice == '2':
                    create_favorite_url(token)
                elif sub_choice == '3':
                    filter_by_category(token)
                elif sub_choice == '4':
                    filter_by_tags(token)
                elif sub_choice == '5':
                    print('Logged out')
                    break
                else:
                    print('Invalid choice, please try again.')
    else:
        print('Invalid choice, please try again.')

def list_favorite_urls(token):
    response = requests.get(f"{BASE_URL}/list_favlinks/", headers={'Authorization': f'Token {token}'})
    if response.status_code == 200:
        urls = response.json()
        for url in urls:
            print(f"Title: {url['title']}, URL: {url['url']}, Is Valid: {url['is_valid']}")
        print(urls)
    else:
        print('Failed to retrieve favorite URLs:', response.json())

def create_favorite_url(token):
    print('--- Create Favorite URL ---')
    title = input('Title: ')
    url = input('URL: ')
    category_id = input('Category ID: ')
    tag_ids = input('Tag IDs (comma separated): ').split(',')
    
    data = {
        'title': title,
        'url': 'https://www.'+url,
        'category': category_id,
        'tags': tag_ids
    }
    
    response = requests.post(f"{BASE_URL}/create_favlink/", headers={'Authorization': f'Token {token}'}, json=data)
    
    if response.status_code == 201:
        print('Favorite URL created successfully')
    else:
        print('Failed to create favorite URL:', response.json())

def filter_by_category(token):
    category_id = input('Enter Category ID: ')
    response = requests.get(f"{BASE_URL}/favorite_urls/?category_id={category_id}", headers={'Authorization': f'Token {token}'})
    if response.status_code == 200:
        urls = response.json()
        for url in urls:
            print(f"Title: {url['title']}, URL: {url['url']}, Is Valid: {url['is_valid']}")
    else:
        print('Failed to retrieve favorite URLs:', response.json())

def filter_by_tags(token):
    tag_ids = input('Enter Tag IDs (comma separated): ').split(',')
    tag_params = '&'.join([f'tag_ids={tag_id}' for tag_id in tag_ids])
    response = requests.get(f"{BASE_URL}/favorite_urls/?{tag_params}", headers={'Authorization': f'Token {token}'})
    if response.status_code == 200:
        urls = response.json()
        for url in urls:
            print(f"Title: {url['title']}, URL: {url['url']}, Is Valid: {url['is_valid']}")
    else:
        print('Failed to retrieve favorite URLs:', response.json())

if __name__ == "__main__":
    favlinks()
