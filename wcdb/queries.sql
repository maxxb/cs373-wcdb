# === FIVE UNIQUE QUERIES BELOW === #

#1. Select all government organizations.
#TODO: get link outputted
SELECT name, kind FROM crises_organizations WHERE kind="Government Agency" 

#2. Select everything not related to anything else.
#select the union of people, orgs, and crises without relations
SELECT name FROM crises_people
	WHERE id not in
	(SELECT person_id FROM crises_peopledata_crises)
	and id not in
	(SELECT person_id FROM crises_peopledata_orgs)
union
SELECT name FROM crises_organizations	
	WHERE id not in
	(SELECT org_id FROM crises_organizationsdata_people)
	and org_id not in
	(SELECT org_id FROM crises_organizationsdata_crises)
union
SELECT name FROM crises_crises
	WHERE id not in
	(SELECT crisis_id FROM crises_crisesdata_orgs)
	and id not in
	(SELECT crisis_id FROM crises_crisesdata_people);

#3. Select the longest running crisis/crises.
SELECT name, start_date FROM crises_crisesdata INNER JOIN crises_crises 
	WHERE start_date <= all 
		(SELECT start_date FROM crises_crisesdata)
	and crisis_id = id

#4. Select most related (most related people/crises) organizations.
# just print id and count of the most-related
# TODO: inner join R,S with crises_organizations to print name along with it?
SELECT id, R.x + S.y #not sure
	FROM
	#count how many times each org_id occurs in each table
	(SELECT id,	COUNT(*) AS x #`num`
		FROM crises_organizationsdata_crises 
		GROUP BY id) as R,
	(SELECT id,	COUNT(*) AS y
		FROM crises_organizationsdata_people 
		GROUP BY id) as S,
WHERE R.x + S.y >= all;

#5. Count the number of crises before the 21st century (earlier than 2000).
SELECT name, start_date FROM crises_crisesdata INNER JOIN crises_crises WHERE start_date < '2000-01-01' and crisis_id = id

# === FIVE NON-UNIQUE QUERIES BELOW === #
#6. Select the person that is involved in most number of crises.
