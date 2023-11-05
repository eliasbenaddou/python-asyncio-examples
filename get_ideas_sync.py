import logging
from time import perf_counter

import requests
from tqdm import tqdm


def main(amount: int) -> None:
    """Main function to write headers to a file and call endpoints synchronously.

    Args:
        amount (int): Number of times to make the endpoint call
    """
    with open("ideas_sync.csv", "w") as f:
        f.write("activity,type,participants,price,link,key,accessibility")
        for _ in tqdm(range(amount)):
            response = requests.request("GET", url).json()
            activity = response["activity"]
            activity_type = response["type"]
            participants = response["participants"]
            price = response["price"]
            link = response["link"]
            key = response["key"]
            accessibility = response["accessibility"]
            f.write(
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


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    amount = int(input("Enter the amount of ideas to get: "))

    start_time = perf_counter()
    url = "https://www.boredapi.com/api/activity"
    main(amount)
    end_time = perf_counter()
    logger.info(
        f"{amount} activity ideas fetched in {perf_counter() - start_time:0.2f} seconds."
    )
