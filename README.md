# BD2 - Monotion

In this project, we developed an API centered in a Notion-like block management system. Once logged in, the user can create, edit, and share blocks as he pleases.
The app was developed in Python, using FastAPI module and Mongo as a document-oriented database that would help us in the block manipulation. 
There are a few considerations that will be explained in detail in the corresponding section.

## Instalation

To install the app, we need to copy the repository and run the following commands in the given order

```bash
make cp-env
```

```bash
make build
```

This commands will generate the needed images to run the app

## Excecution

Once all the installation is finished, to run the project you should only run the following command

```bash
make up
```

## Work and considerations

Now that the project was built and is now running, we can now interact with the Swagger interface and the Mongo Express client respectively
located in `localhost:8002/docs` and `localhost:8081`.

### Swagger (`http://localhost:8002/docs`)
Using this tool, we can interact in a more intuitive way with the API. We can now try every existing method.

![image](https://user-images.githubusercontent.com/67807553/208692686-aa345d08-7a82-41f0-8d54-8688a9a1d978.png)

For trying out the API, the credentials for pre-existing users are

```
admin@gmail.com
admin
```
```
bot@gmail.com
bot
```

### Mongo Express Client (`http://localhost:8081`)
This client provides us an easy way to interact with our MongoDB instance. We can consult any collections and see how the API impacts our DB.

![image](https://user-images.githubusercontent.com/67807553/208691955-27554042-a7da-4b19-bf2d-79835437ebfe.png)

### Kibana (`http://localhost:5601`)
Using this data visualizer, we can see in detail our indexes and how they were built.

![image](https://user-images.githubusercontent.com/67807553/208727519-7e96fbb7-0233-412f-b8b4-93f18cd87557.png)

The yellow health of each index is due to the lack of database replicas.

### Considerations
- We decided to change the implementation proposed in the first presentation of this project, as the deletion process was not efficient and the entire collection of users was iterated when a block was trying to be deleted.
- We decided to share documents publicly instead of sharing them to a certain group of users.
- We decided not to allow all users to create a page-type block inside of another public page. Only the page owner would be the only one capable of creating a page inside an existing page.
- We decided not to impose too many restrictions to the block properties structure. While every page has a title and the other block types have text, the block will be well formed.

## Requirements
- [make](https://www.gnu.org/software/make/)
- [docker-compose](https://docs.docker.com/compose/)
