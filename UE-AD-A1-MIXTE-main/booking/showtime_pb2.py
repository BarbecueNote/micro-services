# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: showtime.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eshowtime.proto\"\x19\n\tTimestamp\x12\x0c\n\x04time\x18\x01 \x01(\t\"\x15\n\x07MovieID\x12\n\n\x02id\x18\x01 \x01(\t\"&\n\tSchedules\x12\x0c\n\x04time\x18\x01 \x01(\t\x12\x0b\n\x03ids\x18\x02 \x03(\t\"\x0e\n\x0c\x45mptyMessage2b\n\x08Showtime\x12*\n\x0eGetMovieByTime\x12\n.Timestamp\x1a\x08.MovieID\"\x00\x30\x01\x12*\n\tShowtimes\x12\r.EmptyMessage\x1a\n.Schedules\"\x00\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'showtime_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_TIMESTAMP']._serialized_start=18
  _globals['_TIMESTAMP']._serialized_end=43
  _globals['_MOVIEID']._serialized_start=45
  _globals['_MOVIEID']._serialized_end=66
  _globals['_SCHEDULES']._serialized_start=68
  _globals['_SCHEDULES']._serialized_end=106
  _globals['_EMPTYMESSAGE']._serialized_start=108
  _globals['_EMPTYMESSAGE']._serialized_end=122
  _globals['_SHOWTIME']._serialized_start=124
  _globals['_SHOWTIME']._serialized_end=222
# @@protoc_insertion_point(module_scope)
