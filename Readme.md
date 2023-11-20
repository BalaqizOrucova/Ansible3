I have created two roles: one for web application, one for database:
 ![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/d149b367-3bd3-42a1-8bdd-aec1c88afedd)


In database roles task I have defined several tasks, installing mysql server and client, installing python3-mysqldb module, starting MYSQL service, creating new database for application, creating tables(this is what I optionally added in order to not connect to db and write manually), and creating new mysql user.
The credentials and sensitive information that would expose details about database are protected and not directly included.
 ![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/69b921c1-4dd4-4f4b-b3e3-7c8958f7354c)


This is credential.yml content which has been encrypted using ansible vault:
 ![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/4738c614-0409-4e18-90ec-f28841e12e4c)


This is the output of ansible playbook which runs database roles for installation and configuration of mysql(the last task is to ensure that if vault encryption and decryption works correctly):
![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/5595ec37-92fd-474c-a429-78da0c62ad49)


When we check we can see successful installation and configuration(mysql is installed, username and database have been created):
 ![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/ced69294-362f-4eea-90ff-3840557dc0ed)


And I have webapp role tasks, which includes starting webapp container with specified image.
I have added database credentials to config.py of web application(note that “mysql-db” is the name of database container that I have mentioned below), and in Dockerfile specified required libraries, tools installations, command executions etc. which will help to create docker image for webapp correctly:
![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/cdc911cb-9f20-488f-a963-8083224e8bc1)


After this step, we will create images and containers for db and webapp separately.
 ![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/06fbfe0a-dc2c-4892-9881-b4720b6ce135)


The above picture shows our mysql-db container creation(for database we don’t need custom image, we assign it by using “image: mysql:5.7”).
For webapp we first create docker image:
 ![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/411b7c40-16c8-403c-bc3e-ccd103a94809)


Then start container based on the created image:
 ![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/2ff179c1-bedb-4ecf-9727-5336b85300b9)


We can see that containers are up and running:
 ![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/0f918e1d-881a-477b-99ca-9d968647a1e1)


Now lets check if we can communicate with webapp-container, mysql-db and if they can communicate with each other. To check this I sent curl requests(POST and GET), and connected to mysql-db with webapp-container.(172.18.0.2 is the ip of webapp-container, 172.18.0.3 is the ip of mysql-db)
 ![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/7aaf24c5-dfa7-4d9d-ad08-c866f0b0ecf6)


GET requests work successfully.
 ![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/eafff5a4-cfa0-477d-acd7-571a4607aa44)


POST request is also successful. Then we check the database and ensure the communication between two containers:
![image](https://github.com/BalaqizOrucova/ansible3/assets/123575558/07e0b7b0-615d-4639-9856-385e57a35a0f)

<img width="960" alt="Screenshot 2023-11-20 121624" src="https://github.com/BalaqizOrucova/ansible3/assets/123575558/66f93e1f-1ecb-4379-ae44-ef41019579a5">
<img width="960" alt="Screenshot 2023-11-20 121715" src="https://github.com/BalaqizOrucova/ansible3/assets/123575558/a8fbf160-2b0a-4405-90ad-a5b8274c7ee0">
<img width="844" alt="Screenshot 2023-11-20 121725" src="https://github.com/BalaqizOrucova/ansible3/assets/123575558/a42814e5-2be7-411e-bb78-52cfd541883d">


 

