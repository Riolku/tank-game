#Database Structure

##Tables:
- Users:
 -username: varchar
 -password (hash): varchar
 -teams: ARRAY (arr of team ids (teams stored in seperate table))
- Teams:
 -id: integer
 -name: varchar
 -tank_n (n = 1,2,3,4,5)(or array idk): json
 {
  -class: varchar (types: repair,artillery,assassin,shield,kamikaze,scout,mortar,htn)
  -ai-id: integer
 }
- AI's (do we want to store these in the db?!?)