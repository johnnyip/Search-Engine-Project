-- ----------------------------------------------------------------------------------------------------
--  Url
-- ----------------------------------------------------------------------------------------------------
select * from url where 1=1
;

select page_id || ':' || clear_content as ccontent from url;
select page_id || ':' || raw_content as 'data' from url;

-- MySQL: update url set clear_content=REGEXP_REPLACE(LOWER(raw_content), '[^a-z0-9]', ' ');


select regexp_replace('password = "123456"', '"[^"]+"', '***');

select page_id || ':' || raw_content  as 'data' from url;

select lower(url) from url;
;

select page_id, raw_title, clear_title from url;
select page_id, raw_content, clear_content from url;

select page_id || ':' || clear_title as 'data' from url;
select clear_title, stem_title from url;
select clear_content, stem_content from url;

select page_id, title, clear_title, stem_title from url where 1=1;

-- ----------------------------------------------------------------------------------------------------
--  Term
-- ----------------------------------------------------------------------------------------------------

select count(*) from term;
select * from term where 1=1
order by term
;

-- All Term
select page_id || ':' || clear_title as data from url
union
select page_id || ':' || clear_content as data from url
;
order by 'data'

-- ----------------------------------------------------------------------------------------------------
--  Stem
-- ----------------------------------------------------------------------------------------------------

select count(*) from stem;
select * from stem where 1=1
--and stem_id = -1
--and stem ='imdb'
--order by 
--stem_id 
--stem
;

-- All Stem
select data from
(select page_id || ':' || stem_title as data from url
union
select page_id || ':' || stem_content as data from url
)
order by 'data'
;


-- ----------------------------------------------------------------------------------------------------
--  Raw Token
-- ----------------------------------------------------------------------------------------------------
--create table raw_token (
--    id integer primary key autoincrement,
--    page_id integer not null,
--    term_id integer not null,
--    type integer not null,
--    position integer not null
--);

select * from raw_token rt where 1=1
--and term_id=-1
--order by
;

select page_id, clear_content from url where 1=1
and page_id=1 -- Test page
--and page_id=18 -- Dinosaur Planet (2003)
;


select 
    rt.page_id, u.clear_title,
    rt.term_id, t.term,
    rt."position",
    rt."type" 
from raw_token rt
left join Url u on u.page_id = rt.page_id 
left join term t on t.term_id =rt.term_id
where 1=1
and rt.page_id=1
--and rt.term_id=2
--and rt."type"=1
and rt."type"=2
order by rt."position" 
;

-- ----------------------------------------------------------------------------------------------------
--  Stem Token
-- ----------------------------------------------------------------------------------------------------

select u.page_id , u.raw_title ,u.stem_content  from url u where u.page_id =1;

select * from stem_token st where 1=1
--and stem_id =-1
and st.page_id = 1
;

select st.page_id, st.stem_id, s.stem, st."position", st."type"  
from stem_token st
left join stem s on s.stem_id =st.stem_id 
where 1=1
and st.page_id=18
--and s.stem ='dinosaur'
and st."type" =1
order by 
st."position"
--s.stem 
;



select 
    st.page_id, 
    u.clear_title , u.stem_title ,
    st.stem_id , s.stem ,
    st."position" ,
    st."type" 
from stem_token st
left join url u on u.page_id =st.page_id 
left join stem s on s.stem_id =st.stem_id 
where 1=1
and st.page_id =1
and st."type" =2
order by st."position" 
;

-- ----------------------------------------------------------------------------------------------------
--  MaxTF
-- ----------------------------------------------------------------------------------------------------
--create table max_tf (
--    page_id integer not null,
--    max_tf integer not null,
--    type integer not null,
--    primary key(page_id, type)
)

select page_id from url;

select 
    page_id, stem, stem, max(count) as max_tf
from (
    select 
        st.page_id , st.stem_id, s.stem ,st.position ,count(s.stem) as count
    from stem_token st 
    left join stem s on s.stem_id =st.stem_id where 1=1
    and st.page_id=18
    and st.type=1
    group by st.page_id, st.stem_id, s.stem
)
;

select * from max_tf mt where 1=1
--and mt.page_id=18
;
-- ----------------------------------------------------------------------------------------------------
--  UrlInverted
-- ----------------------------------------------------------------------------------------------------

select * from url u;
select * from url_inverted ui ;

select
    parent_page_id ,(select url from url where page_id=parent_page_id) as parent_url,
    child_page_id, (select url from url where page_id=child_page_id)  as child_url
from url_inverted ui where 1=1
and parent_page_id =18
;

-- ----------------------------------------------------------------------------------------------------
--  UrlForward
-- ----------------------------------------------------------------------------------------------------
select * from (select distinct child_page_id from url_inverted ui order by child_page_id) a
right join selec


select * 
from url_inverted ui 
--where ui.child_page_id=2
;

select * from url_forward uf ;

select 
    child_page_id, parent_page_id
from url_inverted ui 
order by ui.child_page_id, ui.parent_page_id  
;

select count(*) from url_inverted ui ;
select count(*) from url_forward uf;


insert into url_forward (child_page_id, parent_page_id)
select 
    child_page_id, parent_page_id
from url_inverted ui 
order by ui.child_page_id, ui.parent_page_id  
;

select * from url_forward uf;

-- ----------------------------------------------------------------------------------------------------
--  StemInvertedTitle (View)
-- ----------------------------------------------------------------------------------------------------
select * from v_stem_inverted_title;

-- ----------------------------------------------------------------------------------------------------
--  StemInvertedContent (View)
-- ----------------------------------------------------------------------------------------------------
select * from v_stem_inverted_content;

-- ----------------------------------------------------------------------------------------------------
--  StemForwardTitle (View)
-- ----------------------------------------------------------------------------------------------------
select * from v_stem_forward_title;

-- ----------------------------------------------------------------------------------------------------
--  StemForwardContent (View)
-- ----------------------------------------------------------------------------------------------------
select * from v_stem_forward_content;

-- ----------------------------------------------------------------------------------------------------
--  StemD (View)
-- ----------------------------------------------------------------------------------------------------
select * from v_stem_df;
