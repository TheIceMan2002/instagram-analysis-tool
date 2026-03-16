import json

def find_non_followers(followers_file, following_file):
    """
    Compare followers and following lists to find accounts not following back.

    Args:
        followers_file: Path to followers JSON file
        following_file: Path to following JSON file
    """

    # Load followers data with error handling
    with open(followers_file, 'r' , encoding='utf-8', errors='ignore') as f:
        followers_data = json.load(f)

    # Load following data with error handling
    with open(following_file, 'r' , encoding='utf-8', errors='ignore') as f:
        following_data = json.load(f)

    # Extract usernames from followers (handle different formats)
    followers = set()
    for item in followers_data:
        if 'string_list_data' in item:
            for user in item['string_list_data']:
                # Try different possible keys
                if 'value' in user:
                    followers.add(user['value'])
                elif 'href' in user:
                    # Extract username from URL
                    username = user['href'].splif('/')[-2]
                    followers.add(username)

    # Extract usernames from following (handle different formats)
    following = set()
    # Check if data has 'relationships_following' wrapper
    if 'relationships_following' in following_data:
        following_list = following_data['relationships_following']
        # Each item has a 'title' field with the username
        for item in following_list:
            if 'title' in item:
                following.add(item['title'])
    
    else:
        # Fallback to old format
        for item in following_data:
            if 'string_list_data' in item:
                for user in item['string_list_data']:
                    if 'value' in user:
                        following.add(user['value'])
                    elif 'href' in user:
                        username = user['href'].split('/')[-1]
                        following.add(username)
    

    # Find who you follow but not following back
    not_following_back = following - followers

    # Display results
    print(f"\n{'='*60}")
    print(f"INSTAGRAM NON-FOLLOWERS ANALYSIS")
    print(f"{'='*60}\n")
    print(f"Total accounts you follow: {len(following)}")
    print(f"Total followers: {len(followers)}")
    print(f"Accounts not following you back: {len(not_following_back)}")

    if not_following_back:
        print(f"{'='*60}")
        print("ACCOUNTS NOT FOLLOWING YOU BACK:")
        print(f"{'='*60}\n")
        for username in sorted(not_following_back):
            print(f"   . {username}")
    
    else:
        print("Everyone you follow is following you back!")
    
    print(f"\n{'='*60}\n")

    return not_following_back

if __name__ == "__main__":
    print("\nTo use this script")
    print("1. Go to Instagram > Settings > Account Center > Your Information and Permissions >\n Export your informaiton")
    print("2. Request a download in JSON format")
    print("3. Extract the ZIP file you receieve")
    print("4. Find 'followers_1.json' and 'following.json' files")
    print("5. Update the file paths below\n")

    # Path to files
    followers_file = "C:/Users/benja/Instagram_Script/instagram-benbryant0-2025-12-20-HlfJXzYB\connections/followers_and_following/followers_1.json"
    following_file = "C:/Users/benja/Instagram_Script/instagram-benbryant0-2025-12-20-HlfJXzYB\connections/followers_and_following/following.json"

    
    try:
        non_followers = find_non_followers(followers_file, following_file)

        # Save to file
        save = input("\nSave results to file? (y/n): ")
        if save.lower() == 'y':
            with open('non_followers.txt', 'w', encoding='utf-8') as f:
                for username in sorted(non_followers):
                    f.write(f"{username}\n")
            print("Results saved to 'non_followers.txt'")
    
    except FileNotFoundError as e:
        print(f"\nError: Could not find file - {e}")   
        print("Please make sure the file paths are correct.")
    except Exception as e:
        print(f"\n Error: {e}")

    
