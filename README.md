# Search-Engine-Project

## Teammates

[@Alexlam0258](https://github.com/Alexlam0258)
[@cpawongaa](https://github.com/cpawongaa)

This project is given a starting page [Here](https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm):

- Crawl all the child pages contents
- Build indexes in database
- Search query using the indexes
- Create a frontend for accepting user query

[Project Report](https://drive.google.com/file/d/1oM3HbAVy2fVSZ04gV7BcqzMVeHD2PA71/view?usp=share_link)

# Architecture

![Architecture](./architecture.png)

# URL and Libraries Used

|           | **Frontend**                 | **Python Backend**                             | **Java Backend**               |
| --------- | ---------------------------- | ---------------------------------------------- | ------------------------------ |
| URL       | https://search.johnnyip.com/ | -                                              | -                              |
| Libraries | React.js                     | Flask                                          | Spring Boot                    |
|           | Mantine (UI)                 | pymongo                                        | htmlparser                     |
|           | Axios                        | sqlite3                                        | gson                           |
|           |                              | [sentence_transformers](https://www.sbert.net) | spring-boot-starter-data-redis |
|           |                              | [NLTK](https://www.nltk.org)                   | jsoup                          |
|           |                              | numpy                                          | sqlite-jdbc                    |

## Result Replicate in Docker

!!! Performance of Crawling is much slower (~30 minutes) under Docker environment.
Performance in local is much faster (~2 minutes).

!!! DB file in backend-java is a blank template. It is used for future data update during initialization.

In case any error occurs, please remove all files and run docker compose again.

### Prerequisites

- Before you begin, make sure you have Docker client installed

- Make sure the `compose.yaml` file is inside the folder

- Open Terminal (Mac/Linux), or cmd in Windows, and enter the following commands

```
cd <path_to_your_folder>
docker compose up -d
```

- After those necessary docker images are downloaded, it will be up and running.

- 3 Folders will be created

![](http://johnnyip.com/wp-content/uploads/2023/04/project-docker.png)

- `db` folder contains the SQLite file
- `mongodb` folder contains data of MongoDB
- `redis` folder contains data of Redis DB
