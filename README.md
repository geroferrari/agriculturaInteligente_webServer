# Agricultura Inteligente - Trabajo Profesional Ingenieria electronica - UBA


The main idea of this web server is to be able to receive telemetry from different sensors, show that information in a pretty way and work with that information to send telecomands to an actuator.
To be able to decide when to send the information, it has a fuzzy logic algorithm that use the information of the sensors to define an output.
It is supposed to be used by the owner of the field to know in real time the status of his plants, and turn on/off the irrigation (can be done manually or automatic by the fuzzy logic algorithm).

Some of the characteristics of the web server:
- Users managment, including a log in page.
- Receive telecomands and print dashboards with statistics.
- Receive information from a weather api.
- Send telecomands to an actuator.
- Send email alerts to the owner of the field.


The project idea can be sum up in the next two diagrams:
![image](https://github.com/geroferrari/agriculturaInteligente_webServer/assets/38739978/042809d7-48b7-46ac-9f85-c2da8a7aa980)


![image](https://github.com/geroferrari/agriculturaInteligente_webServer/assets/38739978/947a5fd5-a96c-4dd2-8211-7a5cedd358ff)

DISCLAIMER: This is the public version of my end of career project. The complete project remains private for now. 

DISCLAIMER 2: This was my first python and django experience, and I do not like it. It has a lot of bugs and things that were not well defined and addressed. 
