# Search-Engine-Project

## Teammates

[@Alexlam0258](https://github.com/Alexlam0258)
[@cpawongaa](https://github.com/cpawongaa)

# URL and Libraries Used

|           | **Frontend**                 | **Python Backend**                             | **Java Backend**                   |
|-----------|------------------------------|------------------------------------------------|------------------------------------|
| URL       | https://search.johnnyip.com/ | https://search-back1.johnnyip.com/             | https://search-back2.johnnyip.com/ |
| Libraries | React.js                     | Flask                                          | Spring Boot                        |
|           | Mantine (UI)                 | pymongo                                        | htmlparser                         |
|           | Axios                        | sqlite3                                        | gson                               |
|           |                              | [sentence_transformers](https://www.sbert.net) | spring-boot-starter-data-redis     |
|           |                              | [NLTK](https://www.nltk.org)                   | jsoup                              |
|           |                              | numpy                                          | sqlite-jdbc                        |

## Result Replicate in Docker

!!! Performance of Crawling is much slower (~30 minutes) under Docker environment. 
    Performance in local is much faster (~2 minutes).
    
In case any error occurs, you can remove all files and run docker compose again.

### Prerequisites

- Before you begin, make sure you have Docker client installed

- Download Docker-compose file [here](https://drive.johnnyip.com/d/s/tG79JmBXF1KOeqJ0z19LYFkIN3rYxpf2/WQruMrHYAUkRIpZCbTFTbveZXPGsPTIz-b7HAfiijYQo)

- After downloaded, create a folder and place the compose.yml inside


- Open Terminal (Mac/Linux), or cmd in Windows, and enter the following commands

```
cd <path_to_your_folder>
docker compose up -d
```

- After those necessary docker images are downloaded, it will be up and running.

- 3 Folders will be created

![](http://johnnyip.com/wp-content/uploads/2023/04/project-docker.png)
- ``db`` folder contains the SQLite file
- ``mongodb`` folder contains data of MongoDB
- ``redis`` folder contains data of Redis DB
