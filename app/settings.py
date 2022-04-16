# Make the app require login authentication to access the database
private_app = True
# Create the database automatically if it does not exist when starting the server
auto_db = True
# Allow users to search for videos (shows a search bar and lets users input a "q" query param)
allow_search = True
# Allow users to manually add a record with custom data
manual_add = True
# Prevent forms across the app from asking form resending confirmations and clears the form input instead
prevent_resend = True
# Number of videos shown per page
videos_per_page = 5
# Number of videos shown per page in admin view
videos_per_admin_page = 8
# Keep the original files when archiving them (requires more disk space)
keep_original_files = False
