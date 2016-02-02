package hello;

import java.util.Arrays;
import java.util.logging.Logger;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

@SpringBootApplication
public class RegisterApplication {

	 protected static Logger logger = Logger.getLogger(RegisterApplication.class.getName());

    public static void main(String[] args) {
    	System.setProperty("spring.config.name", "register-application");
        ApplicationContext ctx = SpringApplication.run(RegisterApplication.class, args);

        logger.info("Let's inspect the beans provided by Spring Boot:");

        String[] beanNames = ctx.getBeanDefinitionNames();
        Arrays.sort(beanNames);
        for (String beanName : beanNames) {
           logger.info(beanName);
        }
    }

}