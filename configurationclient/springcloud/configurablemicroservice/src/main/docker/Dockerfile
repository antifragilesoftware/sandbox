FROM java:8
ADD configurablemicroservice-0.0.1-SNAPSHOT.jar microservice.jar
VOLUME /tmp
VOLUME /target
RUN bash -c 'touch /microservice.jar'
EXPOSE 8888
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/microservice.jar"]