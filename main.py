import argparse
from platforms.bili.uploader import BiliUploader
from platforms.douyin.uploader import DouyinUploader
from platforms.toutiao.uploader import ToutiaoUploader
from platforms.xhs.uploader import XhsUploader
from utils.util_sqlite import check

# Define a dictionary that maps platform names to their respective uploader classes
UPLOADERS = {
    'bili': BiliUploader,
    'douyin': DouyinUploader,
    'toutiao': ToutiaoUploader,
    'xhs': XhsUploader
}


async def main(platform_name, video_url, video_path, video_name, cover_path, description, headless=False):
    if check(platform_name, video_url) != 0:
        print(f"Oops!! the {platform_name}:{video_url} have already existed")
        return
    # Ensure the platform is one we know how to handle
    if platform_name not in UPLOADERS:
        print(f"Unsupported platform: {platform_name}")
        return
    # Instantiate the correct uploader class
    uploader_class = UPLOADERS[platform_name]()
    try:
        await uploader_class.upload_video(video_url, video_path, video_name, cover_path, description, headless=headless)
    except Exception as e:
        print(f"MAIN:An error occurred: {e}")


if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Upload videos to various platforms.")
    parser.add_argument('--platforms', required=True,
                        help="The platform to upload the video to (e.g., 'toutiao', 'douyin', 'bili', 'xhs').")
    parser.add_argument('--video_url', required=True, help="Url of the video file.")
    parser.add_argument('--video_path', required=True, help="Path to the video file.")
    parser.add_argument('--video_name', required=True, help="Title of the video.")
    parser.add_argument('--cover_path', required=False, help="Cover of the video.")
    parser.add_argument('--description', required=False, default="", help="Description of the video.")
    parser.add_argument('--headless', required=False, action='store_true',
                        help="Run in headless mode (default: %(default)s)",
                        default=False)

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    import asyncio

    asyncio.run(
        main(args.platforms, args.video_url, args.video_path, args.video_name, args.cover_path, args.description,
             args.headless))
