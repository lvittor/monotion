database = db.getSiblingDB('mongodb');



database.createCollection('users');
database.createCollection('blocks');

database.users.insertMany([
    {
        "_id": ObjectId('639d2ffd68002586d68b232d'),
        "email": 'a@gmail.com',
        "username": 'a',
        "password": '$2b$12$xg/t03ATVG2fRNV9yh8EAueJk9TQgJ.STt5c4ohpLaI8mSLg8qdly',
        "pages": [
            ObjectId("639d4d76abd94dd94b2348cb") 
        ],
    },
    {
        "_id": ObjectId('639e1f2740963d84f4950012'),
        "email": 'b@gmail.com',
        "username": 'b',
        "password": '$2b$12$nZvUwDGzkQRFohMbHq7mR.pL4TFLeTfxmCXxqCza2xMTAhzh26PNy',
        "pages": [],
    }
]);

database.blocks.insertMany([
    {
        "_id": ObjectId("639d4d76abd94dd94b2348cb"),
        "type": "page",
        "properties": {
            "title": "RP"
        },
        "parent": null,
        "content": [
            ObjectId("639d4d9aabd94dd94b2348cc")
        ],
        "is_public": true,
        "creator": ObjectId("639d2ffd68002586d68b232d"),
        "page_owner": ObjectId("639d2ffd68002586d68b232d")
    },
    {
        "_id": ObjectId("639d4d9aabd94dd94b2348cc"),
        "type": "to_do",
        "properties": {
            "title": "A",
            "checked": "No"
        },
        "parent": ObjectId("639d4d76abd94dd94b2348cb"),
        "content": [
            ObjectId("639d516a7e496c4aea0f8bcb"),
            ObjectId("639d518f7e496c4aea0f8bcd"),
        ],
        "is_public": true,
        "creator": ObjectId("639d2ffd68002586d68b232d"),
        "page_owner": ObjectId("639d2ffd68002586d68b232d")
    },
    {
        "_id": ObjectId("639d516a7e496c4aea0f8bcb"),
        "type": "to_do",
        "properties": {
            "title": "B",
            "checked": "No"
        },
        "parent": ObjectId("639d4d9aabd94dd94b2348cc"),
        "content": [
            ObjectId("639d517b7e496c4aea0f8bcc")
        ],
        "is_public": true,
        "creator": ObjectId("639d2ffd68002586d68b232d"),
        "page_owner": ObjectId("639d2ffd68002586d68b232d")
    },
    {
        "_id": ObjectId("639d517b7e496c4aea0f8bcc"),
        "type": "to_do",
        "properties": {
            "title": "D",
            "checked": "No"
        },
        "parent": ObjectId("639d516a7e496c4aea0f8bcb"),
        "content": [],
        "is_public": true,
        "creator": ObjectId("639d2ffd68002586d68b232d"),
        "page_owner": ObjectId("639d2ffd68002586d68b232d")
    },
    {
        "_id": ObjectId("639d518f7e496c4aea0f8bcd"),
        "type": "to_do",
        "properties": {
            "title": "C",
            "checked": "No"
        },
        "parent": ObjectId("639d4d9aabd94dd94b2348cc"),
        "content": [],
        "is_public": true,
        "creator": ObjectId("639d2ffd68002586d68b232d"),
        "page_owner": ObjectId("639d2ffd68002586d68b232d")
    }
]);

