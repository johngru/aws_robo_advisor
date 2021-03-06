# RoboAdvisor : Using Amazon Lex with Lambda Integration on AWS
  > Uses an Amazon Lex chatbot engine with a customized Lambda function initialization, validation, and fullfilment.

![chatbot](chatbot_cover.jpg)

Framework for building a robo advisor that recommends an investment portfolio composition based on age, investment size, and risk tolerance.

## Overview 

Many user centered applications require an easy, conversational method for obtaining data and metrics from users in order to successfully complete a given task with the provided information.  Amazon Lex, an application provided with AWS, is a streamlined method for accomplishing this goal, while also providing the convenience of cloud deployment.  

This project laid the foundation for an investment chatbot that makes recommendations for a portfolio given a user's age, investment amount, and risk tolerance.  

The first task of this framework, is to set up the dialog using Amazon Lex V1 Console.  

The next part is to customize a Lambda function that will validate the data, catch errors in user input, and output a response to the user with the portfolio recommendations.

---
## Technologies

This project is performed on Amazon Web Services, specifically Amazon Lex and Lambda.  The Lambda function is written in ```Python 3.7.xx```.

---

## Installation Guide

No installation is necessary on your local disk.  Although for constructing the Lambda function in Python, it is recommended to view and edit the code in your favorite local code editor ([VSCode](https://code.visualstudio.com/), for example).  An AWS account is required (free tier).  For more information, please visit:
[https://aws.amazon.com/](https://aws.amazon.com/)  

---

## Usage

The RoboAdvisor is initialized through Amazon Lex.  It is provided with some sample utterances and the data slots are determined:
* firstName
* age
* investmentAmount
* riskLevel

Before the Lambda function is created or initialized, this shell chat bot is built and a sample dialogue is created to look something like the video below:

![Amazon Lex - Initial Convo](Video_Demos/initial_dialogue.gif)

After the bot's framework and slots are initialized, the Lambda function is written to validate and fullfill the user's request for a portfolio recommendation.  The Lambda function should give and handle all test events found in the json responses in the [Test_Events directory](Test_Events).

An example of how the RoboAdvisor handles error inputs by the user is demonstrated in the video dialogue below:

![Amazon Lex - Error Conversation](Video_Demos/error_tests_with_lambda_integration.gif)


A successful user exchange dialogue with the RoboAdvisor looks like something below:

![Amazon Lex - Successful Conversation](Video_Demos/lambda_integration.gif)


## Data Sources

The seed code for this RoboAdvisor is provided by the course materials from a UCBerkeley Fintech Extension program.  

---

## Contributors

The seed code is from the course material from a UCBerkeley Extension program.  This chatbot is written and demonstrated by John Gruenewald.<br><br>
For more information, contact **John Gruenewald**:<br>
**e-mail:** [john.h.gruenewald@gmail.com](mailto:john.h.gruenewald@gmail.com)<br> **linked-in:**  [jhgruenewald](https://www.linkedin.com/in/jhgruenewald/)<br>**twitter:**  [@GruenewaldJohn](https://twitter.com/GruenewaldJohn)<br>**medium:**  [@comput99](https://medium.com/@comput99)

---

## License

MIT License

Copyright (c) 2022 John Gruenewald