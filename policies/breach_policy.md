# Breach Policy

This policy provides guidance for breach notification and response procedures at {{ company }}. 

{% if compliance_frameworks.hipaa %}
## Regulatory Context
This policy ensures compliance with:
* HIPAA/HITECH Breach Notification Rules
* Federal Trade Commission (FTC) requirements
* State-specific breach notification laws
* Industry-specific regulatory requirements

### Notification Requirements
Breach notification will be carried out in accordance with:
* HIPAA Security Rule requirements
* HITECH Act provisions
* State-specific timing requirements
* Industry-specific reporting obligations
{% endif %}

{% if compliance_frameworks.soc2 %}
## SOC2 Requirements
This policy supports:
* Security incident management
* Customer communication procedures
* Vendor notification requirements
* Evidence preservation standards
{% endif %}

## Breach Response Overview
{{ company }} implements a comprehensive breach response program that includes:
* Immediate incident containment
* Thorough investigation procedures
* Customer notification processes
* Regulatory reporting requirements

{% if data_storage_vendors %}
### Vendor Responsibilities
{% for vendor in data_storage_vendors %}
{% if vendor in baa_vendors %}
* {{ vendor }} has signed a Business Associate Agreement (BAA) and must comply with all breach notification requirements.
{% endif %}
{% endfor %}
{% endif %}

## Applicable Standards from the HITRUST Common Security Framework

* 11.a Reporting Information Security Events
* 11.c Responsibilities and Procedures

## Applicable Standards from the HIPAA Security Rule

* Security Incident Procedures - 164.308(a)(6)(i)
* HITECH Notification in the Case of Breach - 13402(a) and 13402(b)
* HITECH Timeliness of Notification - 13402(d)(1)
* HITECH Content of Notification - 13402(f)(1)

## {{ company }} Breach Policy

{% if compliance_frameworks.hipaa %}
## HIPAA Breach Requirements
All breaches of ePHI, regardless of platform or service type, must comply with HIPAA Breach Notification Rules and follow the procedures outlined below.
{% endif %}

{% if service_types.saas %}
## SaaS Platform Breach Procedures
* Automated breach detection systems monitor all SaaS platform activities
* Customer data isolation ensures breach scope can be accurately determined
* Immediate customer notification through dashboard and automated alerts
* Platform-wide security measures are automatically evaluated and updated
{% endif %}

{% if service_types.paas %}
## PaaS Environment Breach Procedures
* Container isolation helps prevent breach propagation between customers
* Infrastructure-level breaches are handled by {{ company }}'s security team
* Application-level breaches are reported to affected customers for handling
* Shared responsibility model clearly defines breach response ownership
{% endif %}

{% if service_types.medical_device %}
## Medical Device Breach Procedures
* Device-specific breach detection and reporting mechanisms
* Compliance with both HIPAA and FDA breach reporting requirements
* Emergency procedures for critical device security compromises
* Coordination with healthcare providers for patient safety measures
{% endif %}

{% if service_types.mobile_app %}
## Mobile Application Breach Procedures
* Mobile-specific breach detection and containment procedures
* Remote data wiping capabilities for compromised devices
* App store notification procedures when applicable
* User notification through in-app messaging and push notifications
{% endif %}

1. Discovery of Breach: A breach of ePHI shall be treated as "discovered" as of the first day on which such breach is known to the organization, or, by exercising reasonable diligence would have been known to {{ company }} Following the discovery of a potential breach, the organization shall begin an investigation (see organizational policies for security incident response and/or risk management incident response) immediately, conduct a risk assessment, and based on the results of the risk assessment, begin the process to notify each Customer affected by the breach. {{ company }} shall also begin the process of determining what external notifications are required or should be made (e.g., Secretary of Department of Health & Human Services (HHS), media outlets, law enforcement officials, etc.)
2. Breach Investigation: The {{ company }} Security Officer shall name an individual to act as the investigator of the breach (e.g., privacy officer, security officer, risk manager, etc.).  The investigator shall be responsible for the management of the breach investigation, completion of a risk assessment, and coordinating with others in the organization as appropriate (e.g., administration, security incident response team, human resources, risk management, public relations, legal counsel, etc.) The investigator shall be the key facilitator for all breach notification processes to the appropriate entities (e.g., HHS, media, law enforcement officials, etc.).  All documentation related to the breach investigation, including the risk assessment, shall be retained for a minimum of six years. A template breach log is located [here](breach.log.pdf).
3. Risk Assessment: For an acquisition, access, use or disclosure of ePHI to constitute a breach, it must constitute a violation of the HIPAA Privacy Rule. A use or disclosure of ePHI that is incident to an otherwise permissible use or disclosure and occurs despite reasonable safeguards and proper minimum necessary procedures would not be a violation of the Privacy Rule and would not qualify as a potential breach. To determine if an impermissible use or disclosure of ePHI constitutes a breach and requires further notification, the organization will need to perform a risk assessment to determine if there is significant risk of harm to the individual as a result of the impermissible use or disclosure. The organization shall document the risk assessment as part of the investigation in the incident report form noting the outcome of the risk assessment process. The organization has the burden of proof for demonstrating that all notifications to appropriate Customers or that the use or disclosure did not constitute a breach. Based on the outcome of the risk assessment, the organization will determine the need to move forward with breach notification. The risk assessment and the supporting documentation shall be fact specific and address:
	* Consideration of who impermissibly used or to whom the information was impermissibly disclosed;
	* The type and amount of ePHI involved;
	* The cause of the breach, and the entity responsible for the breach, either Customer, {{ company }}, or Partner.
	* The potential for significant risk of financial, reputational, or other harm. 
4. Timeliness of Notification: Upon discovery of a breach, notice shall be made to the affected {{ company }} Customers no later than 4 hours after the discovery of the breach. It is the responsibility of the organization to demonstrate that all notifications were made as required, including evidence demonstrating the necessity of delay. 
5. Delay of Notification Authorized for Law Enforcement Purposes:  If a law enforcement official states to the organization that a notification, notice, or posting would impede a criminal investigation or cause damage to national security, the organization shall:
	* If the statement is in writing and specifies the time for which a delay is required, delay such notification, notice, or posting of the timer period specified by the official; or
	* If the statement is made orally, document the statement, including the identify of the official making the statement, and delay the notification, notice, or posting temporarily and no longer than 30 days from the date of the oral statement, unless a written statement as described above is submitted during that time. 
6. Content of the Notice: The notice shall be written in plain language and must contain the following information:
	* A brief description of what happened, including the date of the breach and the date of the discovery of the breach, if known;
	* A description of the types of unsecured protected health information that were involved in the breach (such as whether full name, Social Security number, date of birth, home address, account number, diagnosis, disability code or other types of information were involved), if known;
	* Any steps the Customer should take to protect Customer data from potential harm resulting from the breach.
	* A brief description of what {{ company }} is doing to investigate the breach, to mitigate harm to individuals and Customers, and to protect against further breaches.
	* Contact procedures for individuals to ask questions or learn additional information, which may include a toll-free telephone number, an e-mail address, a web site, or postal address.
7. Methods of Notification: {{ company }} Customers will be notified via email and phone within the timeframe for reporting breaches, as outlined above.
8. Maintenance of Breach Information/Log: As described above and in addition to the reports created for each incident, {{ company }} shall maintain a process to record or log all breaches of unsecured ePHI regardless of the number of records and Customers affected. The following information should be collected/logged for each breach (see sample Breach Notification Log):
	* A description of what happened, including the date of the breach, the date of the discovery of the breach, and the number of records and Customers affected, if known.
	* A description of the types of unsecured protected health information that were involved in the breach (such as full name, Social Security number, date of birth, home address, account number, etc.), if known.
	* A description of the action taken with regard to notification of patients regarding the breach.
	* Resolution steps taken to mitigate the breach and prevent future occurrences.
10. Workforce Training: {{ company }} shall train all members of its workforce on the policies and procedures with respect to ePHI as necessary and appropriate for the members to carry out their job responsibilities. Workforce members shall also be trained as to how to identify and report breaches within the organization.
11. Complaints: {{ company }} must provide a process for individuals to make complaints concerning the organization’s patient privacy policies and procedures or its compliance with such policies and procedures.
12. Sanctions: The organization shall have in place and apply appropriate sanctions against members of its workforce, Customers, and Partners who fail to comply with privacy policies and procedures.
13. Retaliation/Waiver: {{ company }} may not intimidate, threaten, coerce, discriminate against, or take other retaliatory action against any individual for the exercise by the individual of any privacy right. The organization may not require individuals to waive their privacy rights under as a condition of the provision of treatment, payment, enrollment in a health plan, or eligibility for benefits.

## {{ company }} Customer Responsibilities

1. The {{ company }} Customer that accesses, maintains, retains, modifies, records, stores, destroys, or otherwise holds, uses, or discloses unsecured ePHI shall, without unreasonable delay and in no case later than 60 calendar days after discovery of a breach, notify {{ company }} of such breach. The Customer shall provide {{ company }} with the following information:
	* A description of what happened, including the date of the breach, the date of the discovery of the breach, and the number of records and Customers affected, if known.
	* A description of the types of unsecured protected health information that were involved in the breach (such as full name, Social Security number, date of birth, home address, account number, etc.), if known.
	* A description of the action taken with regard to notification of patients regarding the breach.
	* Resolution steps taken to mitigate the breach and prevent future occurrences.
4. Notice to Media: {{ company }} Customers are responsible for providing notice to prominent media outlets at the Customer's discretion.
5. Notice to Secretary of HHS: {{ company }} Customers are responsible for providing notice to the Secretary of HHS at the Customer's discretion.

## Sample Letter to Customers in Case of Breach

[Date]


[Name here]
[Address 1 Here]
[Address 2 Here]
[City, State Zip Code]

Dear [Name of Customer]:

I am writing to you from {{ company }}, Inc. with important information about a recent breach that affects your account with us. We became aware of this breach on [Insert Date] which occurred on or about [Insert Date]. The breach occurred as follows:

Describe event and include the following information:
A. A brief description of what happened, including the date of the breach and the date of the discovery of the breach, if known.
B. A description of the types of unsecured protected health information that were involved in the breach (such as whether full name, Social Security number, date of birth, home address, account number, diagnosis, disability code or other types of information were involved), if known.
C. Any steps the Customer should take to protect themselves from potential harm resulting from the breach.
D. A brief description of what {{ company }} is doing to investigate the breach, to mitigate harm to individuals, and to protect against further breaches.
E. Contact procedures for individuals to ask questions or learn additional information, which includes a toll-free telephone number, an e-mail address, web site, or postal address.

Other Optional Considerations:

* Recommendations to assist customer in remedying the breach.

We will assist you in remedying the situation.

Sincerely,


Geoff Oberhofer,
Co-founder - {{ company }}, Inc
geoff@{{ company }}app.com
253-905-4216
