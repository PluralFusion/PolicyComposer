# Mobile Application Security Policy

{% if service_types.mobile_app.enabled %}
{% if compliance_frameworks.hipaa %}
## HIPAA Compliance Context
This policy defines safeguards for mobile applications that collect, process, or store ePHI, addressing HIPAA technical and administrative requirements.
{% endif %}

{% if compliance_frameworks.soc2 %}
## SOC2 Compliance Context
This policy supports SOC2 Security and Confidentiality criteria for mobile app data protection and availability.
{% endif %}

This policy defines security requirements and procedures for {{ company }}'s mobile applications that handle ePHI.

## Applicable Standards
* HIPAA Security Rule
* FDA Mobile Medical Applications Guidance
* NIST Mobile Device Security Guidelines

## Mobile Application Security Controls

### Data Storage and Transmission
* All ePHI must be encrypted at rest using AES-256
* All network communication must use TLS 1.3 or higher
* No ePHI may be stored in device backups
* Automatic data purging after configurable timeout periods

### Authentication and Authorization
* Biometric authentication support required
* Minimum 6-character PIN as fallback
* Automatic session timeout after 5 minutes of inactivity
* Multi-factor authentication for sensitive operations

### Device Security Requirements
* Minimum iOS 14.0 or Android 10.0
* Device must have screen lock enabled
* No jailbroken or rooted devices allowed
* Security policy enforcement through MDM when applicable

### Incident Response
* Ability to remotely wipe application data
* Automated security incident reporting
* User notification mechanisms
* Integration with enterprise security monitoring

### Compliance Monitoring
* Regular security assessments
* Automated vulnerability scanning
* Third-party penetration testing
* Compliance documentation maintenance

{% endif %}