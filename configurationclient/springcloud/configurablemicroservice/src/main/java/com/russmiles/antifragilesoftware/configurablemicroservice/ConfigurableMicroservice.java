
package com.russmiles.antifragilesoftware.configurablemicroservice;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class ConfigurableMicroservice {

	@Value("${foo:World!}")
	private String value;

	@RequestMapping("/")
	public String inspectValue() {
		return "Hello, " + value;
	}

	public static void main(String[] args) {
		SpringApplication.run(ConfigurableMicroservice.class, args);
	}
}
