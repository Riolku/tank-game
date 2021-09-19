# Database Structure

## Tables:
- Users:
 -uid: integer/uuid
 -username: varchar
 -password (hash): varchar
 -ais: ARRAY (arr of AI ids (ais stored somewhere (probably in db)))
- AI's (do we want to store these in the db?!?):
 - id: integer/uuid
 - title: varchar (name of ai)
 - code: (somethingsomething idk)