# import os
# import yt_dlp
# import streamlit as st

# # Function to download the video or audio
# def download_content(url, format_choice):
#     """
#     Downloads video or audio from a given URL using yt-dlp.
#     Returns the path to the downloaded file on success, or an error message.
#     """
#     # Create a temporary directory for downloads
#     # Streamlit Cloud's ephemeral filesystem is suitable for this.
#     download_folder = 'downloads'
#     if not os.path.exists(download_folder):
#         os.makedirs(download_folder)

#     # Base options for yt-dlp
#     ydl_opts = {
#         'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
#         # Bypass potential geo-restrictions
#         'geo_bypass_country': 'US',
#     }

#     if format_choice == 'mp4':
#         ydl_opts.update({
#             'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
#             # This postprocessor will merge video and audio streams
#             'postprocessors': [{
#                 'key': 'FFmpegVideoConvertor',
#                 'preferedformat': 'mp4'
#             }]
#         })
#     elif format_choice == 'mp3':
#         ydl_opts.update({
#             'format': 'bestaudio/best',
#             'postprocessors': [{
#                 'key': 'FFmpegExtractAudio',
#                 'preferredcodec': 'mp3',
#                 'preferredquality': '192',
#             }]
#         })

#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             # Extract info and download the file
#             info_dict = ydl.extract_info(url, download=True)
#             # Find the actual file path of the downloaded content
#             filename = ydl.prepare_filename(info_dict)

#             # yt-dlp might download different extensions, so we handle them
#             # Example: mp4 format might result in an mkv file.
#             if format_choice == 'mp4':
#                 for f in info_dict.get('requested_downloads', []):
#                     if f['ext'] == 'mp4':
#                         filename = f['filepath']
#                         break
#             elif format_choice == 'mp3':
#                 for f in info_dict.get('requested_downloads', []):
#                     if f['ext'] == 'mp3':
#                         filename = f['filepath']
#                         break

#             return filename
#     except Exception as e:
#         return f"An error occurred: {e}"

# # Streamlit UI
# st.set_page_config(page_title="YouTube Video & Audio Downloader", layout="centered")
# st.image("https://upload.wikimedia.org/wikipedia/commons/4/42/YouTube_icon_%282013-2017%29.png", width=100)
# st.title("YouTube Video & Audio Downloader")

# st.markdown("This application allows you to download videos or audio from YouTube. "
#             "Simply enter the URL, select the desired format, and click 'Download'.")

# video_url = st.text_input("Enter the YouTube video URL:")
# format_choice = st.selectbox("Select the format:", ["mp4", "mp3"])

# if st.button("Download"):
#     if video_url:
#         with st.spinner("Preparing your file..."):
#             file_path = download_content(video_url, format_choice)

#             if file_path.startswith("An error occurred"):
#                 st.error(file_path)
#             else:
#                 st.success("Download completed successfully!")
#                 try:
#                     # Provide the download button
#                     with open(file_path, "rb") as file:
#                         mime_type = "audio/mpeg" if format_choice == 'mp3' else "video/mp4"
#                         st.download_button(
#                             label="Click to Download",
#                             data=file,
#                             file_name=os.path.basename(file_path),
#                             mime=mime_type
#                         )
#                 except FileNotFoundError:
#                     st.error("The downloaded file was not found. Please try again.")
#     else:
#         st.error("Please enter a valid YouTube URL.")


import os
import yt_dlp
import streamlit as st
import time

# Function to download the video or audio
def download_content(url, format_choice):
    """
    Downloads video or audio from a given URL using yt-dlp.
    Returns the path to the downloaded file on success, or an error message.
    """
    download_folder = 'downloads'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Base options for yt-dlp
    ydl_opts = {
        'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
        # Bypass potential geo-restrictions by setting a country
        'geo_bypass_country': 'US',
        # User-agent to mimic a browser
        'postprocessors': [],
    }

    if format_choice == 'mp4':
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        })
    elif format_choice == 'mp3':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'].append({
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return filename
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.set_page_config(page_title="YouTube Video & Audio Downloader", layout="centered")
st.title("YouTube Video & Audio Downloader")
st.markdown("This application downloads videos or audio from YouTube. Enter a URL and select a format.")

video_url = st.text_input("Enter the YouTube video URL:")
format_choice = st.selectbox("Select the format:", ["mp4", "mp3"])

if st.button("Download"):
    if video_url:
        with st.spinner("Preparing your file..."):
            start_time = time.time()
            file_path = download_content(video_url, format_choice)
            end_time = time.time()
            st.info(f"Download took {end_time - start_time:.2f} seconds.")

            if file_path.startswith("An error occurred"):
                st.error(file_path)
                st.markdown("If you see an **HTTP 403 Forbidden** error, it's likely due to YouTube blocking the server's IP. Please try again later or use a different video.")
            else:
                st.success("Download completed successfully!")
                try:
                    with open(file_path, "rb") as file:
                        mime_type = "audio/mpeg" if format_choice == 'mp3' else "video/mp4"
                        st.download_button(
                            label="Click to Download",
                            data=file,
                            file_name=os.path.basename(file_path),
                            mime=mime_type
                        )
                except FileNotFoundError:
                    st.error("The downloaded file was not found. Please try again.")
    else:
        st.error("Please enter a valid YouTube URL.")
