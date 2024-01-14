import argparse
from platform.bili.uploader import BiliUploader
from platform.douyin.uploader import DouyinUploader
from platform.xhs.uploader import XhsUploader

"""
python main.py --platform xhs \
--video_url ../files/test/00.mp4 \ 
--video_path ../files/test/00.mp4 --video_name "Your Video Title" --description "Your video description."
"""
# Define a dictionary that maps platform names to their respective uploader classes
UPLOADERS = {
    'bili': BiliUploader,
    'douyin': DouyinUploader,
    'xhs': XhsUploader
}


async def main(platform_name, video_url, video_path, video_name, description):
    # Ensure the platform is one we know how to handle
    if platform_name not in UPLOADERS:
        print(f"Unsupported platform: {platform_name}")
        return

    # Instantiate the correct uploader class
    uploader_class = UPLOADERS[platform_name]()
    try:
        # 假设 video_url 和 video_path 是相同的
        await uploader_class.upload_video(video_url, video_path, video_path, video_name, description)
        print(f"Video uploaded successfully to {platform_name}.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Upload videos to various platforms.")
    parser.add_argument('--platform', required=True,
                        help="The platform to upload the video to (e.g., 'bili', 'douyin', 'xhs').")
    parser.add_argument('--video_url', required=True, help="Url of the video file.")
    parser.add_argument('--video_path', required=True, help="Path to the video file.")
    parser.add_argument('--video_name', required=True, help="Title of the video.")
    parser.add_argument('--description', required=False, default="", help="Description of the video.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the main function with the parsed arguments
    import asyncio

    asyncio.run(main(args.platform, args.video_url, args.video_path, args.video_name, args.description))
