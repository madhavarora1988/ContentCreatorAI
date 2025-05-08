import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, trace

# Step 1: Topic Analysis Agent
topic_analysis_agent = Agent(
    name="topic_analysis_agent",
    instructions="""Analyze the given topic and generate a structured outline with:
    1. Main points to cover
    2. Key subtopics
    3. Target audience
    4. Estimated word count
    Format the output as a clear, structured outline.""",
    output_type=str
)

# Step 2: Content Structure Agent
class ContentStructure(BaseModel):
    introduction: str
    main_sections: list[str]
    conclusion: str
    keywords: list[str]

content_structure_agent = Agent(
    name="content_structure_agent",
    instructions="""Based on the topic analysis, create a detailed content structure.
    Include a compelling introduction, main sections with bullet points, and a conclusion.
    Also identify key SEO keywords for the content.""",
    output_type=ContentStructure
)

# Step 3: Content Generation Agent
content_generation_agent = Agent(
    name="content_generation_agent",
    instructions="""Write a complete blog post based on the provided structure.
    Ensure the content is engaging, well-researched, and follows the structure exactly.
    Include the identified keywords naturally throughout the content.""",
    output_type=str
)

async def create_blog_post(topic: str):
    # Step 1: Analyze the topic
    print("Analyzing topic...")
    analysis_result = await Runner.run(
        topic_analysis_agent,
        topic
    )
    print("Topic analysis complete")

    # Step 2: Create content structure
    print("Creating content structure...")
    structure_result = await Runner.run(
        content_structure_agent,
        analysis_result.final_output
    )
    print("Content structure created")

    # Step 3: Generate the full content
    print("Generating content...")
    content_structure_str = (
        f"Introduction: {structure_result.final_output.introduction}\n"
        f"Main Sections: {', '.join(structure_result.final_output.main_sections)}\n"
        f"Conclusion: {structure_result.final_output.conclusion}\n"
        f"Keywords: {', '.join(structure_result.final_output.keywords)}"
    )
    content_result = await Runner.run(
        content_generation_agent,
        content_structure_str
    )
    print("Content generation complete")

    return {
        "analysis": analysis_result.final_output,
        "structure": structure_result.final_output,
        "content": content_result.final_output
    }

async def main():
    topic = input("Enter the blog post topic: ")
    result = await create_blog_post(topic)
    
    print("\n=== Final Blog Post ===")
    print(result["content"])

if __name__ == "__main__":
    asyncio.run(main()) 