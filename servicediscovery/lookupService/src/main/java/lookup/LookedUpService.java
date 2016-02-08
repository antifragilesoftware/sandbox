package lookup;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import javax.annotation.PostConstruct;
import java.net.URI;
import java.util.logging.Logger;

/**
 * Created by gtarrant-fisher on 03/02/2016.
 */
@Service
public class LookedUpService {

    @Autowired
    protected RestTemplate restTemplate;

    protected String serviceUrl;

    protected Logger logger = Logger.getLogger(LookedUpService.class
            .getName());

    public LookedUpService(String serviceUrl) {
        this.serviceUrl = serviceUrl.startsWith("http") ? serviceUrl
                : "http://" + serviceUrl;
    }

    /**
     * The RestTemplate works because it uses a custom request-factory that uses
     * Ribbon to look-up the service to use. This method simply exists to show
     * this.
     */
    @PostConstruct
    public void demoOnly() {
        // Can't do this in the constructor because the RestTemplate injection
        // happens afterwards.
        logger.warning("The RestTemplate request factory is "
                + restTemplate.getRequestFactory());
    }

    public String hello() {

        return "Hello from service";
    }

    public String lookupGreeting() {

        logger.info("lookupGreeting called");


        //return restTemplate.getForObject(serviceUrl + "/hello", String.class);
        return restTemplate.getForObject(serviceUrl + "/greeting", String.class);
        //return restTemplate.getForObject(serviceUrl + String.format("/greeting?name={%s}",name), String.class);
    }

    public String lookupHello() {

        return restTemplate.getForObject(serviceUrl + "/", String.class);
    }

    public String lookupGreetingWithParam(String name)
    {

        logger.info("lookupGreetingWithParam called with:" + name);

        URI targetUrl = UriComponentsBuilder.fromUriString(serviceUrl)
                .path("/greeting")
                .queryParam("name", name)
                .build()
                .toUri();

        logger.info("uri is :" + targetUrl.toString());

        //String str = String.format("/greeting?name={%s}",name);
        //return restTemplate.getForObject(serviceUrl + str, String.class);
        return restTemplate.getForObject(targetUrl, String.class);
    }



}
