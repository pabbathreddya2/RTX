#!/usr/bin/python3
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

import re
import os
import sys
import subprocess
import json
import datetime
import ast

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../../../")
from RTXConfiguration import RTXConfiguration

from QueryMeSH import QueryMeSH
from swagger_server.models.response import Response

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../../reasoningtool/QuestionAnswering/")
from ParseQuestion import ParseQuestion

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../Feedback/")
from RTXFeedback import RTXFeedback

class RTXQuery:

  def query(self,query):

    #### Get our configuration information
    


    #### If there is no known_query_type_id, then return an error
    if "known_query_type_id" not in query:
      response = Response()
      response.result_code = "No_known_query_type_id"
      response.message = "There was no known_query_type_id specified in the query"
      return(response)

    #### If there is no terms, then return an error
    if "terms" not in query:
      response = Response()
      response.result_code = "No_terms"
      response.message = "There was no terms element specified in the query"
      return(response)

    #### Extract the id and the terms from the incoming parameters
    id = query["known_query_type_id"]
    terms = query["terms"]

    #### Create an RTX Feedback management object
    #eprint(query)
    rtxFeedback = RTXFeedback()
    rtxFeedback.connect()
    cachedResponse = rtxFeedback.getCachedResponse(query)

    #### If we can find a cached response for this query and this version of RTX, then return the cached response
    if ( cachedResponse is not None ):
      apiResponse = Response().from_dict(cachedResponse)
      rtxFeedback.disconnect()
      self.limitResponse(apiResponse,query)
      self.logQuery(query,apiResponse)
      return apiResponse

    #### Still have special handling for Q0
    if id == 'Q0':
      # call out to QueryMeSH here to satify the query "What is XXXXXX?"
      meshQuery = QueryMeSH()
      response = meshQuery.queryTerm(terms["term"])
      if 'original_question' in query:
        response.original_question_text = query["original_question"]
        response.restated_question_text = query["restated_question"]
      response.known_query_type_id = query["known_query_type_id"]
      response.terms = query["terms"]
      id = response.id
      codeString = response.result_code
      self.logQuery(query,response)
      rtxFeedback.addNewResponse(response,query)
      rtxFeedback.disconnect()
      self.limitResponse(response,query)
      return(response)

    #### Call out to OrangeBoard to answer the other types of queries
    else:

      txltr = ParseQuestion()
      command = "python3 " + txltr.get_execution_string(id,terms)

      #### Set CWD to the QuestioningAnswering area and then invoke from the shell the Q1Solution code
      cwd = os.getcwd()
      os.chdir(os.path.dirname(os.path.abspath(__file__))+"/../../../reasoningtool/QuestionAnswering")
      eprint(command)
      returnedText = subprocess.run( [ command ], stdout=subprocess.PIPE, shell=True )
      os.chdir(cwd)

      #### reformat the stdout result of the shell command into a string
      reformattedText = returnedText.stdout.decode('utf-8')
      #eprint(reformattedText)

      #### Try to decode that string into a response object
      try:
          #data = ast.literal_eval(reformattedText)
          data = json.loads(reformattedText)
          response = Response.from_dict(data)

      #### If it fails, the just create a new Response object with a notice about the failure
      except:
          response = Response()
          response.result_code = "InternalError"
          response.message = "Error parsing the response from the reasoner. This is an internal bug that needs to be fixed. Unable to respond to this question at this time. The unparsable response was: " + reformattedText

      print(query)
      if 'original_question' in query:
        response.original_question_text = query["original_question"]
        response.restated_question_text = query["restated_question"]
      response.known_query_type_id = query["known_query_type_id"]
      response.terms = query["terms"]

      #### Log the result and return the Response object
      self.logQuery(query,response)
      rtxFeedback.addNewResponse(response,query)
      rtxFeedback.disconnect()

      #### Limit response
      self.limitResponse(response,query)
      return(response)


    #### If the query type id is not triggered above, then return an error
    response = Response()
    response.result_code = "UnsupportedQueryTypeID"
    response.message = "The specified query id '" + id + "' is not supported at this time"
    rtxFeedback.disconnect()
    return(response)


  def logQuery(self,query,response):
    datetimeString = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "known_query_type_id" not in query or query["known_query_type_id"] is None:
      id = "?"
    else:
      id = query['known_query_type_id']

    if "terms" not in query or query['terms'] is None:
      terms = "{}"
    else:
      terms = stringifyDict(query['terms'])

    if "restated_question" not in query or query["restated_question"] is None:
      restated_question = ""
    else:
      restated_question = query["restated_question"]

    response_code = response.result_code

    with open(os.path.dirname(os.path.abspath(__file__))+"/RTXQueries.log","a") as logfile:
      logfile.write(datetimeString+"\t"+response_code+"\t"+id+"\t"+terms+"\t"+restated_question+"\n")


  def limitResponse(self,response,query):
    if "max_results" in query and query["max_results"] is not None:
      if response.result_list is not None:
        if len(response.result_list) > query["max_results"]:
          del response.result_list[query["max_results"]:]
          response.message += " (output is limited to "+str(query["max_results"]) + " results)"


  def __init__(self):
     None

def stringifyDict(inputDict):
  outString = "{"
  for key,value in sorted(inputDict.items(), key=lambda t: t[0]):
    if outString != "{":
      outString += ","
    outString += "'"+str(key)+"':'"+str(value)+"'"
  outString += "}"
  return(outString)


def main():
  rtxq = RTXQuery()
  query = { "known_query_type_id": "Q0", "terms": { "term": "lovastatin" } }
  #query = { "knownQueryTypeId": "Q0", "terms": [ "foo" ] }
  #query = { "known_query_type_id": "Q1", "terms": [ "malaria" ] }
  #query = { "knownQueryTypeId": "Q2", "terms": [ "physostigmine", "glaucoma" ] }
  query = { "known_query_type_id": "Q2", "terms": {'chemical_substance': 'CHEMBL154', 'disease': 'DOID:8398'} }
  #query = { "knownQueryTypeId": "Q2", "terms": [ "physostigmine", "DOID:1686" ] }
  #query = { "knownQueryTypeId": "Q2", "terms": [ "DOID:1686", "physostigmine" ] }
  #query = { "knownQueryTypeId": "Q3", "terms": [ "acetaminophen" ] }
  response = rtxq.query(query)
  print(json.dumps(ast.literal_eval(repr(response)),sort_keys=True,indent=2))
  #print(response)


if __name__ == "__main__": main()
