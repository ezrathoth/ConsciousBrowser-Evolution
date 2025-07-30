import argparse
import asyncio

from app.agent.L1B3RT4S import L1B3RT4S
from app.logger import logger


async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run L1B3RT4S agent with a prompt")
    parser.add_argument(
        "--prompt", type=str, required=False, help="Input prompt for the agent"
    )
    args = parser.parse_args()

    # Create and initialize L1B3RT4S agent
    agent = await L1B3RT4S.create()
    try:
        # Use command line prompt if provided, otherwise ask for input
        prompt = args.prompt if args.prompt else input("Enter your prompt: ")
        if not prompt.strip():
            logger.warning("Empty prompt provided.")
            return

        logger.warning("Processing your request...")
        await agent.run(prompt)
        logger.info("Request processing completed.")
    except KeyboardInterrupt:
        logger.warning("Operation interrupted.")
    finally:
        # Ensure agent resources are cleaned up before exiting
        await agent.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
