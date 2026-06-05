# Ticket Assignment

## Installation

### Step 1: Clone Repository

git clone <repository-url>

### Step 2: Enter Project Folder

cd ticket-assignment

### Step 3: Install Dependencies

uv sync

### Step 4: Start Ollama

ollama run llama3.2

### Step 5: Run Program

uv run main.py

## Features

* Reads customer messages from a text file
* Uses an LLM to classify tickets
* Validates output using Pydantic
* Automatically retries invalid responses
* Saves results to tickets.json
* Streams summaries using Ollama
* Reports token usage and estimated cost

## Output

Creates a tickets.json file containing structured ticket records.
