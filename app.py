from flask import Flask, redirect, url_for, request, render_template
import requests
import json

app = Flask(__name__, template_folder='./')
context_set = ""

response = [] # A list that will store the conversation

# Your solution here

def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5006)