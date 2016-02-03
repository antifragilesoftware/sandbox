## Lookup service

based on the micro service examples in the 

[Microservices with Spring blog](https://spring.io/blog/2015/07/14/microservices-with-spring) on spring.io

 This example is broken it down into a more simple example, starting from the [Spring Boot Getting Started Guide](https://spring.io/guides/gs/spring-boot/) 
 
 This project is a spring boot application with a Controller and lookup service. The lookup service is located at a 
 logical URL http://HELLO-APPLICATION in the Application file, and as the Application has the annotation
  @EnableDiscoveryClient, thismeans the logical URL is looked on a Netflix Eureka server running locally on the default port.
  It is expecting to see a service located within hte registry as HELLO_APPLICATION
  
  This application is a simple Hello world service that can be seen (github URL)
  
  The service can be triggered by using the following urls
  
  http://locahost:5555/hello - which just returns a string from the local controller
  
  http://locahost:5555/localHello - which just returns a string from the localservice
  
   http://locahost:5555/lookup1 - which just returns a string the service looked up in the registry 
   and then returns result from the remote service
   
   http://locahost:5555/lookup2 - which returns a serialised json object from the 
   service looked up in the registry
    
   http://locahost:5555/lookup3 - returns a serialised json object from the 
    service looked up in the registry, but this can optionally pass a parameter for the name
   
   http://locahost:5555/lookup3?name=fred - returns a serialised json object from the 
    service looked up in the registry, but this can populates the parameter for the name, which gets reflected 
    in the returned json object
   
  The application can be run with
  
  ./gradlew bootRun