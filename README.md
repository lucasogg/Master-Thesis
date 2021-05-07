University of Lausanne, CH, 2020

### The “Internet of Things” and the GDPR Transparency Obligation: A Case Study
 
## I - Intro

It is difficult to determine the exact origin of the concept of connected objects, but it could go back to the genesis of modern telecommunications in the 19th century with the invention of the telegraph line linking two distant machines. The advent of computer science and its own communication protocols, and more particularly the TCP/IP protocol, caused the concept to enter a new era. It was now possible for common objects to benefit from the computing power offered by a computer and its ability to communicate in a network, opening new perspectives for the widespread deployment of information systems and automated data collection.

Since then, these objects have multiplied, embracing major developments in information technology such as the transition from the personal computer to cloud computing, the generalization of "machine-to-machine" (M2M) relationships, the democratization of Internet-connected telephones, or the development of machine learning and big data. This permanent connection of reality to information systems through everyday objects raises many challenges in terms of privacy protection, data security and data processing. Is it still possible to control on these data sets about us? Are their confidentiality and integrity ensured during their collection and transmission? Are we correctly informed about their collection and potential uses?

*It is in this context that this work, delimited by the key European regulatory principles in data protection and supported by forensic analysis principles for the case study, will focus on assessing the concrete relationship between the transparency standards stemming from the GDPR and the provision of products and services in the context of the "Internet of Things".*

## II - Case study

- why ?

The main motivation of this case study is to shed practical light on the relation between the furniture of devices/services in the context of the IoT and the GDPR transparency regulatory framework, through the acquisition, configuration and regular use of three "home assistant" solutions. The final objective is to evaluate the GDPR transparency level of compliance demonstrated by the suppliers of the solutions studied :


Supplier | Name | Model | OS | MobileApp
:--- | :--- | :--- | :--- | :--- 
Amazon | Fire TV Stick | 3rd generation | Fire OS (v. 7.0) | Amazon Fire TV
Philips/Signify | Hue Lighting | 2.1 | proprietary firmware (v. 1941056000) | Philips Hue 
Samsung | Family Hub | RB7500 | Tizen OS (v. 4.0) | Family Hub

<p align="center">
<img src="https://github.com/lucasogg/Master-Thesis/blob/main/report/network_diagram_s.PNG?raw=true" width="600">
</p>

- how ?

0. GDPR analysis : relevant definitions, principles, standards, and their interactions

1. Hardware, software : description & preliminary analysis
 
2. Documentation analysis : general & privacy notice
 
3. Network set up : devices, mobile app's, interfaces (OpenWRT, ElasticSearch)

4. Network data collection : logged activities, network traffic captured
 
5. Cloud data collection : GDPR 15 "right of access" exercise, assessing its practical conditions, the completeness of the information received and its accessibility
 
6. Traces extraction, exploitation and prezentation (Python scripts)
 
7. Comparative analysis of traces : between the log of generating activities, the network traces (IP/DNS request/TLS Client Hello), and cloud traces (GDPR "right of access" data obtained from the various providers)
 
8. Compliance with GDPR transparency standards assessment : the objective of this final analysis was to assess whether the informations gathered from the documentation and the "right of access" exercise describe correctly the behaviour of the devices/services identified at the network level

## III - Findings

- overall assessment 

Supplier | Documentation provided | Exercising the right of access | Content of the received files | Additional information
:---     | :---                   | :---                           | :---                          | :---                  
Amazon | very complete & detailed | *via* a web app, took 5 days | the most complete, accurately reflecting usage of the device and resulting data | multiple requests for few answers 
Philips/Signify | most concise & clear documentation | *via* an online form, took more than GDPR 30-days delay without further justification | not received in time for assessment (but mainly technical logs) | not requested
Samsung | complete & detailed | *via* a web app, took 6 days | basic, mostly profile registering information | a 2nd request provided a bit more information, still evasive & unclear

<p align="center">
<img src="https://github.com/lucasogg/Master-Thesis/blob/main/report/assessment_table.PNG?raw=true" width="650">
</p>

Element | Description 
:--- | :--- 
Documentation provided | clarity, completeness, and level of detail of the information provided to data subjects in the phase of obtaining their consent or concluding the contract
Exercising the right of access | accessibility and effectivness of the request procedure
Content of the received files | completness and accessibility of the files provided
Additional information | assessment of the procedure when additional informations were requested (example : about appropriate safeguards within the framework of personal data transfers to third countries)
Overall assessment | global & final assessment
