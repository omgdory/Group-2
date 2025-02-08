
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
@app.route('/new_counters/<name>', methods=['POST'])
def create_new_counter(name):
  # check if the counter already exists
  if counter_exists(name):
    # counter exists; can't create
    return jsonify({"error": f"Counter {name} already exists. Unable to create."}), status.HTTP_409_CONFLICT
  # counter DNE, so create it
  COUNTERS[name] = 0
  return jsonify({name: COUNTERS[name]}),status.HTTP_201_CREATED

# ===========================  
# Feature: Delete Counter (DELETE /counters/<name>)  
# Author: Franklin La Rosa Diaz  / Sameer Issa
# Date: 2025-02-02  
# Description: Implements the `delete_counter()` function to remove an existing counter.  
# Returns a 204 No Content status upon successful deletion.  
# Raises a 404 Not Found error if the counter does not exist.  
# ===========================  

@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
  """Delete a counter"""
  if not counter_exists(name):
      return jsonify({"error": f"Counter {name} not found"}), status.HTTP_404_NOT_FOUND
  del COUNTERS[name]
  return '', status.HTTP_204_NO_CONTENT


# ===========================
# Feature: Increment Counter (PUT/counter/<name>) / Check if non-existent
# Author: Ashley Arellano / Charles Ballesteros
# Date: 2025-02-03
# Description: Increments the value of a given counter, checks 
# and marks HTTP response as 404 (method not found) if
# the counter does not exist. Otherwise, it marks HTTP response as 200 (OK).
# ===========================
@app.route('/counters/<name>', methods=['PUT'])
def increment_counter(name):
  #Checks if the counter to be incremented exists
  if not counter_exists(name):
    #Counter does not exist, HTTP response is 405
    return jsonify({"error": f"Counter {name} does not exist. Unable to increment."}), status.HTTP_404_NOT_FOUND
  #Counter exists, increment counter and return 200 as HTTP response
  COUNTERS[name] += 1
  return jsonify({name: COUNTERS[name]}),status.HTTP_200_OK

# TODO 3: i will do this later 
# - i will do this later 
# ===========================
# Test: Retrieve an existing counter
# Author: [Abdulrahman Alharbi]
# Date: [02.03.2025]
# Description: i will do this later 
# ===========================
@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    """Retrieve an existing counter"""
    if name in COUNTERS:
        return jsonify({name: COUNTERS[name]}), 200
    return jsonify({"error": "Counter not found"}), 404

# ===========================
# Test: Return 404 for non-existent counter (GET /counters)
# Author: Aviendha Andrus
# Date: 2025-02-06
# Description: GET endpoint to retrieve a 404 error if counter does not exist
# this test is also covered by get_counter function above
# ===========================
@app.route('/counters/<name>', methods=['GET'])
def return_nonexistant(name):
    """Return 404 if not found"""
    if name not in COUNTERS:
        return jsonify({"error": f"Counter not found"}), status.HTTP_404_NOT_FOUND
    return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

# ===========================
# Feature: List all counters
# Author: Christopher Liscano
# Date: 2025-02-04
# Description: GET endpoint to retrieve all counter names and their current values
# ===========================
@app.route('/counters', methods=['GET'])
def list_counters():
    """List all counters"""
    return jsonify(COUNTERS), status.HTTP_200_OK

# ===========================
# Feature: Handle invalid HTTP methods     (Unsupported HTTP Methods)
# Author: Ethan Zambrano
# Date: 2025-02-07
# Description: Ensures that when a client tries to use a invalid HTTP method on a route, that 
#              the server responds when it's a 404, 405, or 500 (whenever applicable) error.
# ===========================
@app.errorhandler(405)
def method_not_allowed(error):
    """Handle unsupported HTTP methods"""
    return jsonify({"error": "Method Not Allowed"}), status.HTTP_405_METHOD_NOT_ALLOWED
