#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup
from termcolor import colored

def scrape_usernames(username):
    """
    Scrape usernames from Instagram's search suggestions.
    """
    url = f"https://www.instagram.com/web/search/topsearch/?context=user&query={username}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        usernames = [username]
        similar_usernames = [user['user']['username'] for user in data['users']]
        return usernames + similar_usernames[:20]  # Limit the number of similar usernames to 20
    except requests.exceptions.RequestException as e:
        print(colored(f"Error: {e}", 'red'))
        return []

def check_passwords(usernames, passwords):
    """
    Check if any username matches with the passwords.
    """
    matched = []
    for username in usernames:
        if username in passwords:
            print(colored(f"{username}: {username} - Matched", 'green'))
            matched.append(username)
        else:
            print(colored(f"{username} - Not matched", 'red'))
    return matched

def search_instagram(query):
    """
    Perform a search on Instagram to find usernames and posts.
    """
    url = f"https://www.instagram.com/web/search/topsearch/?context=blended&query={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        usernames = [user['user']['username'] for user in data['users']]
        posts = [post['caption'] for post in data['posts']]
        return usernames, posts
    except requests.exceptions.RequestException as e:
        print(colored(f"Error: {e}", 'red'))
        return [], []

def main():
    """
    Main function to prompt user inputs and call the above functions.
    """
    username = input("Enter Instagram username or search query: ")
    password1 = input("Enter password 1: ")
    password2 = input("Enter password 2: ")
    password3 = input("Enter password 3: ")
    passwords = [password1, password2, password3]

    print("\nScraping usernames...")
    usernames = scrape_usernames(username)

    if usernames:
        print("\nChecking passwords...")
        matched_usernames = check_passwords(usernames, passwords)

        if not matched_usernames:
            print(colored("No matches found for any username-password pair.", 'red'))

            print("\nSearching Instagram...")
            search_query = input("Enter a search query: ")
            usernames, posts = search_instagram(search_query)
            if usernames or posts:
                print("\nSearch results:")
                if usernames:
                    print("\nUsernames:")
                    for username in usernames:
                        print(f"- {username}")
                if posts:
                    print("\nPosts:")
                    for post in posts:
                        print(f"- {post}")
            else:
                print(colored("No search results found.", 'red'))
    else:
        print(colored("Exiting due to error.", 'red'))

if __name__ == "__main__":
    main()
