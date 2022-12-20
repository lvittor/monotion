def purge_page_data(data):
    purged_data = []
    for hit in data:
        found = {
            "block_id": hit["_source"]["id"],
            "type": "page",
            "title": hit["_source"]["title"],
            "is_public": hit["_source"]["is_public"],
            "page_owner": hit["_source"]["page_owner"],
        }
        purged_data.append(found)
    return purged_data


def purge_note_data(data):
    purged_data = []
    for hit in data:
        found = {
            "block_id": hit["_source"]["id"],
            "type": hit["_source"]["type"],
            "text": hit["_source"]["properties"]["text"],
            "is_public": hit["_source"]["is_public"],
            "creator": hit["_source"]["creator"],
        }
        purged_data.append(found)
    return purged_data


def purge_user_data(data):

    return
