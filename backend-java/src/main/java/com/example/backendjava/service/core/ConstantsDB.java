package com.example.backendjava.service.core;

public class ConstantsDB {

    public final static String db_path  = "/db/";
    public static final String dbFile   = db_path + "csit5930";

    /****************************************************************************************************
     * Insert
     ****************************************************************************************************/
    public static final String insertUrl          = "insert into url(url) values(?);";
    public static final String insertUrlTemp      = "insert into url_temp(url, last_modified_date) values(?, ?);";
    public static final String insertTerm         = "insert into term(term) values(?);";
    public static final String insertStem         = "insert into stem(stem) values(?);";
    public static final String insertRawToken     = "insert into raw_token(page_id, term_id, type, position) values(?, ?, ?, ?);";
    public static final String insertStemToken    = "insert into stem_token(page_id, stem_id,type, position) values(?, ?, ?, ?);";
    public static final String insertMaxTF        = "insert into max_tf(page_id, max_tf, type) values(?, ?, ?);";
    public static final String insertUrlInverted  = "insert into url_inverted(parent_page_id, child_page_id) values(?, ?);";
    //    public static final String insertUrlForward   = "insert into url_forward(child_page_id, parent_page_id) values(?, ?);";
    public static final String insertStemInverted = "insert into stem_inverted(stem_id, page_id, type) values(?, ?, ?);";
    public static final String insertStemForward  = "insert into stem_forward(page_id, stem_id, type) values(?, ?, ?);";
    public static final String insertStemPosition = "insert into stem_position(stem_id, page_id, type, position) values(?, ?, ?, ?);";
    public static final String insertStemDF       = "insert into stem_df(stem_id, df) values(?, ?);";

    public static final String insertHistory      = "insert into page_update_history values(?, ?, ?, ?, ?);";

    /****************************************************************************************************
     * Update
     ****************************************************************************************************/
    public static final String updateInitiallRawContent
            = "update url set raw_title=?, last_modified_date=?, raw_content=?, doc_length=? where url=?;";

    public static final String updateInitiallClearTitle
            = "update url set clear_title=? where page_id=?;";
    public static final String updateInitiallClearContent
            = "update url set clear_content=? where page_id=?;";

    public static final String updateInitiallStemTitle
            = "update url set stem_title=? where page_id=?;";
    public static final String updateInitiallStemContent
            = "update url set stem_content=? where page_id=?;";

    /****************************************************************************************************
     * Delete / Drop / Create
     ****************************************************************************************************/
    public static final String deleteUrl_temp   = "delete from url_temp";

    public static final String dropUrl = "drop table if exists url;";
    public static final String dropTerm = "drop table if exists term;";
    public static final String dropStem = "drop table if exists stem;";
    public static final String dropRawToken = "drop table if exists raw_token;";
    public static final String dropStemToken = "drop table if exists stem_token;";
    public static final String dropMaxTf = "drop table if exists max_tf;";
    public static final String dropUrlInverted = "drop table if exists url_inverted;";
    public static final String dropUrlForward = "drop table if exists url_forward;";

    public static final String createUrl
            = "create table url ("
            + "page_id integer primary key autoincrement,"
            + "url text not null,"
            + "raw_title text,"
            + "clear_title text,"
            + "stem_title text,"
            + "raw_content text,"
            + "clear_content text,"
            + "stem_content text,"
            + "last_modified_date text,"
            + "doc_length integer"
            + ");";

    public static final String createTerm
            = "create table term ("
            + "term_id integer primary key autoincrement,"
            + "term text not null,"
            + "unique(Term)"
            + ");";

    public static final String createStem
            = "create table stem ("
            + "stem_id integer primary key autoincrement,"
            + "stem text not null,"
            + "unique(stem)"
            + ");";

    public static final String createRawToken
            = "create table raw_token ("
            + "page_id integer not null,"
            + "term_id integer not null,"
            + "type integer not null,"
            + "position integer not null,"
            + "primary key(page_id, term_id, type, position)"
            + ");";

    public static final String createStemToken
            = "create table stem_token ("
            + "page_id integer not null,"
            + "stem_id integer not null,"
            + "type integer not null,"
            + "position integer not null,"
            + "primary key(page_id, stem_id, type, position)"
            + ");";

    public static final String createMaxTf
            = "create table max_tf ("
            + "page_id integer not null,"
            + "max_tf integer not null,"
            + "type integer not null,"
            + "primary key(page_id, type)"
            + ");";

    public static final String createUrlInverted
            = "create table url_inverted ("
            + "parent_page_id integer not null,"
            + "child_page_id integer not null,"
            + "primary key(parent_page_id, child_page_id)"
            + ");";

    public static final String createUrlForward
            = "create table url_forward ("
            + "child_page_id integer not null,"
            + "parent_page_id integer not null,"
            + "primary key(child_page_id, parent_page_id)"
            + ");";


    /****************************************************************************************************
     * Select
     ****************************************************************************************************/
    public static final String selectAllUrl
            = "select * from url;";
    public static final String selectNewUrl
            = "select * from url_temp ut left join url u on u.url = ut.url where u.url is null;";
    public static final String selectRemovedUrl
            = "select * from url u left join url_temp ut on ut.url = u.url where ut.url is null;";
    public static final String selectModifiedUrl
            = "select "
            + "u.page_id, u.url, u.last_modified_date as old_date, ut.last_modified_date as new_date "
            + "from url_temp ut "
            + "inner join url u on u.url = ut.url "
            + "where ut.last_modified_date > u.last_modified_date;";

    public static final String selectAllRawTitleWithPageId
            = "select page_id || ':' || raw_title as 'data' from url;";
    public static final String selectAllRawContentWithPageId
            = "select page_id || ':' || raw_content as 'data' from url;";

    public static final String selectAllClearTitleWithPageId
            = "select page_id || ':' || clear_title as 'data' from url;";
    public static final String selectAllClearContentWithPageId
            = "select page_id || ':' || clear_content as 'data' from url;";

    public static final String selectAllStemTitleWithPageId
            = "select page_id || ':' || stem_title as 'data' from url;";
    public static final String selectAllStemContentWithPageId
            = "select page_id || ':' || stem_content as 'data' from url;";

    public static final String selectAllClearTitleAndContentWithPageId
            = "select data from "
            + "("
            + "select page_id || ':' || clear_title as 'data' from url "
            + "union "
            + "select page_id || ':' || clear_content as 'data' from url"
            + ")"
            + "order by 'data';";

    public static final String selectAllStemTitleAndContentWithPageId
            = "select data from "
            + "("
            + "select page_id || ':' || stem_title as 'data' from url "
            + "union "
            + "select page_id || ':' || stem_content as 'data' from url"
            + ")"
            + "order by 'data';";

    public static final String selectAllPageIdClearTitle
            = "select page_id, clear_title as data from url;";
    public static final String selectAllPageIdStemTitle
            = "select page_id, stem_title as data from url;";

    public static final String selectAllPageIdClearContent
            = "select page_id, clear_content as data from url;";
    public static final String selectAllPageIdStemContent
            = "select page_id, stem_content as data from url;";


    public static final String selectAllPageId
            = "select page_id from url;";
    public static final String selectUrlByPageId
            = "select * from url where page_id=?;";
    public static final String selectPageIdByUrl
            = "select * from url where url=?;";

    public static final String selectTermIdByTerm
            = "select term_id as id from term where term=?;";
    public static final String selectStemIdByStem
            = "select stem_id as id from stem where stem=?;";

    public static final String selectMaxTfByPageId
            = "select max(count) as max_tf "
            + "from ("
            + "     select "
            + "         st.page_id , st.stem_id, s.stem ,st.position ,count(s.stem) as count "
            + "     from stem_token st "
            + "     left join stem s on s.stem_id =st.stem_id where 1=1 "
            + "     and st.page_id=? "
            + "     and st.type=? "
            + "group by st.page_id, st.stem_id, s.stem"
            + ")";

    public static final String selectTotalTerms = "select count(*) from term";
    public static final String selectTotalStem = "select count(*) from stem";
    public static final String selectTitleAndMaxTF = "select u.raw_title, max(t.max_tf) as max_tf " +
            "from max_tf t " +
            "left join url u on u.page_id = t.page_id " +
            "group by t.page_id ; ";
    public static final String selectStemListFrequency = "SELECT s.stem , count(st.page_id) as count\n" +
            "FROM stem s \n" +
            "LEFT JOIN stem_token st ON s.stem_id = st.stem_id\n" +
            "GROUP BY s.stem_id\n" +
            "ORDER BY count DESC;";

    public static final String selectRawListFrequency = "SELECT t.term  , count(rt.page_id) as count\n" +
            "FROM term t \n" +
            "LEFT JOIN raw_token rt ON t.term_id  = rt.term_id \n" +
            "GROUP BY t.term_id \n" +
            "ORDER BY count DESC;";

    public static final String selectRawContent = "SELECT u.url, u.raw_content  \n" +
            "FROM url u;";

    /****************************************************************************************************
     * Insert-Select
     ****************************************************************************************************/
    public static final String insertSelectUrlForward
            = "insert into url_forward (child_page_id, parent_page_id) "
            + "select child_page_id, parent_page_id "
            + "from url_inverted "
            + "order by child_page_id, parent_page_id;";

    /****************************************************************************************************
     * Misc.
     ****************************************************************************************************/
    public static final String indexTypeTerm = "term";
    public static final String indexTypeStem = "stem";

    public static final String scopeAllRawTitle = "scopeAllRawTitle";
    public static final String scopeAllRawContent = "scopeAllRawContent";
    public static final String scopeAllClearTitle = "scopeAllClearTitle";
    public static final String scopeAllClearContent = "scopeAllClearContent";
    public static final String scopeAllStemTitle = "scopeAllStemTitle";
    public static final String scopeAllStemContent = "scopeAllStemContent";
    public static final String scopeAllClearTitleAndContent = "scopeAllClearTitleAndContent";
    public static final String scopeAllStemTitleAndContent = "scopeAllStemTitleAndContent";

    public static final String tokenTypeClearTitle   = "clearTitleToken";
    public static final String tokenTypeClearContent = "clearContentToken";
    public static final String tokenTypeStemTitle   = "stemTitleToken";
    public static final String tokenTypeStemContent = "stemContentToken";

    public static final String dataTypeTitle    = "titleData";
    public static final String dataTypeContent  = "ContentData";

    public static final int dsTypeTitle = 1;
    public static final int dsTypeContent = 2;

    public static final String buildUpdateTypeFull = "full";
    public static final String buildUpdateTypePartial = "partial";
}
