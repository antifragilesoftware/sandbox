package lookup;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * Created by gtarrant-fisher on 03/02/2016.
 */
@RestController
public class LookupController {

    @Autowired
    protected LookedUpService lookedUpService;

    public LookupController(LookedUpService lookedUpService) { this.lookedUpService = lookedUpService; }


    @RequestMapping("/hello")
    public String hello() {
        return "Greetings from Spring Booooooooot!";
    }

    @RequestMapping("/localHello")
    public String localHello() {
        return lookedUpService.hello();
    }

    @RequestMapping("/lookup1")
    public String lookup1() {
        return lookedUpService.lookupHello();
    }


    @RequestMapping("/lookup2")
    public String lookup2() {

        return lookedUpService.lookupGreeting();
    }

    @RequestMapping("/lookup3")
    public String look3(@RequestParam(value="name", defaultValue="World") String name) {

        return lookedUpService.lookupGreetingWithParam(name);
    }


}
