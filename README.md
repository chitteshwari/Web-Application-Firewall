# Web-Application-Firewall
Web Application Firewall (Intrusion Detection System) built for a live open source vulnerability website (demo.testfire.net). The data is collected from Acunetix scans (web crawling and high SQL injection vulnerability scans) of the target website. BurpSuite is used as a proxy for these scans. The logs from BurpSuite are cleaned and used as the custom training dataset for the ML model.

Machine Learning (K means clustering) is used to classify whether a live HTTP request made to the website is legitimate or a malicious SQL Injection. 

📤📤Demo of the project:
When the query “hello” is typed, a legitimate request is detected
![image](https://github.com/chitteshwari/Web-Application-Firewall/assets/80682927/5cd923e3-7693-433e-904a-15b15d9adabf)

When the query “1234” is typed, a legitimate request is detected
![image](https://github.com/chitteshwari/Web-Application-Firewall/assets/80682927/8fdac886-32a5-4710-88ee-66b2c99ad616)

When the query “' UNION SELECT sum(columnname ) from tablename –" is typed, SQL injection attack is detected
![image](https://github.com/chitteshwari/Web-Application-Firewall/assets/80682927/6da8f171-9c14-4095-a670-ded8423c19e9)
