#!/usr/bin


# but in coroutiome !!
# if running dint run write logic for it :wq
python3 main.py &

cd message_handlers
python3 coin_message_handler.py &

cd ../side_tasks
python3 keep_updated.py &

cd ../../data_handler
python3 tracker.py
