# Web-Application-Firewall

## ℹ️ℹ️ About the project:

Web Application Firewall (Intrusion Detection System) built for a live open source vulnerability website (demo.testfire.net). The data is collected from Acunetix scans (web crawling and high SQL injection vulnerability scans) of the target website. BurpSuite is used as a proxy for these scans. The logs from BurpSuite are cleaned and used as the custom training dataset for the ML model.

Machine Learning (K means clustering) is used to classify whether a live HTTP request made to the website is legitimate or a malicious SQL Injection. 


## 📤📤Demo of the project:
When the query “hello” is typed, a legitimate request is detected

![image](https://github.com/chitteshwari/Web-Application-Firewall/assets/80682927/2b60497e-f99f-4060-bdf8-d93eb81a5c82)

When the query “1234” is typed, a legitimate request is detected

![image](https://github.com/chitteshwari/Web-Application-Firewall/assets/80682927/aa645e03-c3f6-43ea-9f56-1998f212db6b)

When the query “' UNION SELECT sum(columnname ) from tablename –" is typed, SQL injection attack is detected
![image](https://github.com/chitteshwari/Web-Application-Firewall/assets/80682927/6da8f171-9c14-4095-a670-ded8423c19e9)
