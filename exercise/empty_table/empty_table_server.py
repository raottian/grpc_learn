

from concurrent import futures
import time
import grpc
import empty_table_pb2
import empty_table_pb2_grpc
import logging

import pandas as pd
import sqlalchemy


_ONE_DAY_IN_SECONDS = 60 * 60 * 24
engine=sqlalchemy.create_engine('mysql+pymysql://icare:ginkodrop@139.224.15.45/vsi_dw_etl?charset=utf8')


class SearchTableServicer(empty_table_pb2_grpc.SearchTableServicer):

  def GetData(self,request,context):
    sql="""select * from %s where date(CreateDate)=date_sub(curdate(),interval 1 day)""" % request.name
    df=pd.read_sql(sql,engine)
    if df.empty:
      return empty_table_pb2.Empty(empty=True,table_name=request)
    else:
      return empty_table_pb2.Empty(empty=False,table_name=request)


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  a=SearchTableServicer()
  empty_table_pb2_grpc.add_SearchTableServicer_to_server(a,server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)


if __name__=='__main__':
  logging.basicConfig()
  serve()

