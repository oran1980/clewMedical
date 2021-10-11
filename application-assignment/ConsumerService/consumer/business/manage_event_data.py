import ast

import pandas as pd

from ConsumerService.consumer.model.patient_med_event import PatientMedEvent
from model.patient_med import PatientsMeds
from ConsumerService.consumer.persistence.db import Session, db_engine, Base

# generate database schema
Base.metadata.create_all(db_engine)
# create a new session
session = Session()


def get_patient_med_period(p_id, med):
    results = session.query(PatientsMeds). \
        filter(PatientsMeds.p_id == p_id, PatientsMeds.medication_name == med,
               PatientsMeds.medication_period_end.isnot(None))

    return results


def get_patient_all_meds_periods(p_id):
    results = session.query(PatientsMeds). \
        filter(PatientsMeds.p_id == p_id, PatientsMeds.medication_name.isnot(None),
               PatientsMeds.medication_period_start.isnot(None))

    return results


def save_event(event_str):
    global session
    if session is None:
        session = Session()

    event_dict = ast.literal_eval(event_str)
    print(event_dict)
    event = PatientMedEvent(**event_dict)

    print("saving event record to DB: %", event_str)

    # verify datetime string format
    # datestr = '2021-10-07 00:00:00'
    date_format = "%Y-%m-%d %H:%M:%S"

    try:
        medication_period_start = pd.to_datetime(event.event_time, format=date_format, errors='raise')
        # datetime.datetime.strptime(event.event_time, date_format)
        print("event date format has been verified ({})".format(medication_period_start))

        # handle start
        if event.action == 'start':
            # Read
            nrows = session.query(PatientsMeds). \
                filter(PatientsMeds.p_id == event.p_id, PatientsMeds.medication_name == event.medication_name,
                       PatientsMeds.medication_period_start == medication_period_start). \
                count()

            if nrows == 0:
                # Insert new record
                record = PatientsMeds(event.p_id, event.medication_name, medication_period_start, None)
                # persisting data
                session.add(record)
                session.commit()
        elif event.action == 'cancel_start':
            # delete the record
            session.query(PatientsMeds). \
                filter(PatientsMeds.p_id == event.p_id, PatientsMeds.medication_name == event.medication_name,
                       PatientsMeds.medication_period_end.is_(None), PatientsMeds.medication_period_start.isnot(None)). \
                delete(synchronize_session='fetch')
            session.commit()
        elif event.action == 'stop':
            # update
            # handle stop
            patient_med = session.query(PatientsMeds). \
                filter(PatientsMeds.p_id == event.p_id, PatientsMeds.medication_name == event.medication_name,
                       PatientsMeds.medication_period_start.isnot(None), PatientsMeds.medication_period_end.is_(None))

            patient_med.update({PatientsMeds.medication_period_end: event.event_time})
            session.commit()
        else:
            # handle cancel stop
            patient_med = session.query(PatientsMeds). \
                filter(PatientsMeds.p_id == event.p_id, PatientsMeds.medication_name == event.medication_name,
                       PatientsMeds.medication_period_end.isnot(None))

            patient_med.update({PatientsMeds.medication_period_end: None})
            session.commit()
    except ValueError:
        print("Wrong event date format \'{}\'. event has not been saved/updated. "
              "please fix the date format and try again.".format(event.event_time))
