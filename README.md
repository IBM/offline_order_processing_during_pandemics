# AI powered Backend system for order processing during pandemics

How do we stop panic amongst people of hoarding essentials during lockdown? How do we maintain social distancing while procuring essentials?

Majority of Indian population (specially elderly population) do not have knowledge about digital services. Hence, they will not be able to use the available online portals to order daily essentials & medicines.

A toll free number (ex :- dial *222) based approach to contact control tower will be a better option. Here the user will be able to call toll free number and order the essentials. This will address the limitation mentioned above and will have wider reach with the population to make use of the facility. However,with majority of them using this toll free number based approach the traffic at the backend will be very high. To process of these calls manually will be tedious.

In this code pattern, we propose an AI-powered backend system that can take the daily essentials orders through offline mode. The system processes the audio request by converting it to formatted orders list. A smart way of processing the information quickly.

This AI powered backend system can be later connected to the inventory database for optimising supply chain management aswell. This solution will be applicable into various domains such as ordering medicines and ordering daily essentials(groceries), etc.

When the reader has completed this Code Pattern, they will understand how to:

* Use Speech to Text service.
* Use Watson Language Translator.
* Use and train model on Watson Knowledge Studio.
* Deploy model on Watson Natural Language Understanding.

<!--add an image in this path-->
![](doc/source/images/Architecture.png)

<!--Optionally, add flow steps based on the architecture diagram-->
## Flow

1. Feed the audio to Speech to Text service.
2. Convert the text into english using Watson Language Translator.
3. Feed the English text to Watson Knowledge Studio model which is deployed on Watson Natural Language Understanding.
4. The model deployed on Watson Natural Language Understanding will identify all the required attributes from the text.
5. Visualize the order and customer details from the recordings on a dashboard.

<!--Optionally, update this section when the video is created-->
# Watch the Video

<!--[![](http://img.youtube.com/vi/aA8wTWbmqSU/0.jpg)](https://youtu.be/aA8wTWbmqSU)]-->

## Pre-requisites

* [IBM Cloud account](https://www.ibm.com/cloud/): Create an IBM Cloud account.

# Steps

Please follow the below to setup and run this code pattern.

1. [Clone the repo](#1-clone-the-repo)
2. [Setup Watson Speech to Text ](#2-setup-watson-speech-to-text)
3. [Setup Watson Language Translator](#3-setup-watson-language-translator)
4. [Setup Watson Knowledge Studio](#4-setup-watson-knowledge-studio)
5. [Setup Watson Natural Language Understanding](#5-setup-watson-natural-language-understanding)
6. [Setup IBM Db2](#6-setup-ibm-db2)
7. [Add the Credentials to the Application](#7-add-the-credentials-to-the-application)
8. [Deploy the Application to Cloud Foundry](#8-deploy-the-application-to-cloud-foundry)
9. [Analyze the results](#9-analyze-the-results)

### 1. Clone the repo

Clone the `repo-name` repo locally. In a terminal, run:

```bash
$ git clone https://github.com/IBM/repo-name
```

### 7. Add the Credentials to the Application

- Open the `credentials1.json` file from the root directory and paste the Db2 Credentials and save the file.

- Open `app.py` from the root directory, goto line number `27` and insert the natural language understanding API Key `apikey`, goto line number `28` and insert the natural language understanding URL `nlu_url` and lastly goto line number `29` and insert the knowledge studio model ID `wks_model_id`. 

<pre><code># Initialize WKS Model Credentials

apikey = <b>'YOUR-API-KEY-HERE'</b>
nlu_url = <b>'YOUR-URL-HERE'</b>
wks_model_id = <b>'YOUR-WKS-MODEL-ID-HERE'</b>

</code></pre>

### 8. Deploy the Application to Cloud Foundry

* Make sure you have installed [IBM Cloud CLI](https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started&locale=en-US) before you proceed.

* Log in to your IBM Cloud account, and select an API endpoint.
```bash
$ ibmcloud login
```

>NOTE: If you have a federated user ID, instead use the following command to log in with your single sign-on ID.
```bash
$ ibmcloud login --sso
```

* Target a Cloud Foundry org and space:
```bash
$ ibmcloud target --cf
```

* From within the _cloned directory_ push your app to IBM Cloud.
```bash
$ ibmcloud cf push
```

* Once Deployed You will see output on your terminal as shown, verify the state is _`running`_:

<pre><code>Invoking 'cf push'...

Pushing from manifest to org manoj.jahgirdar@in.ibm.com / space dev as manoj.jahgirdar@in.ibm.com...

...

Waiting for app to start...

name:              order-processing-pandemic
requested state:   started
routes:            <b> order-processing-pandemic.xx-xx.mybluemix.net </b>
last uploaded:     Sat 16 May 18:05:16 IST 2020
stack:             cflinuxfs3
buildpacks:        python

type:            web
instances:       1/1
memory usage:    256M
start command:   python app.py
     state     since                  cpu     memory           disk           details
#0   <b>running</b>   2020-05-16T12:36:15Z   25.6%   116.5M of 256M   796.2M of 1
</code></pre>

* Once the app is deployed you can visit the `routes` to view the application.

