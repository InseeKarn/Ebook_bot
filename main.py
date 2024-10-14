import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from fpdf import FPDF
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve the API keys from the environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Set up the Discord bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Important for newer versions
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Function to generate outline and fetch chapter content
def find_script(topic):
    outline = [
        "Chapter 1: Introduction - Setting the Stage",
        "Chapter 2: The Origins - Historical Context and Evolution",
        "Chapter 3: Core Principles - Foundational Concepts and Ideas",
        "Chapter 4: Applications in the Real World - Practical Use Cases",
        "Chapter 5: Current Trends - What's Happening Now",
        "Chapter 6: Key Challenges and Opportunities - Navigating the Landscape",
        "Chapter 7: Future Predictions - What Lies Ahead",
        "Chapter 8: Conclusion - Wrapping Up",
        "Appendix: Additional Resources and Further Reading"
    ]

    scripts = []
    for chapter in outline:
        prompt = f"Please generate content for the following chapter:\n{chapter}\nThe content should be approximately one A4 page long and provide valuable insights related to the topic '{topic}'. Ensure it is well-structured, informative, and engaging for the reader."
        # Simulate fetching chapter content from Gemini (replace with actual API call)
        script_content = f"This is the dynamically generated content for '{chapter}' related to '{topic}'. " \
                         "It is designed to fill one A4 page and offer valuable insights."
        scripts.append((chapter, script_content))  # Store both outline and script content as tuples
    
    return scripts  # Return list of tuples

# Function to create PDF
def create_pdf(scripts, output_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", size=17)

    for chapter, content in scripts:
        pdf.multi_cell(0, 10, f"{chapter}\n{content}\n")  # Write both chapter title and content to PDF
    
    pdf.output(output_pdf)
    print(f"PDF '{output_pdf}' created successfully!")

@bot.command()
async def create_ebook(ctx, topic: str):
    await ctx.send(f"Generating eBook for topic: {topic}...")
    
    # Get the outline and scripts
    scripts = find_script(topic)
    
    output_pdf = "ebook_outline.pdf"
    
    # Create PDF from the generated scripts
    create_pdf(scripts, output_pdf)

    # Send the PDF to the Discord channel
    await ctx.send(file=discord.File(output_pdf))

    # Cleanup: remove the PDF after use
    os.remove(output_pdf)

bot.run(DISCORD_TOKEN)
