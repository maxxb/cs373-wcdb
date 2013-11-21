# === FIVE UNIQUE QUERIES BELOW === #

#1. Select all government organizations.
#TODO: get link outputted
SELECT name, kind 
    FROM crises_organizations
    WHERE kind='Government Agency';

#2. Select everything not related to anything else.
#select the union of people, orgs, and crises without relations
#TODO: display header row
SELECT 'Person', name FROM crises_people 
	WHERE id not in 
	(SELECT peopledata_id FROM crises_peopledata_crises) 
	and id not in 
	(SELECT peopledata_id FROM crises_peopledata_orgs) 
union 
SELECT 'Organization', name FROM crises_organizations 
	WHERE id not in 
	(SELECT organizationsdata_id FROM crises_organizationsdata_people) 
	and id not in 
	(SELECT organizationsdata_id FROM crises_organizationsdata_crises) 
union SELECT 'Crisis', name FROM crises_crises 
	WHERE id not in 
	(SELECT crisesdata_id FROM crises_crisesdata_orgs) 
	and id not in 
	(SELECT crisesdata_id FROM crises_crisesdata_people);

#3. Select the longest running crisis/crises.
SELECT name, start_date 
	FROM crises_crisesdata 
	INNER JOIN crises_crises 
		ON crisis_id = id 
	WHERE start_date = (SELECT min(start_date) FROM crises_crisesdata);

#4. Select most related (most related people/crises) organizations.
# just print id and count of the most-related
# TODO: inner join R,S with crises_organizations to print name along with it?
SELECT name, total 
	FROM crises_organizations 
	INNER JOIN 
		(SELECT organizationsdata_id, sum(count) AS total 
			FROM 
			(SELECT organizationsdata_id, COUNT(*) AS count 
				FROM crises_organizationsdata_crises GROUP by organizationsdata_id 
			UNION ALL 
				SELECT organizationsdata_id, COUNT(*) AS count 
					FROM crises_organizationsdata_people 
					GROUP by organizationsdata_id) AS Grouping1 
			GROUP BY organizationsdata_id) AS RelationCount 
	ON id = organizationsdata_id 
		WHERE total = (SELECT MAX(total) AS max 
						FROM 
						(SELECT organizationsdata_id, sum(count) AS total 
							FROM (SELECT organizationsdata_id, COUNT(*) AS count 
									FROM crises_organizationsdata_crises 
									GROUP by organizationsdata_id 
								UNION ALL 
									SELECT organizationsdata_id, COUNT(*) AS count 
										FROM crises_organizationsdata_people 
										GROUP by organizationsdata_id) AS Grouping2 
						GROUP BY organizationsdata_id) AS RelationCount2)
#SELECT organizationsdata_id, MAX(numAssociations) FROM
#      (SELECT organizationsdata_id, COUNT(*) AS numAssociations FROM 
#              (crises_organizationsdata_crises INNER JOIN crises_organizationsdata_people USING (or
#              GROUP BY organizationsdata_id);

(SELECT organizationsdata_id, R.x + S.y #not sure
	#count how many times each org_id occurs in each table
	(SELECT organizationsdata_id,	COUNT(*) AS x #`num`
		FROM crises_organizationsdata_crises 
		GROUP BY organizationsdata_id) as R,
	(SELECT organizationsdata_id,	COUNT(*) AS y
		FROM crises_organizationsdata_people 
		GROUP BY organizationsdata_id) as S);

#5. Count the number of crises before the 21st century (earlier than 2000).
SELECT name, start_date 
	FROM crises_crisesdata 
INNER JOIN crises_crises 
ON start_date < '2000-01-01' 
	and crisis_id = id;

#6. Select the person/people involved in most number of crises.
SELECT name FROM crises_people
	WHERE id = person_id
	(SELECT person_id, max(numCrises) FROM 
		(SELECT person_id, count(*) AS numCrises FROM crises_peopledata_crises
			GROUP BY person_id) AS X);

SELECT name, numCrises 
	FROM (SELECT peopledata_id, count(*) As numCrises 
			FROM crises_peopledata_crises 
			GROUP BY peopledata_id) 
			AS poeplecrisescount 
		INNER JOIN crises_people 
			ON peopledata_id = id 
		WHERE numCrises = (SELECT max(numCrises) AS max 
							FROM (SELECT peopledata_id, count(*) AS numCrises 
									FROM crises_peopledata_crises 
									GROUP BY peopledata_id) AS X);

#7. select twitter account link of all people
SELECT twitter FROM crises_peopletwitter #TODO: display name too
SELECT name, twitter 
	FROM crises_people 
INNER JOIN crises_peopletwitter 
	ON crises_people.id = people_id

#8. Select the youngest people in the database
SELECT name, dob 
	FROM crises_people 
INNER JOIN crises_peopledata 
	ON id = person_id 
WHERE dob = (SELECT max(dob) AS minDob 
				FROM crises_peopledata)
#9. Select the crises with the most resources needed
SELECT name, numResourses 
	FROM crises_crises 
INNER JOIN (SELECT crisis_id, count(*) AS numResourses 
				FROM crises_crisesresourses 
				GROUP BY crisis_id) 
				AS R ON id = crisis_id 
			WHERE numResourses = (SELECT max(numResourses) 
									FROM (SELECT crisis_id, count(*) AS numResourses 
											FROM crises_crisesresourses 
											GROUP BY crisis_id) 
											AS T)
#10.Select the crisis kind that has most number of crises.
SELECT kind, numOfCrises 
	FROM (SELECT kind, count(*) AS numOfCrises 
			FROM crises_crises 
			GROUP BY kind) 
			AS Count 
		WHERE numOfCrises = (SELECT max(numOfCrises) 
								FROM (SELECT kind, count(*) AS numOfCrises 
										FROM crises_crises 
										GROUP BY kind) 
										AS Count2)

#Others: Select the crises that have not ended yet. #hard since no "present" end_date
