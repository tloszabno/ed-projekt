--czy są różne regiony dla tego samego usera
select r1.userid_di,r2.userid_di,r1.final_cc_cname_di,r2.final_cc_cname_di  
	from raw_data as r1 join raw_data as r2 
		on r1.userid_di = r2.userid_di 
		where r1.final_cc_cname_di <> r2.final_cc_cname_di;
-- tak :(


--ile osób nie ma wpisanego wykształcenia
select count(*) from raw_data where loe_di is null;
-- 47876


--czy są osoby, że dla jakiego kursu mają różne wykształcenie
select r1.userid_di,r2.userid_di,r1.loe_di,r2.loe_di  
	from raw_data as r1 join raw_data as r2 
		on r1.userid_di = r2.userid_di 
		where r1.loe_di <> r2.loe_di;
--nie :)


-- jakie są i ile jest różnych regionów
select distinct final_cc_cname_di from raw_data;
-- 34

--czy ci sami userzy mają różne daty urodzenia?
select r1.userid_di,r2.userid_di,r1.yob,r2.yob  
	from raw_data as r1 join raw_data as r2 
		on r1.userid_di = r2.userid_di 
		where r1.yob <> r2.yob;
-- nie :)

--a płci nikt nie zmienił
select r1.userid_di,r2.userid_di,r1.gender, r2.gender  
	from raw_data as r1 join raw_data as r2 
		on r1.userid_di = r2.userid_di 
		where r1.gender <> r2.gender;
-- na szczęście nie :)


select count(*) from raw_data where course_id like '%CS50x%' and incomplete_flag = 1


-- liczba użytkowników per kurs
select course_id, count(userid_di) from raw_data group by course_id
-- z nazwami kursów
select c.name, count(rd.userid_di) from raw_data as rd 
	join users_on_courses as uoc on rd.id = uoc.raw_data_old_id 
	join courses as c on c.id = uoc.course_id
	group by c.name

	
	
--ilość kursów ukończonych przez użytkowników
select userid_di, count(course_id) as finished_courses from raw_data 
	where certified = 1
	group by userid_di 
	order by finished_courses desc;

--ilość kursów ropoczętych przez użytkowników
select userid_di, count(course_id) as courses from raw_data 
	group by userid_di 
	order by courses desc;
