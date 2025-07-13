"""
Recipe data processor for cleaning and structuring extracted data
"""
import re
import json
import nltk
from typing import List, Dict, Tuple
from collections import defaultdict
import logging

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

class RecipeProcessor:
    def __init__(self):
        self.food_categories = {
            "Produce": ["onion", "garlic", "tomato", "carrot", "celery", "pepper", "lettuce", "spinach", 
                       "broccoli", "mushroom", "lemon", "lime", "apple", "banana", "potato", "herbs"],
            "Meat & Seafood": ["chicken", "beef", "pork", "fish", "salmon", "shrimp", "turkey", "bacon", 
                              "ground beef", "sausage", "lamb"],
            "Dairy & Eggs": ["milk", "cheese", "butter", "yogurt", "cream", "eggs", "sour cream", 
                            "mozzarella", "parmesan", "cheddar"],
            "Pantry Staples": ["flour", "sugar", "salt", "pepper", "oil", "vinegar", "pasta", "rice", 
                              "beans", "spices", "sauce", "stock", "broth"],
            "Frozen": ["frozen vegetables", "frozen fruit", "ice cream", "frozen pizza"],
            "Bakery": ["bread", "rolls", "bagels", "croissants", "tortillas"],
            "Condiments": ["ketchup", "mustard", "mayo", "hot sauce", "soy sauce", "worcestershire"]
        }
        
        # Common cooking units and measurements
        self.units = [
            "cup", "cups", "tablespoon", "tablespoons", "tbsp", "teaspoon", "teaspoons", "tsp",
            "ounce", "ounces", "oz", "pound", "pounds", "lb", "lbs", "gram", "grams", "g",
            "kilogram", "kg", "milliliter", "ml", "liter", "liters", "pint", "quart", "gallon",
            "pinch", "dash", "handful", "clove", "cloves", "piece", "pieces", "slice", "slices"
        ]
        
        # spaCy removed; using NLTK for NLP processing
        self.nlp = None
    
    def clean_ingredient(self, ingredient: str) -> str:
        """
        Clean and normalize an ingredient string
        """
        # Remove extra whitespace
        ingredient = re.sub(r'\s+', ' ', ingredient.strip())
        
        # Remove common cooking instructions that might be mixed in
        cooking_words = ["chopped", "diced", "sliced", "minced", "grated", "fresh", "dried", 
                        "ground", "whole", "large", "small", "medium", "fine", "coarse"]
        
        # Keep the cooking instruction but clean it
        ingredient = ingredient.lower()
        
        return ingredient
    
    def extract_quantity_and_unit(self, ingredient: str) -> Tuple[str, str, str]:
        """
        Extract quantity, unit, and item from ingredient string
        """
        # Pattern to match quantity, unit, and item
        pattern = r'(\d+(?:\.\d+)?(?:\s*[-/]\s*\d+(?:\.\d+)?)?)\s*({})\s*(?:of\s+)?(.+)'.format(
            '|'.join(self.units)
        )
        
        match = re.match(pattern, ingredient.lower())
        if match:
            quantity = match.group(1)
            unit = match.group(2)
            item = match.group(3)
            return quantity, unit, item
        
        # If no unit found, try to extract just quantity and item
        quantity_pattern = r'(\d+(?:\.\d+)?(?:\s*[-/]\s*\d+(?:\.\d+)?)?)\s+(.+)'
        match = re.match(quantity_pattern, ingredient.lower())
        if match:
            quantity = match.group(1)
            item = match.group(2)
            return quantity, "", item
        
        return "", "", ingredient
    
    def categorize_ingredient(self, ingredient: str) -> str:
        """
        Categorize an ingredient into food categories
        """
        ingredient_lower = ingredient.lower()
        
        for category, keywords in self.food_categories.items():
            for keyword in keywords:
                if keyword in ingredient_lower:
                    return category
        
        return "Other"
    
    def process_ingredients_list(self, ingredients: List[str]) -> Dict[str, List[str]]:
        """
        Process a list of ingredients and categorize them
        """
        categorized = defaultdict(list)
        
        for ingredient in ingredients:
            cleaned = self.clean_ingredient(ingredient)
            if cleaned and len(cleaned) > 2:
                category = self.categorize_ingredient(cleaned)
                categorized[category].append(cleaned)
        
        # Convert to regular dict and sort
        result = {}
        for category in ["Produce", "Meat & Seafood", "Dairy & Eggs", "Pantry Staples", "Bakery", "Condiments", "Frozen", "Other"]:
            if category in categorized:
                result[category] = sorted(list(set(categorized[category])))
        
        return result
    
    def merge_shopping_lists(self, *lists: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Merge multiple shopping lists together
        """
        merged = defaultdict(list)
        
        for shopping_list in lists:
            for category, items in shopping_list.items():
                merged[category].extend(items)
        
        # Remove duplicates and sort
        result = {}
        for category, items in merged.items():
            result[category] = sorted(list(set(items)))
        
        return result
    
    def extract_cooking_instructions(self, transcript: str) -> List[str]:
        """
        Extract cooking instructions from transcript
        """
        instructions = []
        
        # Split transcript into sentences
        sentences = re.split(r'[.!?]+', transcript)
        
        # Look for instruction patterns
        instruction_patterns = [
            r'(first|then|next|after|now|finally).*',
            r'(heat|cook|add|mix|stir|pour|place|put|season|serve).*',
            r'(preheat|boil|simmer|sauté|fry|bake|roast|grill).*'
        ]
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 10:
                for pattern in instruction_patterns:
                    if re.search(pattern, sentence.lower()):
                        instructions.append(sentence)
                        break
        
        return instructions[:10]  # Return top 10 instructions
    
    def generate_recipe_summary(self, recipe_data: Dict) -> Dict:
        """
        Generate a structured summary of recipe data
        """
        summary = {
            "dish_name": recipe_data.get("dish_name", "Unknown Dish"),
            "total_videos": len(recipe_data.get("videos", [])),
            "categorized_ingredients": {},
            "cooking_instructions": [],
            "video_tutorials": []
        }
        
        # Process ingredients
        all_ingredients = recipe_data.get("ingredients", [])
        summary["categorized_ingredients"] = self.process_ingredients_list(all_ingredients)
        
        # Extract instructions from video transcripts
        for video in recipe_data.get("videos", []):
            transcript = video.get("transcript", "")
            if transcript:
                instructions = self.extract_cooking_instructions(transcript)
                summary["cooking_instructions"].extend(instructions)
                
                # Add video tutorial info
                tutorial = {
                    "title": video.get("title", ""),
                    "video_id": video.get("video_id", ""),
                    "channel": video.get("channel_title", ""),
                    "url": f"https://www.youtube.com/watch?v={video.get('video_id', '')}"
                }
                summary["video_tutorials"].append(tutorial)
        
        # Remove duplicate instructions
        summary["cooking_instructions"] = list(set(summary["cooking_instructions"]))[:15]
        
        return summary
