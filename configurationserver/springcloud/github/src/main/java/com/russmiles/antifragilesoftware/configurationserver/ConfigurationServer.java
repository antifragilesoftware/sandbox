package com.russmiles.antifragilesoftware.configurationserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
//import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.config.server.EnableConfigServer;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableAutoConfiguration
@EnableConfigServer
public class ConfigurationServer {

	public static void main(String[] args) {
		SpringApplication.run(ConfigurationServer.class, args);
	}
}