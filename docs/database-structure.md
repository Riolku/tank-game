# Database Structure

## Tables:
- Users:
 -uid: integer/uuid
 -username: varchar
 -password (hash): varchar
 -teams: ARRAY (arr of team ids (teams stored in seperate table))
 -ais: ARRAY (arr of AI ids (ais stored somewhere (probably in db)))
- Teams:
 -id: integer/uuid
 -name: varchar
 -tank_n (n = 1,2,3,4,5)(or array idk): json
 {
  -class: varchar (types: repair,artillery,assassin,shield,kamikaze,scout,mortar,htn)
  -ai-id: integer/uuid
 }
- AI's (do we want to store these in the db?!?):
 - id: integer/uuid
 - title: varchar (name of ai)
 - code: (somethingsomething idk)