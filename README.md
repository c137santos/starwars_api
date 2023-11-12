# API: Astromech's Protocol Interstellar

API desenvolvida para consultar os planetas e filmes de Star Wars.

<div align="center">
    <img width="50%" title="ByBing" src="sw.jpeg" align="center"/>
</div>


Nas galáxias distantes, um novo capítulo da tecnologia se desdobra. Uma fusão entre realidade e ficção, a 'API: Astromech's Protocol Interstellar'. Prepare-se para uma jornada intergaláctica que ultrapassa os limites do espaço e do tempo.

Neste universo, os droids Astromech, como o destemido R2-D2 e o leal R5-D4, reinam supremos. Dotados de habilidades técnicas incomparáveis, esses droids desempenham um papel vital nas naves estelares, desde a manutenção até a navegação intragaláctica. 

Com o 'Protocol Interstellar' suas capacidades são amplificadas, aprimorando o desempenho da tecnologia e proporcionar aos usuários uma experiência imersiva que os transporta para os confins mais distantes da galáxia.

Os Astromech podem dados sobre planetas distantes e filmes que documentam as grandes batalhas, como se você estivesse lá! explorando o universo Star Wars por conta própria!

Preparem-se, entusiastas da tecnologia e aventureiros intergalácticos, para uma experiência que transcende os limites da imaginação. Com a 'API: Astromech's Protocol Interstellar', o universo de Star Wars está ao seu alcance como nunca antes!


# Setup A.P.I

Este projeto utiliza tecnologias listadas no arquivo `requirements.txt` para produção e `requirements.tests.txt` para desenvolvimento e testes.

### Tecnologias Principais

- **Flask==3.0.0**: Framework web utilizado para desenvolvimento.
- **uWSGI==2.0.23**: Servidor web que atua como interface entre o Flask e o servidor HTTP.
- **pytest==7.4.3**: Framework de testes utilizado para garantir a qualidade do código.
- **pydantic==1.10.13**: Biblioteca para validação de dados com suporte a tipos.
- **pymongo==4.6.0**: Driver oficial do MongoDB para Python.

### Ferramentas de Desenvolvimento

- **black==23.11.0**: Formata código Python.
- **coverage==7.3.2**: Mede de cobertura de código.
- **pytest-cov==4.1.0**: Extensão do Pytest para integração com o Coverage.

### Bibliotecas Adicionais

- **flask-pydantic-spec==0.5.0**: Gerar especificações de API para aplicativos Flask usando Pydantic.


## Executando o Projeto com Docker

O projeto está dockerizado, facilitando a configuração do ambiente. Para iniciar, basta executar o seguinte comando:

```bash
docker compose up -d
```

## Executando os testes

Executando os testes por dentro do docker:

```bash
docker compose run --rm test_flask_app pytest
```

Para verificar a cobertura do projeto:

```bash
docker compose run --rm test_flask_app pytest --cov
```

Para verificar a cobertura do projeto em HTML:


```bash
docker compose run --rm test_flask_app pytest --cov --cov-report=html:tests/html_dir
```

### Documentação OpenAPI

A documentação, gerada pelo flask-pydantic-spec, pode ser acessada através do endpoint /swagger:

http://localhost/apidoc/swagger


