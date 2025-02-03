
"""
Counter API Implementation
"""

from flask import Flask, jsonify
from . import status  # Notice the dot for relative import
from flask import Flask

app = Flask(__name__)

COUNTERS = {}

def counter_exists(name):
  """Check if counter exists"""
  return name in COUNTERS

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
  """Create a counter"""
  if counter_exists(name):
      return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
  COUNTERS[name] = 0
  return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
  """Delete a counter"""
  if not counter_exists(name):
      return jsonify({"error": f"Counter {name} not found"}), status.HTTP_404_NOT_FOUND
  del COUNTERS[name]
  return '', status.HTTP_204_NO_CONTENT

# ===========================
# Feature: Increment Counter (PUT/counter/<name>)
# Author: Ashley Arellano
# Date: 2025-02-03
# Description: Increments the value of a given counter, checks 
# and marks HTTP response as 405 (method not allowed) if 
# the counter does not exist. Otherwise, it marks HTTP response as 200 (OK).
# ===========================
@app.route('/counters/<name>', methods=['PUT'])
def increment_counter(name):
  #Checks if the counter to be incremented exists
  if not counter_exists(name):
    #Counter does not exist, HTTP response is 405
    return jsonify({"error": f"Counter {name} does not exist. Unable to increment."}), status.HTTP_405_METHOD_NOT_ALLOWED
  #Counter exists, increment counter and return 200 as HTTP response
  COUNTERS[name] += 1
  return jsonify({name: COUNTERS[name]}),status.HTTP_200_OK

