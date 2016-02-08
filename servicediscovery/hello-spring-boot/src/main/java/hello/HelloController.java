package hello;

import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;

import java.util.concurrent.atomic.AtomicLong;

@EnableDiscoveryClient
@RestController
public class HelloController {

    private static final String template = "Hello, %s!";
    private final AtomicLong counter = new AtomicLong();

    @RequestMapping("/")
    public String index() {
        return "Greetings from Spring Boooooooooot!";
    }


    @RequestMapping("/greeting")
    public Greeting greeting(@RequestParam(value="name", defaultValue="World") String name) {
        return new Greeting(counter.incrementAndGet(),
                String.format(template, name));
    }

}