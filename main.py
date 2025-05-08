import sys
import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, trace
from blog_creator import main as blog_creator_main, create_blog_post, topic_analysis_agent, content_structure_agent


def print_menu():
    print("\n=== Content Creator AI ===")
    print("Select a pattern to run:")
    print("1. Deterministic Blog Creator")
    print("2. Blog + Social Summaries (Blog, Tweet, LinkedIn)")
    print("3. Blog + Social + SEO Keywords")
    print("4. Blog + Social + SEO + Judge")
    print("5. Blog Parallelization (Multiple Styles)")
    print("6. Full Suite: Blog + Social + SEO + Judge + Parallel Video Scripts")
    print("7. Full Suite + Guardrails (Input & Output)")
    print("0. Exit")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            asyncio.run(blog_creator_main())
        elif choice == "2":
            async def blog_and_social():
                topic = input("Enter the blog post topic: ")
                result = await create_blog_post(topic)
                blog_content = result["content"]
                print("\n=== Final Blog Post ===\n" + blog_content)

                # Social summary agents
                tweet_agent = Agent(
                    name="tweet_agent",
                    instructions="""
                    Write a concise, engaging tweet (max 280 characters) summarizing the following blog post. Use a friendly, conversational tone and include relevant hashtags if appropriate.
                    """,
                    output_type=str
                )
                linkedin_agent = Agent(
                    name="linkedin_agent",
                    instructions="""
                    Write a professional LinkedIn post introducing and summarizing the following blog post. Use a formal yet approachable tone, highlight key insights, and encourage engagement.
                    """,
                    output_type=str
                )
                print("\nGenerating Tweet summary...")
                tweet_result = await Runner.run(tweet_agent, blog_content)
                print("\n=== Tweet Summary ===\n" + tweet_result.final_output)
                print("\nGenerating LinkedIn summary...")
                linkedin_result = await Runner.run(linkedin_agent, blog_content)
                print("\n=== LinkedIn Summary ===\n" + linkedin_result.final_output)

            asyncio.run(blog_and_social())
        elif choice == "3":
            async def blog_social_seo():
                topic = input("Enter the blog post topic: ")
                result = await create_blog_post(topic)
                blog_content = result["content"]
                print("\n=== Final Blog Post ===\n" + blog_content)

                # Social summary agents
                tweet_agent = Agent(
                    name="tweet_agent",
                    instructions="""
                    Write a concise, engaging tweet (max 280 characters) summarizing the following blog post. Use a friendly, conversational tone and include relevant hashtags if appropriate.
                    """,
                    output_type=str
                )
                linkedin_agent = Agent(
                    name="linkedin_agent",
                    instructions="""
                    Write a professional LinkedIn post introducing and summarizing the following blog post. Use a formal yet approachable tone, highlight key insights, and encourage engagement.
                    """,
                    output_type=str
                )
                seo_keyword_agent = Agent(
                    name="seo_keyword_agent",
                    instructions="""
                    Extract the top 5 SEO keywords or phrases from the following blog post. Return them as a comma-separated list.
                    """,
                    output_type=str
                )
                print("\nGenerating Tweet summary...")
                tweet_result = await Runner.run(tweet_agent, blog_content)
                print("\n=== Tweet Summary ===\n" + tweet_result.final_output)
                print("\nGenerating LinkedIn summary...")
                linkedin_result = await Runner.run(linkedin_agent, blog_content)
                print("\n=== LinkedIn Summary ===\n" + linkedin_result.final_output)
                print("\nExtracting SEO keywords...")
                seo_result = await Runner.run(seo_keyword_agent, blog_content)
                print("\n=== SEO Keywords ===\n" + seo_result.final_output)

            asyncio.run(blog_social_seo())
        elif choice == "4":
            class JudgeOutput(BaseModel):
                score: int
                feedback: str

            async def blog_social_seo_judge():
                topic = input("Enter the blog post topic: ")
                result = await create_blog_post(topic)
                blog_content = result["content"]
                print("\n=== Final Blog Post ===\n" + blog_content)

                # Social summary agents
                tweet_agent = Agent(
                    name="tweet_agent",
                    instructions="""
                    Write a concise, engaging tweet (max 280 characters) summarizing the following blog post. Use a friendly, conversational tone and include relevant hashtags if appropriate.
                    """,
                    output_type=str
                )
                linkedin_agent = Agent(
                    name="linkedin_agent",
                    instructions="""
                    Write a professional LinkedIn post introducing and summarizing the following blog post. Use a formal yet approachable tone, highlight key insights, and encourage engagement.
                    """,
                    output_type=str
                )
                seo_keyword_agent = Agent(
                    name="seo_keyword_agent",
                    instructions="""
                    Extract the top 5 SEO keywords or phrases from the following blog post. Return them as a comma-separated list.
                    """,
                    output_type=str
                )
                judge_agent = Agent(
                    name="judge_agent",
                    instructions="""
                    You are a writing quality judge. Read the following blog post and provide:
                    - A quality score from 1 (poor) to 10 (excellent)
                    - Brief feedback on how to improve the post
                    Return your answer as a JSON object with 'score' and 'feedback'.
                    """,
                    output_type=JudgeOutput
                )
                print("\nGenerating Tweet summary...")
                tweet_result = await Runner.run(tweet_agent, blog_content)
                print("\n=== Tweet Summary ===\n" + tweet_result.final_output)
                print("\nGenerating LinkedIn summary...")
                linkedin_result = await Runner.run(linkedin_agent, blog_content)
                print("\n=== LinkedIn Summary ===\n" + linkedin_result.final_output)
                print("\nExtracting SEO keywords...")
                seo_result = await Runner.run(seo_keyword_agent, blog_content)
                print("\n=== SEO Keywords ===\n" + seo_result.final_output)
                print("\nJudging blog quality...")
                judge_result = await Runner.run(judge_agent, blog_content)
                print(f"\n=== Judge Feedback ===\nScore: {judge_result.final_output.score}\nFeedback: {judge_result.final_output.feedback}")

            asyncio.run(blog_social_seo_judge())
        elif choice == "5":
            async def blog_parallel():
                topic = input("Enter the blog post topic: ")
                with trace("Blog Parallelization Flow"):
                    print("Analyzing topic...")
                    analysis_result = await Runner.run(
                        topic_analysis_agent,
                        topic
                    )
                    print("Topic analysis complete")
                    print("Creating content structure...")
                    structure_result = await Runner.run(
                        content_structure_agent,
                        analysis_result.final_output
                    )
                    print("Content structure created\n")
                    structure = structure_result.final_output
                    content_structure_str = (
                        f"Introduction: {structure.introduction}\n"
                        f"Main Sections: {', '.join(structure.main_sections)}\n"
                        f"Conclusion: {structure.conclusion}\n"
                        f"Keywords: {', '.join(structure.keywords)}"
                    )
                    # Define agents for each style
                    professional_agent = Agent(
                        name="professional_blog_agent",
                        instructions="""
                        Write a professional, well-structured blog post based on the provided structure. Use a formal tone and ensure clarity and depth.
                        """,
                        output_type=str
                    )
                    youtube_agent = Agent(
                        name="youtube_transcript_agent",
                        instructions="""
                        Write a transcript for a YouTube video based on the provided structure. The transcript should be engaging, clear, and suitable for a 5-10 minute video.
                        """,
                        output_type=str
                    )
                    tiktok_agent = Agent(
                        name="tiktok_transcript_agent",
                        instructions="""
                        Write a short, punchy transcript for a TikTok video (under 1 minute) based on the provided structure. Make it catchy and suitable for a fast-paced video.
                        """,
                        output_type=str
                    )
                    print("Generating all styles in parallel...")
                    results = await asyncio.gather(
                        Runner.run(professional_agent, content_structure_str),
                        Runner.run(youtube_agent, content_structure_str),
                        Runner.run(tiktok_agent, content_structure_str)
                    )
                    print("\n=== Professional Blog Post ===\n" + results[0].final_output)
                    print("\n=== YouTube Video Transcript ===\n" + results[1].final_output)
                    print("\n=== TikTok Video Transcript ===\n" + results[2].final_output)

            asyncio.run(blog_parallel())
        elif choice == "6":
            class JudgeOutput(BaseModel):
                score: int
                feedback: str

            async def full_suite():
                topic = input("Enter the blog post topic: ")
                with trace("Full Suite Flow"):
                    # Blog (professional)
                    result = await create_blog_post(topic)
                    blog_content = result["content"]
                    print("\n=== Final Blog Post (Professional) ===\n" + blog_content)

                    # Social summary agents
                    tweet_agent = Agent(
                        name="tweet_agent",
                        instructions="""
                        Write a concise, engaging tweet (max 280 characters) summarizing the following blog post. Use a friendly, conversational tone and include relevant hashtags if appropriate.
                        """,
                        output_type=str
                    )
                    linkedin_agent = Agent(
                        name="linkedin_agent",
                        instructions="""
                        Write a professional LinkedIn post introducing and summarizing the following blog post. Use a formal yet approachable tone, highlight key insights, and encourage engagement.
                        """,
                        output_type=str
                    )
                    seo_keyword_agent = Agent(
                        name="seo_keyword_agent",
                        instructions="""
                        Extract the top 5 SEO keywords or phrases from the following blog post. Return them as a comma-separated list.
                        """,
                        output_type=str
                    )
                    judge_agent = Agent(
                        name="judge_agent",
                        instructions="""
                        You are a writing quality judge. Read the following blog post and provide:
                        - A quality score from 1 (poor) to 10 (excellent)
                        - Brief feedback on how to improve the post
                        Return your answer as a JSON object with 'score' and 'feedback'.
                        """,
                        output_type=JudgeOutput
                    )
                    youtube_agent = Agent(
                        name="youtube_transcript_agent",
                        instructions="""
                        Write a transcript for a YouTube video based on the following blog post. The transcript should be engaging, clear, and suitable for a 5-10 minute video.
                        """,
                        output_type=str
                    )
                    tiktok_agent = Agent(
                        name="tiktok_transcript_agent",
                        instructions="""
                        Write a short, punchy transcript for a TikTok video (under 1 minute) based on the following blog post. Make it catchy and suitable for a fast-paced video.
                        """,
                        output_type=str
                    )
                    print("\nGenerating Tweet and LinkedIn summaries, SEO keywords, judging blog quality, and video transcripts in parallel...")
                    tweet_result, linkedin_result, seo_result, judge_result, youtube_result, tiktok_result = await asyncio.gather(
                        Runner.run(tweet_agent, blog_content),
                        Runner.run(linkedin_agent, blog_content),
                        Runner.run(seo_keyword_agent, blog_content),
                        Runner.run(judge_agent, blog_content),
                        Runner.run(youtube_agent, blog_content),
                        Runner.run(tiktok_agent, blog_content)
                    )
                    print("\n=== Tweet Summary ===\n" + tweet_result.final_output)
                    print("\n=== LinkedIn Summary ===\n" + linkedin_result.final_output)
                    print("\n=== SEO Keywords ===\n" + seo_result.final_output)
                    print(f"\n=== Judge Feedback ===\nScore: {judge_result.final_output.score}\nFeedback: {judge_result.final_output.feedback}")
                    print("\n=== YouTube Video Transcript ===\n" + youtube_result.final_output)
                    print("\n=== TikTok Video Transcript ===\n" + tiktok_result.final_output)

            asyncio.run(full_suite())
        elif choice == "7":
            class JudgeOutput(BaseModel):
                score: int
                feedback: str

            class GuardrailOutput(BaseModel):
                valid: bool
                reason: str

            async def full_suite_guardrails():
                topic = input("Enter the blog post topic: ")
                input_guardrail_agent = Agent(
                    name="input_guardrail_agent",
                    instructions="""
                    Check if the following topic is appropriate for content creation. It should not be offensive, too short, or irrelevant. 
                    Return valid: true if the topic is acceptable, otherwise valid: false and a reason.
                    Return your answer as a JSON object with 'valid' and 'reason'.
                    """,
                    output_type=GuardrailOutput
                )
                with trace("Full Suite + Guardrails Flow"):
                    print("Checking input guardrails...")
                    guardrail_result = await Runner.run(input_guardrail_agent, topic)
                    if not guardrail_result.final_output.valid:
                        print(f"Input guardrail tripped: {guardrail_result.final_output.reason}")
                        return
                    print("Input passed guardrails. Proceeding...\n")
                    # Blog (professional)
                    result = await create_blog_post(topic)
                    blog_content = result["content"]
                    output_guardrail_agent = Agent(
                        name="output_guardrail_agent",
                        instructions="""
                        Check if the following blog post is appropriate for publication. It should not contain offensive language, must be at least 200 words, and should be relevant to the topic. 
                        Return valid: true if the blog is acceptable, otherwise valid: false and a reason.
                        Return your answer as a JSON object with 'valid' and 'reason'.
                        """,
                        output_type=GuardrailOutput
                    )
                    print("Checking output guardrails...")
                    output_guardrail_result = await Runner.run(output_guardrail_agent, blog_content)
                    if not output_guardrail_result.final_output.valid:
                        print(f"Output guardrail tripped: {output_guardrail_result.final_output.reason}")
                        return
                    print("Output passed guardrails. Proceeding...\n")
                    # Social summary agents
                    tweet_agent = Agent(
                        name="tweet_agent",
                        instructions="""
                        Write a concise, engaging tweet (max 280 characters) summarizing the following blog post. Use a friendly, conversational tone and include relevant hashtags if appropriate.
                        """,
                        output_type=str
                    )
                    linkedin_agent = Agent(
                        name="linkedin_agent",
                        instructions="""
                        Write a professional LinkedIn post introducing and summarizing the following blog post. Use a formal yet approachable tone, highlight key insights, and encourage engagement.
                        """,
                        output_type=str
                    )
                    seo_keyword_agent = Agent(
                        name="seo_keyword_agent",
                        instructions="""
                        Extract the top 5 SEO keywords or phrases from the following blog post. Return them as a comma-separated list.
                        """,
                        output_type=str
                    )
                    judge_agent = Agent(
                        name="judge_agent",
                        instructions="""
                        You are a writing quality judge. Read the following blog post and provide:
                        - A quality score from 1 (poor) to 10 (excellent)
                        - Brief feedback on how to improve the post
                        Return your answer as a JSON object with 'score' and 'feedback'.
                        """,
                        output_type=JudgeOutput
                    )
                    youtube_agent = Agent(
                        name="youtube_transcript_agent",
                        instructions="""
                        Write a transcript for a YouTube video based on the following blog post. The transcript should be engaging, clear, and suitable for a 5-10 minute video.
                        """,
                        output_type=str
                    )
                    tiktok_agent = Agent(
                        name="tiktok_transcript_agent",
                        instructions="""
                        Write a short, punchy transcript for a TikTok video (under 1 minute) based on the following blog post. Make it catchy and suitable for a fast-paced video.
                        """,
                        output_type=str
                    )
                    print("\nGenerating all outputs in parallel...")
                    tweet_result, linkedin_result, seo_result, judge_result, youtube_result, tiktok_result = await asyncio.gather(
                        Runner.run(tweet_agent, blog_content),
                        Runner.run(linkedin_agent, blog_content),
                        Runner.run(seo_keyword_agent, blog_content),
                        Runner.run(judge_agent, blog_content),
                        Runner.run(youtube_agent, blog_content),
                        Runner.run(tiktok_agent, blog_content)
                    )
                    print("\n=== Final Blog Post (Professional) ===\n" + blog_content)
                    print("\n=== Tweet Summary ===\n" + tweet_result.final_output)
                    print("\n=== LinkedIn Summary ===\n" + linkedin_result.final_output)
                    print("\n=== SEO Keywords ===\n" + seo_result.final_output)
                    print(f"\n=== Judge Feedback ===\nScore: {judge_result.final_output.score}\nFeedback: {judge_result.final_output.feedback}")
                    print("\n=== YouTube Video Transcript ===\n" + youtube_result.final_output)
                    print("\n=== TikTok Video Transcript ===\n" + tiktok_result.final_output)

            asyncio.run(full_suite_guardrails())
        elif choice == "0":
            print("Exiting.")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 