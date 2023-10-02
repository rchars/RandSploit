# import Interpreter.state as state
# import concurrent.futures as cf
# import sys
#
#
# def recv_data_q(queue):
# 	# while parent_conn.poll() and (buff := parent_conn.recv()):'
# 	try:
# 		while True:
# 			print(queue.get(), end='')
# 	except Exception as e:
# 		print(e)
#
#
# def send_data_q(queue):
# 	# problem with gnu readline
# 	while True: queue.put(sys.stdin.readline())
#
#
# def recv_data(parent_conn):
# 	# while parent_conn.poll() and (buff := parent_conn.recv()):'
# 	try:
# 		while True:
# 			if not parent_conn.poll(): break
# 	except Exception as e:
# 		print(e)
#
#
# def send_data(queue):
# 	# problem with gnu readline
# 	while True: queue.put(sys.stdin.readline())
#
#
#
# def execute(session_number):
# 	session = state.BACKGROUND_MODS[session_number := int(session_number)].session
# 	try:
# 		with cf.ThreadPoolExecutor(max_workers=2) as proc_handler:
# 			threads = [
# 				proc_handler.submit(recv_data_q, session.out_queue),
# 				proc_handler.submit(send_data_q, session.in_queue)
# 			]
# 			for thread in threads: thread.result(timeout=0)
# 		proc_handler.shutdown()
# 	finally:
# 		if session.is_alive():
# 			session.terminate()


def execute(): print('Not implemented')