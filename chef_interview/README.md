# Python 3.11 is used along with virtual environment

The code base uses conda, however, other environments can be deployed
Run ./setup_venv.sh to setup with conda

# Navigating package:
chef_interview
    |
    src/chef_interview
    tests
    config

The two challenges are within simulated_perception.py and simulated_controller.py

I have written part of the thought process as docstrings in the beginning of the code
Please feel free to email with additional questions
The ideas need more testing and guardrails but this is good for time frame

Time Spent:
- 3 hours on coding
- I'd have spent an additional 1.5 hour on brushing up concepts and looking things up online in articles and papers


Run:

python src/chef_interview/simulated_perception.py
python src/chef_interview/simulated_controller.py
pytest -v