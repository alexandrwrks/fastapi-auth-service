import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from notification_service.rabbit.subscriber import router

broker = RabbitBroker()

broker.include_router(router)

app = FastStream(broker)


async def main():
    print("Подключение к FastStream")

    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
