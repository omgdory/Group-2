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

# ===========================
# Feature: Create a new counter (POST /counters/<name>)
# Author: Dorian Akhavan
# Date: 2025-02-04
# Description: Attempts to create a counter
# ===========================
@app.route('/counters/<name>', methods=['POST'])
def create_new_counter(name):
  # check if the counter already exists
  if counter_exists(name):
    # counter exists; can't create
    return jsonify({"error": f"Counter {name} already exists. Unable to create."}), status.HTTP_409_CONFLICT
  # counter DNE, so create it
  COUNTERS[name] = 0
  return jsonify({name: COUNTERS[name]}),status.HTTP_201_CREATED