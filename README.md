![eierkocher](https://s3-eu-west-1.amazonaws.com/mkl-images/shot_4.png)

## alexa-egg-alarm

![python version](https://img.shields.io/badge/python-3.6-blue.svg)

Alexa skill that will time your boiled eggs to perfection. 🐣

## Skill Store

Egg Alarm / Egg Timer / Eierkocher is available in Germany, UK, USA, Canada, Australia, and India.
- [View in German store](https://www.amazon.de/Max-Lamberti-Eierkocher/dp/B078PWZNNW)
- [View in English store](https://www.amazon.co.uk/Max-Lamberti-Egg-Timer/dp/B078PWZNNW)

#### Description

Do you have problems boiling your eggs? Are your egg whites too runny? Do you loose track of time and boil your eggs into unsavoury pebbles? Fret not! Whether you like your eggs hard, medium or soft boiled, this skill has got it all! Simply preboil a pot of water, place your eggs inside, and tell Egg Alarm how you like them. Egg Alarm will keep track of time and alert you with the crow of a rooster once your egg is done.

## Tech

- [Zappa](https://github.com/Miserlou/Zappa) - deploy serverless Python applications
- [Flask](https://github.com/pallets/flask) - micro framework for web applications
- [Flask-Ask](https://github.com/johnwheeler/flask-ask) - Alexa Skills Kit for Python
- [AWS Lambda](https://aws.amazon.com/lambda/) - serverless compute service
- [AWS RDS](https://aws.amazon.com/rds/) - relational database service
- [krakenex](https://github.com/veox/python3-krakenex) - API for Kraken exchange

## Setup and Deployment Instructions

#### Run app locally:
Use Python 3.6, install requirements.txt file, and set environment variables (example provided in [example.env](https://github.com/hexamax/alexa-egg-alarm/blob/master/example.env)).

```
source example.env
python -m skill.app
```

#### Deploy:

Use deploy script for an automated deploy with latest virtual environment, configs and speech assets.

```sh deploy.sh {all, dev, production_eu, production_us, production_au}```
