import argparse
from platforms.bili.uploader import BiliUploader
from platforms.douyin.uploader import DouyinUploader
from platforms.xhs.uploader import XhsUploader
from utils.util_sqlite import check

"""eg:
python main.py --platforms xhs --video_url "https://test" --video_path "files/test/11.mp4" --video_name "我只在乎你鄧麗君" --description "我只在乎你鄧麗君 琵琶 演奏"
python main.py --platforms douyin --video_url "https://test" --video_path "files/test/11.mp4" --video_name "我只在乎你鄧麗君" --description "我只在乎你鄧麗君 琵琶 演奏"
python main.py --platforms bili --video_url "https://test" --video_path "files/test/11.mp4" --video_name "我只在乎你鄧麗君" --description "我只在乎你鄧麗君 琵琶 演奏"

"""
# Define a dictionary that maps platform names to their respective uploader classes
UPLOADERS = {
    'bili': BiliUploader,
    'douyin': DouyinUploader,
    'xhs': XhsUploader
}


async def main(platform_name, video_url, video_path, video_name, description, headless=False):
    if check(platform_name, video_url) != 0:
        print(f"ERR!! the {platform_name}:{video_url} have already existed")
        return
    # Ensure the platform is one we know how to handle
    if platform_name not in UPLOADERS:
        print(f"Unsupported platform: {platform_name}")
        return
    # Instantiate the correct uploader class
    uploader_class = UPLOADERS[platform_name]()
    try:
        await uploader_class.upload_video(video_url, video_path, video_name, description, headless)
    except Exception as e:
        print(f"MAIN:An error occurred: {e}")


if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Upload videos to various platforms.")
    parser.add_argument('--platforms', required=True,
                        help="The platform to upload the video to (e.g., 'bili', 'douyin', 'xhs').")
    parser.add_argument('--video_url', required=True, help="Url of the video file.")
    parser.add_argument('--video_path', required=True, help="Path to the video file.")
    parser.add_argument('--video_name', required=True, help="Title of the video.")
    parser.add_argument('--description', required=False, default="", help="Description of the video.")
    parser.add_argument('--headless', action='store_true', help="Run in headless mode (default: %(default)s)",
                        default=False)

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    import asyncio

    asyncio.run(main(args.platforms, args.video_url, args.video_path, args.video_name, args.description, args.headless))
