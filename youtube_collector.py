"""
YouTube API handler for recipe data collection
"""
import os
import json
import logging
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re
from config import Config

class YouTubeRecipeCollector:
    def __init__(self):
        self.config = Config()
        self.youtube = None
        if self.config.YOUTUBE_API_KEY:
            self.youtube = build(
                self.config.YOUTUBE_API_SERVICE_NAME,
                self.config.YOUTUBE_API_VERSION,
                developerKey=self.config.YOUTUBE_API_KEY
            )
        
    def search_recipe_videos(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for recipe videos on YouTube
        """
        if not self.youtube:
            return []
            
        try:
            search_response = self.youtube.search().list(
                q=f"{query} recipe cooking",
                part="id,snippet",
                maxResults=max_results,
                type="video",
                videoDuration="medium",  # 4-20 minutes
                videoDefinition="high",
                order="relevance"
            ).execute()
            
            videos = []
            for item in search_response["items"]:
                video_data = {
                    "video_id": item["id"]["videoId"],
                    "title": item["snippet"]["title"],
                    "description": item["snippet"]["description"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "published_at": item["snippet"]["publishedAt"],
                    "thumbnail_url": item["snippet"]["thumbnails"]["high"]["url"]
                }
                videos.append(video_data)
                
            return videos
            
        except Exception as e:
            logging.error(f"Error searching YouTube videos: {e}")
            return []
    
    def get_video_transcript(self, video_id: str) -> Optional[str]:
        """
        Get transcript for a YouTube video
        """
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            formatter = TextFormatter()
            transcript = formatter.format_transcript(transcript_list)
            return transcript
        except Exception as e:
            logging.error(f"Error getting transcript for video {video_id}: {e}")
            return None
    
    def extract_ingredients_from_transcript(self, transcript: str) -> List[str]:
        """
        Extract ingredients from video transcript using regex patterns
        """
        ingredients = []
        
        # Common ingredient patterns
        patterns = [
            r'(\d+\s*(?:cups?|tablespoons?|teaspoons?|tbsp|tsp|oz|pounds?|lbs?|grams?|g|ml|liters?)\s+(?:of\s+)?[\w\s]+)',
            r'(\d+\s+[\w\s]+(?:cups?|tablespoons?|teaspoons?|tbsp|tsp|oz|pounds?|lbs?|grams?|g|ml|liters?))',
            r'(a\s+(?:pinch|dash|handful)\s+of\s+[\w\s]+)',
            r'(\d+\s+[\w\s]+(?:chopped|diced|sliced|minced|grated))',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            ingredients.extend(matches)
        
        # Clean up ingredients
        cleaned_ingredients = []
        for ingredient in ingredients:
            ingredient = ingredient.strip()
            if len(ingredient) > 3 and len(ingredient) < 100:
                cleaned_ingredients.append(ingredient)
        
        return list(set(cleaned_ingredients))  # Remove duplicates
    
    def get_recipe_data(self, dish_name: str) -> Dict:
        """
        Get comprehensive recipe data for a dish
        """
        videos = self.search_recipe_videos(dish_name)
        recipe_data = {
            "dish_name": dish_name,
            "videos": [],
            "ingredients": [],
            "instructions": []
        }
        
        for video in videos:
            transcript = self.get_video_transcript(video["video_id"])
            if transcript:
                ingredients = self.extract_ingredients_from_transcript(transcript)
                video["transcript"] = transcript
                video["extracted_ingredients"] = ingredients
                recipe_data["ingredients"].extend(ingredients)
                
            recipe_data["videos"].append(video)
        
        # Remove duplicate ingredients
        recipe_data["ingredients"] = list(set(recipe_data["ingredients"]))
        
        return recipe_data
    
    def save_recipe_data(self, recipe_data: Dict, filename: str):
        """
        Save recipe data to JSON file
        """
        os.makedirs(self.config.RECIPE_DATA_DIR, exist_ok=True)
        filepath = os.path.join(self.config.RECIPE_DATA_DIR, f"{filename}.json")
        
        with open(filepath, 'w') as f:
            json.dump(recipe_data, f, indent=2)
        
        return filepath
