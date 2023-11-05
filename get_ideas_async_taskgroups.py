import asyncio
import logging
from time import perf_counter

import aiofiles
from aiofiles.threadpool.text import AsyncTextIOWrapper as AsyncIOFile
from aiohttp import ClientSession


async def make_endpoint_calls(url: str, amount: int, outfile: AsyncIOFile) -> None:
    """Create a number of async tasks based on the input amount and gather.

    Args:
        url (str): The URL to fetch data from
        amount (int): Number of times to make the endpoint call
        outfile (AsyncIOFile): The path to the file to write data to
    """
    async with ClientSession() as session:
        try:
            async with asyncio.TaskGroup() as tg:
                for _ in range(amount):
                    tg.create_task(make_get_request(session, url, outfile))
        except Exception as e:
            logger.error(e)
            raise e


async def make_get_request(
    session: ClientSession, url: str, outfile: AsyncIOFile
) -> None:
    """Make the GET request and write the data to the outfile.

    Args:
        session (ClientSession): aiohttp client session
        outfile (AsyncIOFile): The path to the file to write data to
    """
    async with session.get(url=url) as resp:
        response = await resp.json()
        activity = response["activity"]
        activity_type = response["type"]
        participants = response["participantss"]
        price = response["price"]
        link = response["link"]
        key = response["key"]
        accessibility = response["accessibility"]
        await outfile.write(
            "\n"
            + activity
            + ","
            + activity_type
            + ","
            + str(participants)
            + ","
            + str(price)
            + ","
            + link
            + ","
            + key
            + ","
            + str(accessibility)
        )


async def main(url: str, amount: int) -> None:
    """Main function to write headers to a file, call endpoints and write data asynchronously.

    Args:
        url (str): The URL to fetch data from
        amount (int): Number of times to make the endpoint call
    """
    start_time = perf_counter()
    async with aiofiles.open("ideas.csv", "w") as outfile:
        await outfile.write("activity,type,participants,price,link,key,accessibility")
        await make_endpoint_calls(url, amount, outfile)
    logger.info(
        f"{amount} activity ideas fetched in {perf_counter() - start_time:0.2f} seconds."
    )


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    url = "https://www.boredapi.com/api/activity"
    amount = int(input("Enter the amount of ideas to get: "))
    asyncio.run(main(url, amount))
