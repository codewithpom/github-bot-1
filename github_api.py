import requests
from bs4 import BeautifulSoup as sp


url = "https://api.github.com/users/"
search_url = "https://github.com/search?q="

def user_data(user):
    

    user_url = url + user

    data = requests.get(user_url).json()
    try:
        public_repos = data['public_repos']

        public_gists = data['public_gists']
        user_bio = data['bio']
        avatar = data['avatar_url']
        return {'repos': public_repos, 'gists': public_gists, 'bio': user_bio, 'url': avatar}
    except Exception:
        return False
    # print(f"He/She has {public_repos} public repositories")

    # print(f"He/She has {public_gists} public repositories")

    # print(f"His/Her bio is {user_bio}")

def repos(username):
    data = requests.get(url + username + "/repos").json()
    finished_data = []
    for i in data:
        try:
            name = i['name']
            description = i['description']
            clone_url = i['clone_url']
            language = i['language']
            forks_count = i['forks_count']
            to_be_added = {'name': name, 'desc': description, 'clone': clone_url, 'lang': language, 'forks': forks_count}
            finished_data.append(to_be_added)
        except Exception:
            return False

    return finished_data

def search(query: str):
    query = query.replace(" ", "+")
    complete_url = search_url + query
    data = requests.get(complete_url).text
    soup = sp(data, 'html.parser')
    ul = soup.find('ul', class_="repo-list")
    lis = ul.find_all('li')
    finished_data = []
    for i in lis:
        title = i.find('a').text
        try:
            des = i.find('p', class_="mb-1").text.strip()
        except Exception as e:
            pass
        link_href = i.find('a')['href']
        language = i.find('span', itemprop="programmingLanguage").text
        to_be_put = {'title': title, 'des': des, 'lang': language, 'href': link_href}
        finished_data.append(to_be_put)
    
    return finished_data
'''
data = search("cargame in python")

for i in data:
    print(i['title'].split("/")[1])
    print(i['des'])
    print(i['lang'])
    print("https://github.com" + i['href'])

'''




