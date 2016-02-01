## Simple Hello World (Micro) Service

This is based on the micro service examples in the 

[Microservices with Spring blog](https://spring.io/blog/2015/07/14/microservices-with-spring) on spring.io

 This example is broken it down into a more simple example, starting from the [Spring Boot Getting Started Guide](https://spring.io/guides/gs/spring-boot/) 

A simple Hello world service and Spring boot Application class using gradle, it is slightly elaborated to a a path that provides a simple json object. Then added an annotation to the service so it registered itself on the Eureka server.

The Eureka server is using the SpringBoot [Eureka Server Sample](https://github.com/spring-cloud-samples/eureka) running on the default port. Once running the server can be accessed on http://localhost:8761 with registered leases visible at http://localhost:8761/lastn.

Now to register the service, all is required is to add @EnableDiscoveryClient to the RestController and include the dependencies.

To allow for some configuration a YAML configuration file has been added to the application by adding
'System.setProperty("spring.config.name", "register-application");'
 
 and placing register-application.yml in the resources directory
 the configuration file includes:
 '''
 # Spring properties
spring:
  application:
    name: Hello-Application  # Identify this application



# HTTP Server
server:
  port: 4444   # HTTP (Jetty) port
'''
which registers the service as Hello-Application and specifies the HTTP server port to be 4444

The example can be run with 
./gradlew bootRun

After running you should be able to see the service running at
1. http://localhost:4444
1. http://localhost:4444/greeting
1. http://localhost:4444/greeting&name=Freddy

Next up is the lookup service to follow shortly





