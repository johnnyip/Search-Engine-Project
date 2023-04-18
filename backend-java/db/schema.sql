-- ----------------------------------------------------------------------------------------------------
--  Test Table
-- ----------------------------------------------------------------------------------------------------
--drop table test;
--create table test (
--    id integer primary key autoincrement,
--    txt_1 text not null,
--    int_2 int
--);
--pragma table_info(test);
-- ----------------------------------------------------------------------------------------------------
--  Url
-- ----------------------------------------------------------------------------------------------------
drop table url;
create table url (
    page_id integer primary key autoincrement,
    url text not null,
    raw_title text,
    clear_title text,
    stem_title text,
    raw_content text,
    clear_content text,
    stem_content text,
    last_modified_date text
);
pragma table_info(url);
-- ----------------------------------------------------------------------------------------------------
--  Term
-- ----------------------------------------------------------------------------------------------------
drop table term;
create table term (
    term_id integer primary key autoincrement,
    term text not null,
    unique(Term)
);
pragma table_info(term);
-- ----------------------------------------------------------------------------------------------------
--  Stem
-- ----------------------------------------------------------------------------------------------------
drop table stem;
create table stem (
    stem_id integer primary key autoincrement,
    stem text not null,
    unique(stem)
);
pragma table_info(stem);
-- ----------------------------------------------------------------------------------------------------
--  RawToken
-- ----------------------------------------------------------------------------------------------------
drop table raw_token;
create table raw_token (
    page_id integer not null,
    term_id integer not null,
    type integer not null,
    position integer not null,
    primary key(page_id, term_id, type, position)
);
pragma table_info(raw_token);
-- ----------------------------------------------------------------------------------------------------
--  StemToken
-- ----------------------------------------------------------------------------------------------------
drop table stem_token;
create table stem_token (
    page_id integer not null,
    stem_id integer not null,
    type integer not null,
    position integer not null,
    primary key(page_id, stem_id, type, position)
);
pragma table_info(stem_token);
-- ----------------------------------------------------------------------------------------------------
--  MaxTF
-- ----------------------------------------------------------------------------------------------------
drop table max_tf;
create table max_tf (
    page_id integer not null,
    max_tf integer not null,
    type integer not null,
    primary key(page_id, type)
);
pragma table_info(max_tf);
-- ----------------------------------------------------------------------------------------------------
--  UrlInverted
-- ----------------------------------------------------------------------------------------------------
drop table url_inverted;
create table url_inverted (
--    url_inverted_id integer primary key autoincrement,
    parent_page_id integer not null,
    child_page_id integer not null,
    primary key(parent_page_id, child_page_id)
);
pragma table_info(url_inverted);
-- ----------------------------------------------------------------------------------------------------
--  UrlForward
-- ----------------------------------------------------------------------------------------------------
drop table url_forward;
create table url_forward (
--    url_forward_id integer primary key autoincrement,
    child_page_id integer not null,
    parent_page_id integer not null,
    primary key(child_page_id, parent_page_id)
);
pragma table_info(url_forward);
-- ----------------------------------------------------------------------------------------------------
--  StemInvertedTitle (Change to View)
-- ----------------------------------------------------------------------------------------------------
drop view v_stem_inverted_title;
create view v_stem_inverted_title
as
select
    st.stem_id, s.stem
    ,st.page_id, u.url  
    ,st.position
--    ,st.type 
from stem_token st
left join stem s on s.stem_id = st.stem_id 
left join url u on u.page_id = st.page_id
where type=1
order by st.stem_id, st.page_id, st.position
;
pragma table_info(v_stem_inverted_title);
-- ----------------------------------------------------------------------------------------------------
--  StemInvertedContent (Change to View)
-- ----------------------------------------------------------------------------------------------------
drop view v_stem_inverted_content;
create view v_stem_inverted_content
as
select
    st.stem_id, s.stem
    ,st.page_id, u.url  
    ,st.position
--    ,st.type 
from stem_token st
left join stem s on s.stem_id = st.stem_id 
left join url u on u.page_id = st.page_id
where type=2
order by st.stem_id, st.page_id, st.position
;
pragma table_info(v_stem_inverted_content);
-- ----------------------------------------------------------------------------------------------------
--  StemForwardTitle (Change to View)
-- ----------------------------------------------------------------------------------------------------
drop view v_stem_forward_title;
create view v_stem_forward_title
as
select
    st.page_id
    ,st.stem_id, s.stem
--    ,st.type
from stem_token st 
left join stem s on s.stem_id = st.stem_id 
where st.type=1
order by st.page_id, st.stem_id
;
pragma table_info(v_stem_forward_title);
-- ----------------------------------------------------------------------------------------------------
--  StemForwardContent (Change to View)
-- ----------------------------------------------------------------------------------------------------
drop view v_stem_forward_content;
create view v_stem_forward_content
as
select
    st.page_id
    ,st.stem_id, s.stem
--    ,st.type
from stem_token st 
left join stem s on s.stem_id = st.stem_id 
where st.type=2
order by st.page_id, st.stem_id
;
pragma table_info(v_stem_forward_content);
-- ----------------------------------------------------------------------------------------------------
--  StemPosition (replaced my v_stem_inverted_title & v_stem_inverted_content)
-- ----------------------------------------------------------------------------------------------------
--drop table stem_position;
--create table stem_position (
--    stem_id integer not null,
--    page_id integer not null,
--    type int integer null,
--    position integer not null,
--    primary key(stem_id, page_id, type, position)
--);
--pragma table_info(stem_position);
-- ----------------------------------------------------------------------------------------------------
--  StemDF (Change to View)
-- ----------------------------------------------------------------------------------------------------
drop view v_stem_df;
create view v_stem_df
as
select
    a.stem_id
    , (select stem from stem where stem_id =a.stem_id) as stem
    , count(page_id) as df
from (
    select
        distinct stem_id , page_id 
    from 
    stem_token st 
    order by stem_id , page_id 
) a
group by a.stem_id
;
pragma table_info(v_stem_df);
