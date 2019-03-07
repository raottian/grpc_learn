

import logging
import grpc
import empty_table_pb2
import empty_table_pb2_grpc


def run():

  channel=grpc.insecure_channel('localhost:50051')

  stub=empty_table_pb2_grpc.SearchTableStub(channel)
  result=stub.GetData(empty_table_pb2.Table(name='fourier_traininglist'))

  if result.empty:

    print("Alert!!!!!!!!Table called %s is empty" % result.table_name.name)

  else:
    print("It is OK!Table called %s is not empty" % result.table_name.name)


if __name__ == '__main__':
    logging.basicConfig()
    run()
