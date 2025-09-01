# Travel Itinerary Planner using LangChain
# A multi-LLM system for comprehensive travel planning

import os
import json
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAI

# Load environment variables
load_dotenv()


class OutlineGenerator:
    """LLM 1: ChatGroq for generating day-by-day travel plan outline"""
    
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",
            temperature=0.7
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["destination", "duration", "preferences", "chat_history"],
            template="""
            You are a travel planning expert. Based on the user's destination, trip duration, and preferences, 
            create a day-by-day travel plan outline.

            Destination: {destination}
            Trip Duration: {duration} days
            User Preferences from Previous Conversations: {preferences}
            Chat History: {chat_history}

            Please create a concise day-by-day outline that considers:
            - The user's stated preferences
            - Popular attractions and activities in {destination}
            - Logical geographical flow
            - Balance between different types of activities

            Format your response as:
            Day 1: [Brief description of main activities/theme]
            Day 2: [Brief description of main activities/theme]
            ... and so on

            Day-by-day Outline:
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def generate_outline(self, destination, duration, preferences, chat_history):
        return self.chain.run(
            destination=destination,
            duration=duration,
            preferences=preferences,
            chat_history=chat_history
        )


class DetailedItineraryGenerator:
    """LLM 2: Gemini for generating detailed itinerary with places, food, activities, timings"""
    
    def __init__(self):
        self.llm = GoogleGenerativeAI(
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            model="gemini-1.5-flash",
            temperature=0.6
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["outline", "destination", "preferences", "chat_history"],
            template="""
            You are a detailed travel itinerary specialist. Using the provided day-by-day outline,
            create a comprehensive detailed itinerary with specific places, restaurants, activities, and timings.

            Destination: {destination}
            Day-by-day Outline: {outline}
            User Preferences: {preferences}
            Chat History: {chat_history}

            For each day, provide:
            - Specific morning, afternoon, and evening activities
            - Recommended restaurants/cafes with cuisine types
            - Exact locations and addresses when possible
            - Suggested timing for each activity
            - Transportation tips between locations
            - Cost estimates where relevant

            Make sure the itinerary aligns with the user's preferences and is practical to follow.

            Detailed Itinerary:
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def generate_detailed_itinerary(self, outline, destination, preferences, chat_history):
        return self.chain.run(
            outline=outline,
            destination=destination,
            preferences=preferences,
            chat_history=chat_history
        )


class PackingChecklistGenerator:
    """LLM 3: ChatGroq for generating packing checklist based on activities and weather"""
    
    def __init__(self):
        # Use ChatGroq for packing checklist generation
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-8b-instant",  # Using the same model as outline generator
            temperature=0.4  # Lower temperature for more consistent packing recommendations
        )
        
        self.prompt_template = PromptTemplate(
            input_variables=["itinerary", "destination", "chat_history"],
            template="""
            You are a travel packing expert. Based on the detailed itinerary and destination,
            create a comprehensive packing checklist that considers the planned activities and expected weather.

            Destination: {destination}
            Detailed Itinerary: {itinerary}
            Chat History: {chat_history}

            Analyze the activities mentioned in the itinerary and create a packing checklist organized by categories:

            CLOTHING:
            - Weather-appropriate clothing for {destination}
            - Activity-specific clothing (hiking, swimming, formal dining, etc.)

            ELECTRONICS:
            - Essential electronics and accessories

            DOCUMENTS:
            - Travel documents and important papers

            HEALTH & HYGIENE:
            - Personal care items and medications

            ACTIVITY-SPECIFIC ITEMS:
            - Items needed for specific activities mentioned in the itinerary

            MISCELLANEOUS:
            - Other useful items for the trip

            Be specific and practical. Consider the season, climate, and specific activities planned.
            Include quantity suggestions where helpful (e.g., "3-4 t-shirts").

            Packing Checklist:
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def generate_packing_checklist(self, itinerary, destination, chat_history):
        return self.chain.run(
            itinerary=itinerary,
            destination=destination,
            chat_history=chat_history
        )


class TravelPlanner:
    """Main controller class that orchestrates the three LLM classes and manages memory"""
    
    def __init__(self, preferences_file="user_preferences.json"):
        self.preferences_file = preferences_file
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Load persistent preferences
        self.persistent_preferences = self.load_preferences()
        
        self.outline_generator = OutlineGenerator()
        self.detailed_generator = DetailedItineraryGenerator()
        self.packing_generator = PackingChecklistGenerator()
    
    def load_preferences(self):
        """Load preferences from JSON file"""
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Warning: Could not load preferences file: {e}")
            return []
    
    def save_preferences(self):
        """Save preferences to JSON file"""
        try:
            with open(self.preferences_file, 'w') as f:
                json.dump(self.persistent_preferences, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save preferences: {e}")
    
    def extract_preferences_from_memory(self):
        """Extract user preferences from conversation history and persistent storage"""
        # Combine persistent preferences with current session preferences
        all_preferences = self.persistent_preferences.copy()
        
        # Add preferences from current session memory
        chat_history = self.memory.chat_memory.messages
        for message in chat_history:
            content = message.content
            if any(keyword in content.lower() for keyword in ['prefer', 'like', 'love', 'enjoy', 'hate', 'dislike', 'preference']):
                if "User preference:" in content:
                    preference_text = content.split("User preference:")[-1].strip()
                    if preference_text and preference_text not in all_preferences:
                        all_preferences.append(preference_text)
                elif "Preference noted:" in content:
                    preference_text = content.split("Preference noted:")[-1].strip()
                    if preference_text and preference_text not in all_preferences:
                        all_preferences.append(preference_text)
        
        return " | ".join(all_preferences) if all_preferences else "No specific preferences stored yet."
    
    def plan_trip(self, destination, duration):
        """Main method to orchestrate the complete travel planning pipeline"""
        
        print(f"\n🌍 Planning your {duration}-day trip to {destination}...")
        print("=" * 50)
        
        # Get stored preferences
        stored_preferences = self.extract_preferences_from_memory()
        chat_history = str(self.memory.chat_memory.messages)
        
        try:
            # Step 1: Generate outline using ChatGroq
            print("\n📋 Step 1: Generating day-by-day outline...")
            outline = self.outline_generator.generate_outline(
                destination, duration, stored_preferences, chat_history
            )
            print("✅ Outline generated!")
            
            # Step 2: Generate detailed itinerary using Gemini
            print("\n📅 Step 2: Creating detailed itinerary...")
            detailed_itinerary = self.detailed_generator.generate_detailed_itinerary(
                outline, destination, stored_preferences, chat_history
            )
            print("✅ Detailed itinerary created!")
            
            # Step 3: Generate packing checklist using ChatGroq
            print("\n🎒 Step 3: Generating packing checklist...")
            packing_checklist = self.packing_generator.generate_packing_checklist(
                detailed_itinerary, destination, chat_history
            )
            print("✅ Packing checklist ready!")
            
            # Store this conversation in memory
            self.memory.save_context(
                {"input": f"Plan trip to {destination} for {duration} days"},
                {"output": f"Generated complete travel plan including outline, detailed itinerary, and packing list"}
            )
            
            return {
                "outline": outline,
                "detailed_itinerary": detailed_itinerary,
                "packing_checklist": packing_checklist
            }
            
        except Exception as e:
            print(f"❌ Error in travel planning pipeline: {e}")
            raise
    
    def add_preference(self, preference):
        """Allow users to add preferences that will be stored persistently"""
        if preference not in self.persistent_preferences:
            self.persistent_preferences.append(preference)
            self.save_preferences()
        
        # Also add to current session memory
        self.memory.save_context(
            {"input": f"User preference: {preference}"},
            {"output": f"Preference noted: {preference}"}
        )
        print(f"✅ Preference saved: {preference}")
    
    def remove_preference(self, preference):
        """Remove a preference from persistent storage"""
        if preference in self.persistent_preferences:
            self.persistent_preferences.remove(preference)
            self.save_preferences()
            return True
        return False
    
    def show_stored_preferences(self):
        """Display currently stored preferences"""
        if self.persistent_preferences:
            print(f"\n💡 Stored Preferences ({len(self.persistent_preferences)}):")
            for i, pref in enumerate(self.persistent_preferences, 1):
                print(f"   {i}. {pref}")
        else:
            print(f"\n💡 No preferences stored yet.")
    
    def get_all_preferences(self):
        """Get all preferences as a list"""
        return self.persistent_preferences.copy()


def main():
    """Main function to run the Travel Itinerary Planner"""
    
    print("🏖️ Welcome to the AI Travel Itinerary Planner! 🏖️")
    print("This system uses multiple AI models to create your perfect trip:")
    print("• ChatGroq (Llama 3.1-8B) for day-by-day planning")
    print("• Google Gemini Flash for detailed itineraries") 
    print("• ChatGroq (Llama 3.1-8B) for packing lists")
    print("=" * 60)
    
    # Initialize the travel planner
    try:
        planner = TravelPlanner()
        print("✅ AI models initialized successfully!")
        
        # Show existing preferences if any
        if planner.get_all_preferences():
            planner.show_stored_preferences()
            
    except Exception as e:
        print(f"❌ Error initializing AI models. Please check your API keys in .env file.")
        print(f"Error details: {e}")
        return
    
    while True:
        print("\n🎯 What would you like to do?")
        print("1. Plan a new trip")
        print("2. Add a travel preference")
        print("3. View stored preferences")
        print("4. Remove a preference")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            # Plan a new trip
            destination = input("\n📍 Where would you like to travel? ").strip()
            if not destination:
                print("❌ Please enter a valid destination.")
                continue
                
            while True:
                try:
                    duration = int(input("📅 How many days is your trip? "))
                    if duration > 0:
                        break
                    else:
                        print("Please enter a positive number of days.")
                except ValueError:
                    print("Please enter a valid number.")
            
            try:
                # Generate the complete travel plan
                results = planner.plan_trip(destination, duration)
                
                # Display results
                print("\n" + "="*60)
                print("📋 DAY-BY-DAY OUTLINE")
                print("="*60)
                print(results["outline"])
                
                print("\n" + "="*60)
                print("📅 DETAILED ITINERARY")
                print("="*60)
                print(results["detailed_itinerary"])
                
                print("\n" + "="*60)
                print("🎒 PACKING CHECKLIST")
                print("="*60)
                print(results["packing_checklist"])
                
                print("\n🎉 Your complete travel plan is ready!")
                
                # Ask if user wants to save this as a preference
                if input("\n💾 Would you like to add any preferences based on this trip? (y/n): ").lower().startswith('y'):
                    new_pref = input("Enter your preference: ").strip()
                    if new_pref:
                        planner.add_preference(new_pref)
                
            except Exception as e:
                print(f"❌ Error generating travel plan: {e}")
        
        elif choice == "2":
            # Add a preference
            preference = input("\n💡 What's your travel preference? (e.g., 'I prefer nature over museums'): ").strip()
            if preference:
                planner.add_preference(preference)
            else:
                print("❌ Please enter a valid preference.")
        
        elif choice == "3":
            # Show stored preferences
            planner.show_stored_preferences()
        
        elif choice == "4":
            # Remove a preference
            planner.show_stored_preferences()
            if planner.get_all_preferences():
                try:
                    pref_num = int(input("\nEnter the number of the preference to remove: "))
                    if 1 <= pref_num <= len(planner.get_all_preferences()):
                        pref_to_remove = planner.get_all_preferences()[pref_num - 1]
                        if planner.remove_preference(pref_to_remove):
                            print(f"✅ Removed preference: {pref_to_remove}")
                        else:
                            print("❌ Error removing preference.")
                    else:
                        print("❌ Invalid preference number.")
                except ValueError:
                    print("❌ Please enter a valid number.")
        
        elif choice == "5":
            print("\n✈️ Thank you for using the AI Travel Itinerary Planner! Safe travels! 🌍")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    main()
