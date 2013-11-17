# === FIVE UNIQUE QUERIES BELOW === #

#1. Select all government organizations.
#TODO: get link outputted
SELECT name, kind FROM crises_organizations WHERE kind="Government Agency";

#2. Select everything not related to anything else.
#select the union of people, orgs, and crises without relations
#TODO: display header row
SELECT "Person", name FROM crises_people
	WHERE id not in
	(SELECT peopledata_id FROM crises_peopledata_crises) #not sure why id doesn't work...
	and id not in
	(SELECT peopledata_id FROM crises_peopledata_orgs)
union
SELECT "Organization", name FROM crises_organizations	
	WHERE id not in
	(SELECT organizationsdata_id FROM crises_organizationsdata_people)
	and id not in
	(SELECT organizationsdata_id FROM crises_organizationsdata_crises)
union
SELECT "Crisis", name FROM crises_crises
	WHERE id not in
	(SELECT crisesdata_id FROM crises_crisesdata_orgs)
	and id not in
	(SELECT crisesdata_id FROM crises_crisesdata_people);

#3. Select the longest running crisis/crises.
SELECT name, start_date FROM 
	crises_crisesdata INNER JOIN crises_crises ON crisis_id = id #ON required, otherwise cross join
	WHERE start_date = 
		(SELECT min(start_date) FROM crises_crisesdata)
	and crisis_id = id;

#4. Select most related (most related people/crises) organizations.
# just print id and count of the most-related
# TODO: inner join R,S with crises_organizations to print name along with it?
SELECT organizationsdata_id, MAX(numAssociations) FROM
	(SELECT organizationsdata_id, COUNT(*) AS numAssociations FROM 
		(crises_organizationsdata_crises INNER JOIN crises_organizationsdata_people USING (organizationsdata_id))
		GROUP BY organizationsdata_id);

#5. Count the number of crises before the 21st century (earlier than 2000).
SELECT name, start_date FROM crises_crisesdata INNER JOIN crises_crises WHERE start_date < '2000-01-01' and crisis_id = id

#6. Select the person/people involved in most number of crises.
SELECT name FROM crises_people
	WHERE id = person_id
	(SELECT person_id, max(numCrises) FROM 
		(SELECT person_id, count(*) AS numCrises FROM crises_peopledata_crises
			GROUP BY person_id) AS X);
