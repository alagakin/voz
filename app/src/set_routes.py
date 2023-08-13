import asyncio

from parser.services import parse


def main():
    asyncio.run(parse())


if __name__ == "__main__":
    main()
