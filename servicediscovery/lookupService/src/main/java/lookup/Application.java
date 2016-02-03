package lookup;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;

import java.util.Arrays;
import java.util.logging.Logger;

/**
 * Created by gtarrant-fisher on 03/02/2016.
 */
@SpringBootApplication
@EnableDiscoveryClient
// Disable component scanner ...
@ComponentScan(useDefaultFilters = false)
public class Application {


    protected static Logger logger = Logger.getLogger(Application.class.getName());

    public static final String SERVICE_URL = "http://HELLO-APPLICATION";
    public static void main(String[] args) {
        System.setProperty("spring.config.name", "lookup-" +
                "application");
        ApplicationContext ctx = SpringApplication.run(Application.class, args);

        logger.info("Let's inspect the beans provided by Spring Boot:");

        String[] beanNames = ctx.getBeanDefinitionNames();
        Arrays.sort(beanNames);
        for (String beanName : beanNames) {
            //logger.info(beanName);
        }
    }

    @Bean
    public LookedUpService lookedUpService() {
        return new LookedUpService(SERVICE_URL);
    }

    @Bean
    public LookupController lookedUpController() { return new LookupController(lookedUpService());}
}
