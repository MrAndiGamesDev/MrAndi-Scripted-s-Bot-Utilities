import discord
from discord.ext import commands
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

APIKEY = os.getenv("YOUTUBEAPIKEY")

class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Set up the YouTube API client with your API key
        self.youtube = build("youtube", "v3", developerKey=APIKEY)

    @commands.command(name="ytinfo")
    async def ytinfo(self, ctx, url: str):
        """Fetches information about a YouTube video."""
        try:
            # Extract video ID from the URL using the helper function
            video_id = self.extract_video_id(url)
            if not video_id:
                return await ctx.send("Invalid YouTube URL. Please provide a valid video URL.")

            # Fetch video details from YouTube API
            request = self.youtube.videos().list(part="snippet,statistics", id=video_id)
            response = request.execute()

            if response["items"]:
                video = response["items"][0]
                title = video["snippet"]["title"]
                description = video["snippet"]["description"][:200]  # Truncate description to 200 characters
                thumbnail_url = video["snippet"]["thumbnails"]["high"]["url"]
                views = int(video["statistics"]["viewCount"])  # Convert views to int for better formatting
                upload_date = video["snippet"]["publishedAt"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"

                # Prepare the embed with the video details
                embed = discord.Embed(title=title, url=video_url, description=description)
                embed.set_thumbnail(url=thumbnail_url)
                embed.add_field(name="Views", value=f"{views:,}", inline=True)
                embed.add_field(name="Upload Date", value=upload_date, inline=True)
                embed.set_footer(text="Video Information from YouTube API")

                await ctx.send(embed=embed)
            else:
                await ctx.send("Could not find information for the provided video URL.")

        except Exception as e:
            # Handle errors gracefully and inform the user
            await ctx.send(f"An error occurred while fetching video data: {str(e)}")

    def extract_video_id(self, url: str):
        """Extracts the video ID from a YouTube URL."""
        # Improved regular expression to handle both regular and shortened YouTube URLs
        regex = r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
        match = re.match(regex, url)
        if match:
            return match.group(1)
        return None

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(YouTube(bot))