import logging
import asyncio
import os
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import queue
import time, threading

class EventHubHandler(logging.StreamHandler):
    """
    A handler class which stores logs in queue
    """
    def __init__(self):
        super().__init__()

        #### ENV VARIABLES ####
        self.connection_string = os.environ.get("eh_ns_connection_string") or self.closeProgram("eh_ns_connection_string env variable needed")
        self.eventhub_name = os.environ.get("eventhub_name") or self.closeProgram("eventhub_name env variable needed")
        self.bulk_size = os.environ.get("bulk_size") or 10
        self.freq = os.environ.get("frequency") or 5

        ## queue
        self.logQueue = queue.Queue()

        ## separate thread
        self.logThread = threading.Thread(target=self.threadLoop)
        self.logThread.daemon = True
        self.logThread.start()

    def emit(self, record: logging.LogRecord):
        try:
            msg = self.format(record)
            self.logQueue.put(msg)
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    async def sendLogs(self):
        """
        A function which send logs from queue to event hub 
        """
        producer = EventHubProducerClient.from_connection_string(conn_str=self.connection_string, eventhub_name=self.eventhub_name)
        async with producer:
            # Create a batch.
            event_data_batch = await producer.create_batch()

            # Add events to the batch.
            counter = self.bulk_size
            sendFlag = False
            
            while not self.logQueue.empty() and counter > 0:
                sendFlag = True
                log = self.logQueue.get()
                event_data_batch.add(EventData(log))
                counter = counter - 1

            # Send the batch of events to the event hub. 
            if sendFlag:       
                await producer.send_batch(event_data_batch)
        

    def threadLoop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while True:
            loop.run_until_complete(self.sendLogs())
            time.sleep(self.freq)

    def closeProgram(self, msg: str):
        print(msg)
        exit(1)
