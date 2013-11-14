#Select all organizations operating in multiple countries.
SELECT org_id FROM OrganizationsData

#Select everything not related to anything else.
SELECT person_id FROM 
#union
SELECT org_id
#union
SELECT crisis_id

#Select the longest running crisis.
SELECT

#Select most related (most related people/crises) organizations.
SELECT

#Count the number of crises before the 21st century (earlier than 2000).
SELECT name, start_date FROM crises_crisesdata INNER JOIN crises_crises WHERE start_date < '2000-01-01' and crisis_id = id
