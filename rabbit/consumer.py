import json
from datetime import datetime

import aio_pika
import asyncio
from database import async_session_maker
from rabbit.models.logs_model import LogsModel


class Consumer:
    def __init__(self):
        self.channel = None
        self.connection = None

    async def set_pika_connection(self, ):
        self.connection = await aio_pika.connect_robust(host='localhost', port=5672)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)

        queue = await self.channel.declare_queue('queue', auto_delete=False)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    data = self.decode_bytes(body=message.body)
                    await self.create_logs(data=data, queue=queue)

                    if queue.name in message.body.decode():
                        break

    def decode_bytes(self, body):
        decoded_str = body.decode('utf-8')
        return json.loads(decoded_str)

    async def create_logs(self, data, queue):
        async with async_session_maker() as session:
            datetime_str = data.pop('datetime_open')
            datatime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')

            log = LogsModel(datetime_open=datatime, **data)
            session.add(log)
            await session.commit()
            queue.delete()


async def main():
    await Consumer().set_pika_connection()


if __name__ == "__main__":
    asyncio.run(main())
