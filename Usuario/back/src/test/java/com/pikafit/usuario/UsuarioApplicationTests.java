package com.pikafit.usuario;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest(properties = {
		"spring.mongodb.uri=mongodb://localhost:27017/test",
		"app.cors.allowed-origins=http://localhost:3000"
})
class UsuarioApplicationTests {

	@Test
	void contextLoads() {
	}
}