use anguslipse_csit5930;
use csit5930;

-- ----------------------------------------------------------------------------------------------------
--  Test Table
-- ----------------------------------------------------------------------------------------------------
drop table test;
create table test (
    id integer primary key autoincrement,
    txt_1 text not null,
    int_2 int
);
pragma table_info(test);

insert into Test(Txt1, Int2) values('1', 2);

select * from test;
-- ----------------------------------------------------------------------------------------------------

== MySQL ==
Start [ buildUrl ] ... 
(22.745 seconds)
[ Done ]

== SQLite ==
Start [ buildUrl ] ... 
(24.265 seconds)
[ Done ]


== MySQL ==
Start [ updateUrlInitContent ] ... 
(60.202 seconds)
[ Done ]

== SQLite ==
Start [ updateUrlInitContent ] ... 
(114.324 seconds)
[ Done ]

Start [ updateUrlInitContent ] ... 
(87.235 seconds)
[ Done ]


== MySQL ==
Start [ normalizeUrlContent ] ... 
(1.592 seconds)
[ Done ]

== SQLite ==
Start [ normalizeRawContentInJava ] ... 
(0.662 seconds)
[ Done ]


== MySQL ==
Start [ updateUrlInitStemContent ] ... 
(4331.671 seconds)
[ Done ]

== SQLite ==
Start [ updateUrlInitStemContent ] ... 
(7.196 seconds)
[ Done ]


Start [ buildTerm ] ... 
[Total unique [term]: 17016]
(0.152 seconds)
[ Done ]

Start [ buildStem ] ... 
[Total unique [stem]: 14194]
(0.088 seconds)
[ Done ]

Start [ buildRawContentToken ] ... 
(27.218 seconds)
[ Done ]




-- ----------------------------------------------------------------------------------------------------
-- 	Url
-- ----------------------------------------------------------------------------------------------------
drop table url;
create table Url (
    page_id integer primary key autoincrement,
    url text not null,
    title text,
    last_modified_date text,
    raw_content text,
    clear_content text,
    stem_content text
);
pragma table_info(url);

select count(*) from Url;
select * from Url where 1=1
-- and url='https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm'
;
select RawContent from Url where RawContent not like '%[,.!?;;]%';
select ClearContent from Url where ClearContent like '%[,.!?;;][A-Z]%';

update Url set ClearContent = null;
update Url set ClearContent=REGEXP_REPLACE(LOWER(RawContent), '[^a-z0-9]', ' ');
select RawContent, ClearContent from Url;
select ClearContent, StemContent from Url;

select concat(PageId,':', ClearContent) as cContent from Url;
-- ----------------------------------------------------------------------------------------------------
-- 	Term
-- ----------------------------------------------------------------------------------------------------
drop table term;
create table term (
    term_id integer primary key autoincrement,
    Term text not null,
    unique(Term)
);
pragma table_info(term);

select count(*) from Term;
-- term count[17456], inserted[17454]
-- stem count[14317], inserted[17454]
select * from Term where 1=1
and Term REGEXP '[^a-zA-Z0-9]'
-- and Term like '%[^a-zA-Z0-9]%'
order by Term 
;
select TermId from Term where Term='drinks';
select TermId from Term where Term='books';

insert into Term(Term) values("books");
insert into Term(Term) values("drinks");
insert into Term(Term) values("happy");
insert into Term(Term) values("pp");

-- ----------------------------------------------------------------------------------------------------
-- 	Stem
-- ----------------------------------------------------------------------------------------------------
drop table stem;
create table stem (
    stem_id integer primary key autoincrement,
    stem text not null,
    unique(stem)
);
pragma table_info(stem);

select count(*) from Stem;

select * from Stem where 1=1
order by Stem;
select StemId from Stem where Stem='drinks';

insert into Stem(Stem) values("pp");
insert into Stem(Stem) values("app");

-- ----------------------------------------------------------------------------------------------------
-- 	RawToken
-- ----------------------------------------------------------------------------------------------------
drop table raw_token;
create table raw_token (
    id integer primary key autoincrement,
    page_id integer not null,
    stem_id integer not null,
    type integer not null,
    position integer not null
);
pragma table_info(raw_token);
-- ----------------------------------------------------------------------------------------------------
-- 	StemToken
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
-- 	MaxTF
-- ----------------------------------------------------------------------------------------------------
drop table max_tF;
create table max_tF (
    page_id integer not null,
    type integer not null,
    max_tF integer not null,
    primary key(page_id, type)
);
pragma table_info(max_tf);
-- ----------------------------------------------------------------------------------------------------
-- 	UrlInverted
-- ----------------------------------------------------------------------------------------------------
drop table url_inverted;
create table url_inverted (
    url_inverted_id integer primary key autoincrement,
    parent_page_id integer not null,
    child_page_id integer not null
);
pragma table_info(url_inverted);
-- ----------------------------------------------------------------------------------------------------
-- 	UrlForward
-- ----------------------------------------------------------------------------------------------------
drop table url_forward;
create table url_forward (
    url_forward_id integer primary key autoincrement,
    child_page_id integer not null,
    parent_page_id integer not null
);
pragma table_info(url_forward);
-- ----------------------------------------------------------------------------------------------------
-- 	StemInverted
-- ----------------------------------------------------------------------------------------------------
drop table stem_inverted;
create table stem_inverted (
    stem_id integer not null,
    page_id integer not null,
    type int integer null,
    primary key(stem_id, page_id, type)
);
pragma table_info(stem_inverted);
-- ----------------------------------------------------------------------------------------------------
-- 	StemForward
-- ----------------------------------------------------------------------------------------------------
drop table stem_forward;
create table stem_forward (
    page_id integer not null,
    stem_id integer not null,
    type integer not null,
    primary key(page_id, stem_id, type)
);
pragma table_info(stem_forward);
-- ----------------------------------------------------------------------------------------------------
-- 	StemPosition
-- ----------------------------------------------------------------------------------------------------
drop table stem_position;
create table stem_position (
    stem_id integer not null,
    page_id integer not null,
    type int integer null,
    position integer not null,
    primary key(stem_id, page_id, type, position)
);
pragma table_info(stem_position);
-- ----------------------------------------------------------------------------------------------------
--  StemDF
-- ----------------------------------------------------------------------------------------------------
drop table stem_df;
create table stem_df (
    stem_id int not null,
    type integer not null,
    df integer not null,
    primary key(stem_id, type)
);
pragma table_info(stem_dF);
