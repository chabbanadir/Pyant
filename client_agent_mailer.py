import asyncio
from src.gmail_agent import setup_dependencies, gmail_agent

async def main():
    """Interactive terminal client for the Gmail agent"""
    try:
        print("\n=== Interactive Gmail Agent Client ===")
        agent_deps = setup_dependencies()

        while True:
            prompt = input("\nEnter your prompt (or type '/exit' to quit):\n")
            if prompt.lower() == "/exit":
                break

            try:
                if "search for emails on date" in prompt.lower():
                    date = prompt.split("date")[-1].strip()
                    result = await gmail_agent.run(f"search for emails on date {date}", deps=agent_deps)
                else:
                    result = await gmail_agent.run(prompt, deps=agent_deps)
                print("\n=== Agent Response ===")
                print(result.data)
                print("===\n")
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            print("Another event loop is already running. This can happen in interactive environments.")
            print("Attempting to use a different method to run the client...")
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            print(f"\n❌ Error: {str(e)}")
    print("\n=== Client Terminated ===")
