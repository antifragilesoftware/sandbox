package lookup;

import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockServletContext;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;
import org.springframework.test.context.web.WebAppConfiguration;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.hamcrest.Matchers.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * Created by gtarrant-fisher on 03/02/2016.
 */
@RunWith(SpringJUnit4ClassRunner.class)
@SpringApplicationConfiguration(classes = MockServletContext.class)
@WebAppConfiguration
public class LookupControllerTest {

    private MockMvc mvc;
    public static final String SERVICE_URL = "http://HELLO-APPLICATION";

    @Before
    public void setUp() throws Exception {

        LookedUpService lookedUpService = new LookedUpService(SERVICE_URL);

        mvc = MockMvcBuilders.standaloneSetup(new LookupController(lookedUpService)).build();
        //mvc = MockMvcBuilders.standaloneSetup(new HelloController()).build();


    }

    @Test
    public void getHello() throws Exception {
        mvc.perform(MockMvcRequestBuilders.get("/hello").accept(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(content().string(equalTo("Greetings from Spring Booooooooot!")));
    }


//    @Test
//    public void getlookup1() throws Exception {
//        mvc.perform(MockMvcRequestBuilders.get("/lookup1").accept(MediaType.APPLICATION_JSON))
//                .andExpect(status().isOk())
//                .andExpect(content().string(equalTo("Greetings from Spring Boooooooooot")));
//    }







}
