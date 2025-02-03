from flask import Flask, jsonify
from . import status  # Notice the dot for relative import
"""
Counter API Implementation
"""
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
  if not counter_exists(name):
    return jsonify({"error": f"Counter {name} does not exist. Unable to increment."}), status.HTTP_405_METHOD_NOT_ALLOWED
  COUNTERS[name] += 1
  return jsonify({name: COUNTERS[name]}),status.HTTP_200_OK


