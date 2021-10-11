import asyncio
import threading
from sqlalchemy.orm import Query

from ConsumerService.consumer.persistence import db
from ConsumerService.consumer.business import manage_event_data
from aio_pika import connect, ExchangeType
from flask import Flask, request, jsonify, Response

app = Flask(__name__)


@app.route('/getPatientMedsPeriods')
def get_patient_med_period():
    p_id = request.args['p_id']
    med = request.args['med']
    patient_meds_periods = []
    result = manage_event_data.get_patient_med_period(p_id, med)
    if isinstance(result,Query):
        _len = result.count()
    else:
        _len = len(result)

    if _len > 0:
        for r in result:
            a = {"p_id": r.p_id, "medication_name": r.medication_name,
                 "medication_period_start": r.medication_period_start,
                 "medication_period_end": r.medication_period_end}
            patient_meds_periods.append(a)
        return jsonify(patient_meds_periods)
    else:  # No elements in the result --> return NOT_FOUND_404
        return Response('No medication periods has been found for patient {} with medication: {}'.format(p_id, med),
                        404)


@app.route('/getPatientAllMedsPeriods')
def get_patient_all_meds_period():
    p_id = request.args['p_id']
    patient_meds_periods = []
    result = manage_event_data.get_patient_all_meds_periods(p_id)
    if isinstance(result,Query):
        _len = result.count()
    else:
        _len = len(result)

    if _len > 0:
        for r in result:
            a = {"p_id": r.p_id, "medication_name": r.medication_name,
                 "medication_period_start": r.medication_period_start,
                 "medication_period_end": r.medication_period_end}
            patient_meds_periods.append(a)
        return jsonify(patient_meds_periods)
    else:  # No elements in the result --> return NOT_FOUND_404
        return Response('No medication periods has been found for patient:{}'.format(p_id), 404)


async def main(loop):
    print("Connecting to the PostgreSQL database...")

    if not db.is_table_exist():
        conn = db.create_tables()
    else:
        conn = db.get_connection()

    connection = await connect(host="localhost",
                               login="admin",
                               password="password",
                               loop=loop
                               )
    # connection = await connect(host=os.environ.get('RABBIT_HOST'),
    #                            login=os.environ.get('RABBIT_USER'),
    #                            password=os.environ.get('RABBIT_PASS'),
    #                            loop=loop
    #                            )

    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring the queue
        queue = await channel.declare_queue(name='events', auto_delete=True)
        exchange = await channel.declare_exchange("meds", ExchangeType.FANOUT)
        routing_key = "new.events"
        await queue.bind(exchange, routing_key)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    event_str = message.body.decode('UTF-8')
                    manage_event_data.save_event(event_str)

if __name__ == '__main__':

    # start flask on separate thread
    threading.Thread(target=lambda : app.run(debug=True, use_reloader=False)).start()
    # Get the current event loop.
    # If there is no current event loop set in the current OS thread, 
    # the OS thread is main, and set_event_loop() has not yet been called, 
    # asyncio will create a new event loop and set it as the current one.
    loop = asyncio.get_event_loop()
    if loop is not None:
        loop.run_until_complete(main(loop))
    else:
        print("Error establishing event loop!")
