# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: movie.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bmovie.proto\"\x15\n\x07MovieID\x12\n\n\x02id\x18\x01 \x01(\t\"H\n\tMovieData\x12\r\n\x05title\x18\x01 \x01(\t\x12\x0e\n\x06rating\x18\x02 \x01(\x02\x12\x10\n\x08\x64irector\x18\x03 \x01(\t\x12\n\n\x02id\x18\x04 \x01(\t2/\n\x05Movie\x12&\n\x0cGetMovieByID\x12\x08.MovieID\x1a\n.MovieData\"\x00\x62\x06proto3')



_MOVIEID = DESCRIPTOR.message_types_by_name['MovieID']
_MOVIEDATA = DESCRIPTOR.message_types_by_name['MovieData']
MovieID = _reflection.GeneratedProtocolMessageType('MovieID', (_message.Message,), {
  'DESCRIPTOR' : _MOVIEID,
  '__module__' : 'movie_pb2'
  # @@protoc_insertion_point(class_scope:MovieID)
  })
_sym_db.RegisterMessage(MovieID)

MovieData = _reflection.GeneratedProtocolMessageType('MovieData', (_message.Message,), {
  'DESCRIPTOR' : _MOVIEDATA,
  '__module__' : 'movie_pb2'
  # @@protoc_insertion_point(class_scope:MovieData)
  })
_sym_db.RegisterMessage(MovieData)

_MOVIE = DESCRIPTOR.services_by_name['Movie']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MOVIEID._serialized_start=15
  _MOVIEID._serialized_end=36
  _MOVIEDATA._serialized_start=38
  _MOVIEDATA._serialized_end=110
  _MOVIE._serialized_start=112
  _MOVIE._serialized_end=159
# @@protoc_insertion_point(module_scope)
