import re
import random

class User:
    def __init__(self, email, phone, password):
        self.email = email
        self.phone = phone
        self.password = password
        self.name = ""
        self.profile_picture = None
        self.preferences = {}
        self.library = []
        self.history = []
        self.playlists = {}
        self.points = 0
        self.notifications_enabled = True


class Admin:
    def __init__(self):
        self.contents = []

    def upload_content(self, content):
        self.contents.append(content)
        print(f"Uploaded: {content['type']} - {content['title']}")

    def update_content(self, title, new_data):
        for content in self.contents:
            if content['title'] == title:
                content.update(new_data)
                print(f"Updated: {title}")
                return
        print("Content not found.")

    def remove_content(self, title):
        title_lower = title.lower()
        for content in self.contents:
            if content['title'].lower() == title_lower:
                self.contents = [c for c in self.contents if c['title'].lower() != title_lower]
                print(f"Removed: {content['title']}")
                return
        print("Cannot remove. Title not found in uploaded content.")



class MusicApp:
    def __init__(self):
        self.users = {}
        self.admin = Admin()
        self.content = {
            "songs": [
                {"title": "Blinding Lights", "artist": "The Weeknd", "album": "After Hours", "duration": "3:20", "artwork": "🎵"},
                {"title": "Shape of You", "artist": "Ed Sheeran", "album": "Divide", "duration": "4:00", "artwork": "🎶"},
                {"title": "Bohemian Rhapsody", "artist": "Queen", "album": "A Night at the Opera", "duration": "5:55", "artwork": "🎼"}
            ],
            "albums": ["Divide", "After Hours"],
            "artists": ["Ed Sheeran", "The Weeknd", "Queen"],
            "genres": ["Pop", "Rock", "Electronic"],
            "playlists": ["Top Hits"],
            "podcasts": ["TechTalk"]
        }
        self.volume = 5  # scale of 0–10
        self.repeat = False
        self.playback_speed = 1.0  # 1.0x normal speed


    def validate_email(self, email):
    # Only allow emails ending with these domains
        allowed_domains = ["@gmail.com", "@yahoo.com", "@outlook.com"]
        pattern = r"^[^@]+@[^@]+\.[^@]+$"

        return re.match(pattern, email) and any(email.endswith(domain) for domain in allowed_domains)

    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10

    def register(self):
        email = input("Enter Email: ")
        while not self.validate_email(email):
            print("Invalid email format.")
            email = input("Enter Email: ")

        phone = input("Enter Phone (10 digits): ")
        while not self.validate_phone(phone):
            print("Invalid phone number. It should be 10 digits.")
            phone = input("Enter Phone (10 digits): ")

        password = input("Create Password: ")
        if email in self.users:
            print("User already exists.")
        else:
            self.users[email] = User(email, phone, password)
            print("Registration successful.")

    def login(self):
        email = input("Email: ")
        password = input("Password: ")
        user = self.users.get(email)
        if user and user.password == password:
            print(f"Welcome back, {user.name or 'User'}!")
            self.user_menu(user)
        else:
            print("Invalid login.")

    def reset_password(self):
        email = input("Enter your email: ")
        if email in self.users:
            password = input("Enter old password:")
            new_pw = input("Enter new password: ")
            while new_pw == password:
                print("Old password cannot be your new password")
                new_pw = input("Enter new password:")
            self.users[email].password = new_pw
            print("Password reset.")
        else:
            print("Email not found.")

    def update_profile(self, user):
        name = input("Enter your name: ")

    # Validate profile picture format
        allowed_extensions = ('.jpg', '.jpeg', '.png')
        while True:
            pic = input("Upload profile picture (filename with extension): ")
            if pic.lower().endswith(allowed_extensions):
                print("Uploaded!")
                break
            print("Invalid file format. Please upload an image (.jpg, .jpeg, .png")

    # Define allowed genres and languages
        allowed_genres = ["Pop", "Rock", "Hip Hop", "Jazz", "Classical", "Electronic"]
        allowed_languages = ["English", "Kannada", "Hindi", "Telugu", "Korean"]

    # Genre selection with loop and case-insensitive check
        while True:
            print("\nAvailable Genres:", ", ".join(allowed_genres))
            selected_genres = input("Enter preferred genres (comma separated): ").split(",")
            selected_genres_clean = [g.strip().title() for g in selected_genres]

            if all(g in allowed_genres for g in selected_genres_clean):
                print("Updated!")
                break
            print("Error: One or more genres are invalid. Please choose only from the available options.")

    # Language selection with loop and case-insensitive check
        while True:
            print("Available Languages:", ", ".join(allowed_languages))
            selected_languages = input("Enter preferred languages (comma separated): ").split(",")
            selected_languages_clean = [l.strip().title() for l in selected_languages]

            if all(l in allowed_languages for l in selected_languages_clean):
                print("Updated!")
                break
            print("Error: One or more languages are invalid. Please choose only from the available options.")

    # Save to user profile
        user.name = name
        user.profile_picture = pic
        user.preferences = {
            "genres": selected_genres_clean,
            "languages": selected_languages_clean,
            "followed_artists": ["Ed Sheeran", "The Weeknd"],
            "followed_playlists": ["Top Hits"]
        }

        print("Profile updated.")


    def search(self):
        term = input("Search: ").lower()
        found = False
    
        # Define searchable categories
        searchable_categories = {
            "Songs": self.content.get("songs", []),
            "Albums": self.content.get("albums", []),
            "Artists": self.content.get("artists", []),
            "Genres": self.content.get("genres", []),
            "Playlists": self.content.get("playlists", []),
            "Podcasts": self.content.get("podcasts", [])
        }
    
        # Perform search in each category
        for category, items in searchable_categories.items():
            if category == "Songs":
                matches = [song for song in items if term in song["title"].lower()]
                if matches:
                    found = True
                    print(f"\n{category} matches:")
                    for song in matches:
                        print(f"- {song['title']} by {song['artist']} ({song['duration']})")
            else:
                matches = [item for item in items if term in item.lower()]
                if matches:
                    found = True
                    print(f"\n{category} matches:")
                    for match in matches:
                        print(f"- {match}")
    
        # Print this only once after all categories are checked
        if not found:
            print("No matches found.")

    def play_music(self, user):
        playlist = self.content["songs"]
        if not playlist:
            print("No songs available.")
            return

        current_index = 0
        is_playing = True

        def display_song(song):
            print(f"\nNow Playing: {song['title']} by {song['artist']}")
            print(f"Album: {song['album']} | Duration: {song['duration']} | Artwork: {song['artwork']}")
            print(f"Volume: {self.volume}/10 | Speed: {self.playback_speed}x | Repeat: {'On' if self.repeat else 'Off'}")

        while True:
            song = playlist[current_index]
            if is_playing:
                display_song(song)
                user.history.append(song["title"])
                user.points += 1
                print("🎧 +1 point for listening!")


            print("\nControls: [P]ause, [R]esume, [S]kip, [B]ack, [Sh]uffle, [V]olume, [T]oggle Repeat, [Sp]eed, [Q]uit")
            choice = input("Choose an action: ").strip().lower()

            if choice == 'p':
                is_playing = False
                print("Music paused.")
            elif choice == 'r':
                if not is_playing:
                    is_playing = True
                    print("Music resumed.")
                else:
                    print("Already playing.")
            elif choice == 's':
                if current_index < len(playlist) - 1:
                    current_index += 1
                elif self.repeat:
                    current_index = 0
                else:
                    print("Reached end of playlist.")
            elif choice == 'b':
                if current_index > 0:
                    current_index -= 1
                else:
                    print("Already at beginning.")
            elif choice == 'sh':
                current_index = random.randint(0, len(playlist) - 1)
            elif choice == 'v':
                try:
                    vol = int(input("Set volume (0–10): "))
                    if 0 <= vol <= 10:
                        self.volume = vol
                    else:
                        print("Invalid volume.")
                except:
                    print("Please enter an integer.")
            elif choice == 't':
                self.repeat = not self.repeat
                print(f"Repeat {'enabled' if self.repeat else 'disabled'}.")
            elif choice == 'sp':
                try:
                    speed = float(input("Set speed (e.g., 0.5 for slow, 1.0 normal, 1.5/2.0 fast): "))
                    if 0.5 <= speed <= 2.0:
                        self.playback_speed = speed
                    else:
                        print("Speed must be between 0.5x and 2.0x.")
                except:
                    print("Please enter a valid number.")
            elif choice == 'q':
                print("Exiting playback.")
                break
            else:
                print("Invalid choice.")

    def manage_playlist(self, user):
        while True:
            print("\n1. Create\n2. Add Song\n3. View\n4. Remove Song\n5. Delete Playlist\n6. Back")
            choice = input("Choose: ")
        
            if choice == '1':
                name = input("Playlist name: ")
                if name in user.playlists:
                    print("Playlist already exists.")
                else:
                    user.playlists[name] = []
                    print("Playlist created.")

            elif choice == '2':
                name = input("Playlist name: ")
                if name in user.playlists:
                    song = input("Song to add: ")
                    user.playlists[name].append(song)
                    print("Song added.")
                else:
                    print("Playlist not found.")

            elif choice == '3':
                if user.playlists:
                    for name, songs in user.playlists.items():
                        print(f"{name}: {songs if songs else 'No songs'}")
                else:
                    print("No playlists available.")
                
            elif choice == '4':
                name = input("Playlist name: ")
                if name in user.playlists:
                    songs = user.playlists[name]
                    if not songs:
                        print("Playlist is empty.")
                        continue
                    print(f"Songs in {name}: {songs}")
                    song_to_remove = input("Enter song to remove: ")
                    if song_to_remove in songs:
                        songs.remove(song_to_remove)
                        print("Song removed.")
                    else:
                        print("Song not found in playlist.")
                else:
                    print("Playlist not found.")

            elif choice == '5':
                name = input("Playlist name to delete: ")
                if name in user.playlists:
                    del user.playlists[name]
                    print("Playlist deleted.")
                else:
                    print("Playlist not found.")

            elif choice == '6':
                break
            else:
                print("Invalid choice.")


    def library(self, user):
        while True:
            print("\nLibrary Menu:")
            print("1. Add to Library")
            print("2. View Library")
            print("3. View History")
            print("4. Back")
            choice = input("Choose: ").strip()

            if choice == '1':
                category = input("Enter category (song/album/artist/playlist): ").strip().lower()
                item = input(f"Enter {category} to add: ").strip()
            
            # Avoid duplicates
                if (category, item) not in user.library:
                    user.library.append((category, item))
                    print(f"{category.title()} '{item}' added to your library.")
                else:
                    print(f"{category.title()} '{item}' is already in your library.")

            elif choice == '2':
                print("Your Library:")
                if user.library:
                    categorized = {}
                    for category, item in user.library:
                        categorized.setdefault(category, []).append(item)

                    for cat, items in categorized.items():
                        print(f"\n{cat.title()}:")
                        for i in items:
                            print(f"- {i}")
                else:
                    print("Your library is empty.")

            elif choice == '3':
                print("Playback History:")
                if user.history:
                    for index, song in enumerate(user.history, start=1):
                        print(f"{index}. {song}")
                else:
                    print("No history available.")


            elif choice == '4':
                break

            else:
                print("Invalid choice. Please try again.")


    def check_rewards(self, user):
        print(f"\n🎉 You have {user.points} points.")
        if user.points >= 30:
            print("🎁 Surprise content unlocked!")
        elif user.points >= 20:
            print("🏅 You've earned a Premium Listener badge!")
        elif user.points >= 10:
            print("✅ You unlocked a free download!")
        else:
            print("Keep exploring to earn rewards!")


    def audio_settings(self):
        bitrate = input("Set bitrate (e.g., 128kbps, 320kbps): ")
        bass = int(input("Bass level (0-10): "))
        while not bass<=10:
            print("Choose value only from 0-10")
            bass = int(input("Bass level (0-10): "))
        treble = int(input("Treble level (0-10): "))
        while not treble<=10:
            print("Choose value only from 0-10")
            treble = int(input("Treble level (0-10): "))
        print(f"Audio set to {bitrate}kbps, Bass: {bass}, Treble: {treble}")

    def notifications(self, user):
        while True:
            print("\n1. Toggle Notifications ON/OFF")
            print("2. View Updates")
            print("3. Back")
            choice = input("Choose: ")

            if choice == '1':
                toggle = input("Turn notifications ON/OFF: ").lower()
                if toggle in ["on", "off"]:
                    user.notifications_enabled = (toggle == "on")
                    print(f"Notifications {'enabled' if user.notifications_enabled else 'disabled'}.")
                else:
                    print("Invalid input. Use 'ON' or 'OFF'.")
            elif choice == '2':
                if not user.notifications_enabled:
                    print("Notifications are turned OFF.")
                else:
            # Dummy updates (in real app, this would be dynamic)
                    followed_artists = user.preferences.get("followed_artists", [])
                    followed_playlists = user.preferences.get("followed_playlists", [])
            
                    print("🎵 Notifications Feed:")
                    if "Ed Sheeran" in followed_artists:
                        print("- New release by Ed Sheeran: 'Sunrise Symphony'")
                    if "Top Hits" in followed_playlists:
                        print("- Playlist 'Top Hits' has been updated!")
                    print("- Upcoming concert: The Weeknd – July 15, 2025, NYC Arena")
    
            elif choice == '3':
                return
            else:
                print("Invalid choice.")
            

    def admin_panel(self):
        while True:
            print("\n1. Upload\n2. Update\n3. Delete\n4. Back")
            choice = input("Admin Choice: ")
            if choice == '1':
                t = input("Content type (song/album): ")
                title = input("Title: ")
                self.admin.upload_content({"type": t, "title": title})
            elif choice == '2':
                title = input("Title to update: ")
                new = input("New title: ")
                self.admin.update_content(title, {"title": new})
            elif choice == '3':
                title = input("Title to remove: ")
                self.admin.remove_content(title)
            elif choice == '4':
                print("Back to main menu")
                break
            else:
                print("Invalid choice.")




    def user_menu(self, user):
        while True:
            print("\n1.Update Profile 2.Search 3.Play Music 4.Playlists 5.Library 6.Rewards 7.Audio Settings 8.Notifications 9.Logout")
            choice = input("Choose: ")
            if choice == '1':
                self.update_profile(user)
            elif choice == '2':
                self.search()
            elif choice == '3':
                self.play_music(user)
            elif choice == '4':
                self.manage_playlist(user)
            elif choice == '5':
                self.library(user)
            elif choice == '6':
                self.check_rewards(user)
            elif choice == '7':
                self.audio_settings()
            elif choice == '8':
                self.notifications(user)
            elif choice == '9':
                print("Logging out...")
                print("Logout successful")
                break
            else:
                print("Invalid choice.")

    def run(self):
        while True:
            print("\n1.Register 2.Login 3.Reset Password 4.Admin Panel 5.Exit")
            choice = input("Choose: ")
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                self.reset_password()
            elif choice == '4':
                self.admin_panel()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        #if __name__ == "__main__":
                #import re
                #import random
    
class User:
    def __init__(self, email, phone, password):
        self.email = email
        self.phone = phone
        self.password = password
        self.name = ""
        self.profile_picture = None
        self.preferences = {}
        self.library = []
        self.history = []
        self.playlists = {}
        self.points = 0
        self.notifications_enabled = True
    
    
class Admin:
    def __init__(self):
        self.contents = []
    
    def upload_content(self, content):
        self.contents.append(content)
        print(f"Uploaded: {content['type']} - {content['title']}")
    
    def update_content(self, title, new_data):
        for content in self.contents:
            if content['title'] == title:
                content.update(new_data)
                print(f"Updated: {title}")
                return
        print("Content not found.")
    
    def remove_content(self, title):
        title_lower = title.lower()
        for content in self.contents:
            if content['title'].lower() == title_lower:
                self.contents = [c for c in self.contents if c['title'].lower() != title_lower]
                print(f"Removed: {content['title']}")
                return
        print("Cannot remove. Title not found in uploaded content.")
    
    
    
class MusicApp:
    def __init__(self):
        self.users = {}
        self.admin = Admin()
        self.content = {
            "songs": [
                {"title": "Blinding Lights", "artist": "The Weeknd", "album": "After Hours", "duration": "3:20", "artwork": "🎵"},
                {"title": "Shape of You", "artist": "Ed Sheeran", "album": "Divide", "duration": "4:00", "artwork": "🎶"},
                {"title": "Bohemian Rhapsody", "artist": "Queen", "album": "A Night at the Opera", "duration": "5:55", "artwork": "🎼"}
            ],
            "albums": ["Divide", "After Hours"],
            "artists": ["Ed Sheeran", "The Weeknd", "Queen"],
            "genres": ["Pop", "Rock", "Electronic"],
            "playlists": ["Top Hits"],
            "podcasts": ["TechTalk"]
        }
        self.volume = 5  # scale of 0–10
        self.repeat = False
        self.playback_speed = 1.0  # 1.0x normal speed
    
    
    def validate_email(self, email):
    # Only allow emails ending with these domains
        allowed_domains = ["@gmail.com", "@yahoo.com", "@outlook.com"]
        pattern = r"^[^@]+@[^@]+\.[^@]+$"
    
        return re.match(pattern, email) and any(email.endswith(domain) for domain in allowed_domains)
    
    def validate_phone(self, phone):
        return phone.isdigit() and len(phone) == 10
    
    def register(self):
        email = input("Enter Email: ")
        while not self.validate_email(email):
            print("Invalid email format.")
            email = input("Enter Email: ")
    
        phone = input("Enter Phone (10 digits): ")
        while not self.validate_phone(phone):
            print("Invalid phone number. It should be 10 digits.")
            phone = input("Enter Phone (10 digits): ")
    
        password = input("Create Password: ")
        if email in self.users:
            print("User already exists.")
        else:
            self.users[email] = User(email, phone, password)
            print("Registration successful.")
    
    def login(self):
        email = input("Email: ")
        password = input("Password: ")
        user = self.users.get(email)
        if user and user.password == password:
            print(f"Welcome back, {user.name or 'User'}!")
            self.user_menu(user)
        else:
            print("Invalid login.")
    
    def reset_password(self):
        email = input("Enter your email: ")
        if email in self.users:
            password = input("Enter old password:")
            new_pw = input("Enter new password: ")
            while new_pw == password:
                print("Old password cannot be your new password")
                new_pw = input("Enter new password:")
            self.users[email].password = new_pw
            print("Password reset.")
        else:
            print("Email not found.")
    
    def update_profile(self, user):
        name = input("Enter your name: ")
    
    # Validate profile picture format
        allowed_extensions = ('.jpg', '.jpeg', '.png')
        while True:
            pic = input("Upload profile picture (filename with extension): ")
            if pic.lower().endswith(allowed_extensions):
                print("Uploaded!")
                break
            print("Invalid file format. Please upload an image (.jpg, .jpeg, .png")
    
    # Define allowed genres and languages
        allowed_genres = ["Pop", "Rock", "Hip Hop", "Jazz", "Classical", "Electronic"]
        allowed_languages = ["English", "Kannada", "Hindi", "Telugu", "Korean"]
    
    # Genre selection with loop and case-insensitive check
        while True:
            print("\nAvailable Genres:", ", ".join(allowed_genres))
            selected_genres = input("Enter preferred genres (comma separated): ").split(",")
            selected_genres_clean = [g.strip().title() for g in selected_genres]
    
            if all(g in allowed_genres for g in selected_genres_clean):
                print("Updated!")
                break
            print("Error: One or more genres are invalid. Please choose only from the available options.")
    
    # Language selection with loop and case-insensitive check
        while True:
            print("Available Languages:", ", ".join(allowed_languages))
            selected_languages = input("Enter preferred languages (comma separated): ").split(",")
            selected_languages_clean = [l.strip().title() for l in selected_languages]
    
            if all(l in allowed_languages for l in selected_languages_clean):
                print("Updated!")
                break
            print("Error: One or more languages are invalid. Please choose only from the available options.")
    
    # Save to user profile
        user.name = name
        user.profile_picture = pic
        user.preferences = {
            "genres": selected_genres_clean,
            "languages": selected_languages_clean,
            "followed_artists": ["Ed Sheeran", "The Weeknd"],
            "followed_playlists": ["Top Hits"]
        }
    
        print("Profile updated.")
    
    
    def search(self):
        term = input("Search: ").lower()
        found = False
    
    # Define searchable categories
        searchable_categories = {
            "Songs": self.content.get("songs", []),
            "Albums": self.content.get("albums", []),
            "Artists": self.content.get("artists", []),
            "Genres": self.content.get("genres", []),
            "Playlists": self.content.get("playlists", []),
            "Podcasts": self.content.get("podcasts", [])
        }
    
    # Perform search in each category
        for category, items in searchable_categories.items():
            if category == "Songs":
                matches = [song for song in items if term in song["title"].lower()]
                if matches:
                    found = True
                    print(f"\n{category} matches:")
                    for song in matches:
                        print(f"- {song['title']} by {song['artist']} ({song['duration']})")
            else:
                matches = [item for item in items if term in item.lower()]
                if matches:
                    found = True
                    print(f"\n{category} matches:")
                    for match in matches:
                        print(f"- {match}")
    # If no matches found
        if not found:
            print("No matches found.")
            
    def play_music(self, user):
        playlist = self.content["songs"]
        if not playlist:
            print("No songs available.")
            return
    
        current_index = 0
        is_playing = True
    
        def display_song(song):
            print(f"\nNow Playing: {song['title']} by {song['artist']}")
            print(f"Album: {song['album']} | Duration: {song['duration']} | Artwork: {song['artwork']}")
            print(f"Volume: {self.volume}/10 | Speed: {self.playback_speed}x | Repeat: {'On' if self.repeat else 'Off'}")
    
        while True:
            song = playlist[current_index]
            if is_playing:
                display_song(song)
                user.history.append(song["title"])
                user.points += 1
                print("🎧 +1 point for listening!")
    
    
            print("\nControls: [P]ause, [R]esume, [S]kip, [B]ack, [Sh]uffle, [V]olume, [T]oggle Repeat, [Sp]eed, [Q]uit")
            choice = input("Choose an action: ").strip().lower()
    
            if choice == 'p':
                is_playing = False
                print("Music paused.")
            elif choice == 'r':
                if not is_playing:
                    is_playing = True
                    print("Music resumed.")
                else:
                    print("Already playing.")
            elif choice == 's':
                if current_index < len(playlist) - 1:
                    current_index += 1
                elif self.repeat:
                    current_index = 0
                else:
                    print("Reached end of playlist.")
            elif choice == 'b':
                if current_index > 0:
                    current_index -= 1
                else:
                    print("Already at beginning.")
            elif choice == 'sh':
                current_index = random.randint(0, len(playlist) - 1)
            elif choice == 'v':
                try:
                    vol = int(input("Set volume (0–10): "))
                    if 0 <= vol <= 10:
                        self.volume = vol
                    else:
                        print("Invalid volume.")
                except:
                    print("Please enter an integer.")
            elif choice == 't':
                self.repeat = not self.repeat
                print(f"Repeat {'enabled' if self.repeat else 'disabled'}.")
            elif choice == 'sp':
                try:
                    speed = float(input("Set speed (e.g., 0.5 for slow, 1.0 normal, 1.5/2.0 fast): "))
                    if 0.5 <= speed <= 2.0:
                        self.playback_speed = speed
                    else:
                        print("Speed must be between 0.5x and 2.0x.")
                except:
                    print("Please enter a valid number.")
            elif choice == 'q':
                print("Exiting playback.")
                break
            else:
                print("Invalid choice.")
    
    def manage_playlist(self, user):
        while True:
            print("\n1. Create\n2. Add Song\n3. View\n4. Remove Song\n5. Delete Playlist\n6. Back")
            choice = input("Choose: ")
        
            if choice == '1':
                name = input("Playlist name: ")
                if name in user.playlists:
                    print("Playlist already exists.")
                else:
                    user.playlists[name] = []
                    print("Playlist created.")
    
            elif choice == '2':
                name = input("Playlist name: ")
                if name in user.playlists:
                    song = input("Song to add: ")
                    user.playlists[name].append(song)
                    print("Song added.")
                else:
                    print("Playlist not found.")
    
            elif choice == '3':
                if user.playlists:
                    for name, songs in user.playlists.items():
                        print(f"{name}: {songs if songs else 'No songs'}")
                else:
                    print("No playlists available.")
                
            elif choice == '4':
                name = input("Playlist name: ")
                if name in user.playlists:
                    songs = user.playlists[name]
                    if not songs:
                        print("Playlist is empty.")
                        continue
                    print(f"Songs in {name}: {songs}")
                    song_to_remove = input("Enter song to remove: ")
                    if song_to_remove in songs:
                        songs.remove(song_to_remove)
                        print("Song removed.")
                    else:
                        print("Song not found in playlist.")
                else:
                    print("Playlist not found.")
    
            elif choice == '5':
                name = input("Playlist name to delete: ")
                if name in user.playlists:
                    del user.playlists[name]
                    print("Playlist deleted.")
                else:
                    print("Playlist not found.")
    
            elif choice == '6':
                break
            else:
                print("Invalid choice.")
    
    
    def library(self, user):
        while True:
            print("\nLibrary Menu:")
            print("1. Add to Library")
            print("2. View Library")
            print("3. View History")
            print("4. Back")
            choice = input("Choose: ").strip()
    
            if choice == '1':
                category = input("Enter category (song/album/artist/playlist): ").strip().lower()
                item = input(f"Enter {category} to add: ").strip()
            
            # Avoid duplicates
                if (category, item) not in user.library:
                    user.library.append((category, item))
                    print(f"{category.title()} '{item}' added to your library.")
                else:
                    print(f"{category.title()} '{item}' is already in your library.")
    
            elif choice == '2':
                print("Your Library:")
                if user.library:
                    categorized = {}
                    for category, item in user.library:
                        categorized.setdefault(category, []).append(item)
    
                    for cat, items in categorized.items():
                        print(f"\n{cat.title()}:")
                        for i in items:
                            print(f"- {i}")
                else:
                    print("Your library is empty.")
    
            elif choice == '3':
                print("Playback History:")
                if user.history:
                    for index, song in enumerate(user.history, start=1):
                        print(f"{index}. {song}")
                else:
                    print("No history available.")
    
    
            elif choice == '4':
                break
    
            else:
                print("Invalid choice. Please try again.")
    
    
    def check_rewards(self, user):
        print(f"\n🎉 You have {user.points} points.")
        if user.points >= 30:
            print("🎁 Surprise content unlocked!")
        elif user.points >= 20:
            print("🏅 You've earned a Premium Listener badge!")
        elif user.points >= 10:
            print("✅ You unlocked a free download!")
        else:
            print("Keep exploring to earn rewards!")
    
    
    def audio_settings(self):
        bitrate = input("Set bitrate (e.g., 128kbps, 320kbps): ")
        bass = int(input("Bass level (0-10): "))
        while not bass<=10:
            print("Choose value only from 0-10")
            bass = int(input("Bass level (0-10): "))
        treble = int(input("Treble level (0-10): "))
        while not treble<=10:
            print("Choose value only from 0-10")
            treble = int(input("Treble level (0-10): "))
        print(f"Audio set to {bitrate}kbps, Bass: {bass}, Treble: {treble}")
    
    def notifications(self, user):
        while True:
            print("\n1. Toggle Notifications ON/OFF")
            print("2. View Updates")
            print("3. Back")
            choice = input("Choose: ")
    
            if choice == '1':
                toggle = input("Turn notifications ON/OFF: ").lower()
                if toggle in ["on", "off"]:
                    user.notifications_enabled = (toggle == "on")
                    print(f"Notifications {'enabled' if user.notifications_enabled else 'disabled'}.")
                else:
                    print("Invalid input. Use 'ON' or 'OFF'.")
            elif choice == '2':
                if not user.notifications_enabled:
                    print("Notifications are turned OFF.")
                else:
            # Dummy updates (in real app, this would be dynamic)
                    followed_artists = user.preferences.get("followed_artists", [])
                    followed_playlists = user.preferences.get("followed_playlists", [])
            
                    print("🎵 Notifications Feed:")
                    if "Ed Sheeran" in followed_artists:
                        print("- New release by Ed Sheeran: 'Sunrise Symphony'")
                    if "Top Hits" in followed_playlists:
                        print("- Playlist 'Top Hits' has been updated!")
                    print("- Upcoming concert: The Weeknd – July 15, 2025, NYC Arena")
    
            elif choice == '3':
                return
            else:
                print("Invalid choice.")
            
    
    def admin_panel(self):
        while True:
            print("\n1. Upload\n2. Update\n3. Delete\n4. Back")
            choice = input("Admin Choice: ")
            if choice == '1':
                t = input("Content type (song/album): ")
                title = input("Title: ")
                self.admin.upload_content({"type": t, "title": title})
            elif choice == '2':
                title = input("Title to update: ")
                new = input("New title: ")
                self.admin.update_content(title, {"title": new})
            elif choice == '3':
                title = input("Title to remove: ")
                self.admin.remove_content(title)
            elif choice == '4':
                print("Back to main menu")
                break
            else:
                print("Invalid choice.")
    
    
    
    
    def user_menu(self, user):
        while True:
            print("\n1.Update Profile 2.Search 3.Play Music 4.Playlists 5.Library 6.Rewards 7.Audio Settings 8.Notifications 9.Logout")
            choice = input("Choose: ")
            if choice == '1':
                self.update_profile(user)
            elif choice == '2':
                self.search()
            elif choice == '3':
                self.play_music(user)
            elif choice == '4':
                self.manage_playlist(user)
            elif choice == '5':
                self.library(user)
            elif choice == '6':
                self.check_rewards(user)
            elif choice == '7':
                self.audio_settings()
            elif choice == '8':
                self.notifications(user)
            elif choice == '9':
                print("Logging out...")
                print("Logout successful")
                break
            else:
                print("Invalid choice.")
    
    def run(self):
        while True:
            print("\n1.Register 2.Login 3.Reset Password 4.Admin Panel 5.Exit")
            choice = input("Choose: ")
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                self.reset_password()
            elif choice == '4':
                self.admin_panel()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
                
                
                
if __name__ == "__main__":
    app = MusicApp()
    app.run()
