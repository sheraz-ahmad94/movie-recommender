import requests
import json

BASE_URL = 'https://api.themoviedb.org/3'


def print_genre():
    print("Pick a Genre to Start:")
    print("1. Action")
    print("2. Comedy")
    print("3. Drama")
    print("4. Horror")
    print("5. Sci-Fi")

def print_menu():
    print("-" * 20)
    print("Movie Recommender")
    print("-" * 20)
    print("1. Search Movie By Name")
    print("2. Get Recommendations")

def display_search_results(data):
    print("Page:", data['page'])

    count = len(data['results'])

    for i in range(count):
        title = data['results'][i]['title']     
        overview = data['results'][i]['overview']  
        released_date =  data['results'][i]['release_date']  
        language = data['results'][i]['original_language']
        vote_average = data['results'][i]['vote_average'] 

        print("-" * 20)
        print(f"{i+1}. {title}")
        print("-" * 20)
        print(f"Description: {overview}\n")
        print(f"Released Date: {released_date}\n")
        print(f"Original Language: {language}\n")
        print(f"Average Votes: {vote_average}")
        print("-" * 50)

def print_other_filters():
    print("Select Other Filters (Enter q to Get Recommendations): ")
    print("1. Actors")
    print("2. Release Year")
    print("3. Minimum Vote Average")
    print("4: Keyword")
    print("5: Show Recommendations")

def add_genre_to_url(url, genre):
    new_url = url + f"&with_genres={genre}"
    return new_url

def add_other_filters_to_url(url, filter_type, user_input):
    new_url = url + f"&{filter_type}={user_input}"
    return new_url

auth_url = f"{BASE_URL}/authentication"
header = {
    "accept": 'application/json',
    "Authorization": "Bearer PASTE_YOUR_API_READ_ACCESS_TOKEN_HERE"
}

response = requests.get(auth_url, headers=header)

if response.status_code == 200:
    print_menu()
    option = int(input("Select: "))
    if option == 1:
        movie_name = input("Enter Movie Name: ")
        url = f"{BASE_URL}/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"
        search_response = requests.get(url, headers=header)
        data = search_response.json()
        display_search_results(data)
    
    elif option == 2:
        url = f"{BASE_URL}/discover/movie?include_adult=false&language=en-US&page=1&sort_by=popularity.desc"
        print_genre()
        select = int(input("Select: "))
        if select == 1:
            genre = "action"
            url = add_genre_to_url(url, genre)
        elif select == 2:
            genre = "comedy"
            url = add_genre_to_url(url, genre)
        elif select == 3:
            genre = "drama"
            url = add_genre_to_url(url, genre)
        elif select == 4:
            genre = "horror"
            url = add_genre_to_url(url, genre)
        elif select == 5:
            genre = "sci-fi"
            url = add_genre_to_url(url, genre)
        else:
            print("Error! Wrong Input.")

        flag_actors = 0
        flag_year = 0
        flag_vote = 0
        flag_keyword = 0

        while True:
            print_other_filters()
            filter_option = input("Select: ")
        
            if filter_option == '1':
                if flag_actors == 0:
                    add_filter_actor = input("Enter Actors (Separated by Comma): ")
                    url = add_other_filters_to_url(url, "with_cast", add_filter_actor)
                    flag_actors = 1
                else:
                    print("Already Entered")
            
            elif filter_option == '2':
                if flag_year == 0:
                    add_filter_year = int(input("Enter The Release Year: "))
                    url = add_other_filters_to_url(url, "year", add_filter_year)
                    flag_year = 1
                else:
                    print("Already Entered")
            
            elif filter_option == '3':
                if flag_vote == 0:
                    add_filter_vote_average = float(input("Enter Minimum Vote Average: "))
                    url = add_other_filters_to_url(url, "vote_count.gte", add_filter_vote_average)
                    flag_vote = 1
                else:
                    print("Already Entered")

            elif filter_option == '4':
                if flag_keyword == 0:
                    add_filter_keyword = input("Enter a Keyword (Separated by Comma): ")
                    url = add_other_filters_to_url(url, "with_keywords", add_filter_keyword)
                    flag_keyword = 1
                else:
                    print("Already Entered")

            elif filter_option == '5':
                break            
            else:
                print("Error! Wrong Input.")
        
        discovery_response = requests.get(url, headers=header)
        data = discovery_response.json()
        display_search_results(data)
        

    else:
        print("Error! Wrong Input.")
else:
    print("Error! Could Not Connect to the Website!")