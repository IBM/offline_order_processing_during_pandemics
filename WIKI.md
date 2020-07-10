# Short title

Order processng during pandemics for offline mode

# Long title

Use Watson Knowledge Studio and Speech To Text to automate offline order processing during pandemics

# Author

> Provide names and IBM email addresses.

* Rahul Reddy Ravipally <raravi86@in.ibm.com>
* Sharath Kumar R K  <sharrkum@in.ibm.comm>
* Manoj Jahgirdar  <manoj.jahgirdar@in.ibm.com>
* Srikanth Manne  <srikanth.manne@in.ibm.com>
* Msnjula G. Hosurmath  <mhosurma@in.ibm.com>

# URLs

### Github repo

* [Order processng during pandemics for offline mode](https://github.com/IBM/offline_order_processing_during_pandemics)

### Other URLs

* Video Demo link: https://youtu.be/n5rrJ0FMGQk

# Summary

In this code pattern, we build an AI-powered backend system that can take the daily essentials orders through offline mode. The system processes the audio request by converting it to formatted orders list. A smart way of processing the information quickly.

# Technologies

* [Python](https://developer.ibm.com/technologies/python/): An open-source interpreted high-level programming language for general-purpose programming.

* [Data science](https://developer.ibm.com/technologies/data-science/): Analyze structured and unstructured data to extract knowledge and insights.

* [Web development](https://developer.ibm.com/technologies/web-development/): Use open-standards technologies to build modern web apps.

# Description

How do we stop panic amongst people of hoarding essentials during lockdown? How do we maintain social distancing while procuring essentials?

Majority of Indian population (specially elderly population) do not have knowledge about digital services. Hence, they will not be able to use the available online portals to order daily essentials & medicines.

A toll free number (ex :- dial *222) based approach to contact control tower will be a better option. Here the user will be able to call toll free number and order the essentials. This will address the limitation mentioned above and will have wider reach with the population to make use of the facility. However,with majority of them using this toll free number based approach the traffic at the backend will be very high. To process of these calls manually will be tedious.

In this code pattern, we build an AI-powered backend system that can take the daily essentials orders through offline mode. The system processes the audio request by converting it to formatted orders list. A smart way of processing the information quickly.

This AI powered backend system can be later connected to the inventory database for optimising supply chain management aswell. This solution will be applicable into various domains such as ordering medicines and ordering daily essentials(groceries), etc.

# Flow

1. Feed the audio to Speech to Text service.
2. Convert the text into english using Watson Language Translator.
3. Feed the English text to Watson Knowledge Studio model which is deployed on Watson Natural Language Understanding.
4. The model deployed on Watson Natural Language Understanding will identify all the required attributes from the text.
5. Visualize the order and customer details from the recordings on a dashboard.

# Instructions

> Find the detailed steps for this pattern in the [readme file](https://github.com/IBM/offline_order_processing_during_pandemics/blob/master/README.md). The steps will show you how to:

1. Clone the repo
2. Setup Watson Speech to Text
3. Setup Watson Language Translator
4. Setup Watson Knowledge Studio and Natural Language Understanding
5. Setup IBM Db2
6. Add the Credentials to the Application
7. Deploy the Application to Cloud Foundry
8. Analyze the results

# Components and services

* [Watson Speech to Text service](https://cloud.ibm.com/catalog/services/speech-to-text)
* [Watson Language Translator](https://cloud.ibm.com/catalog/services/language-translator)
* [Watson Natural Language Understanding](https://cloud.ibm.com/catalog/services/natural-language-understanding)
* [Watson Knowledge Studio](https://cloud.ibm.com/catalog/services/knowledge-studio)
* [Cloud Object Storage](https://cloud.ibm.com/catalog/services/cloud-object-storage)
* [IBM DB2](https://cloud.ibm.com/catalog/services/db2)

# Runtimes

* Python 3
* JavaScript

# Related IBM Developer content

> List any IBM Developer resources that are closely related to this pattern, such as other patterns, blog posts, tutorials, etc..

* [How to enhance social distancing to combat the pandemic](url): <<**Content under progress**>>
* [Online order processing system during pandemic](url): <<**Content under progress**>>
* [Create an AI powered dashboard for realtime predictions & recommendations](url): <<**Content under progress**>>

