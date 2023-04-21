package com.example.backendjava.service.core;

import java.awt.Toolkit;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.sql.Connection;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Date;
import java.util.LinkedHashSet;
import java.util.Set;
import java.util.StringTokenizer;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

//import to.UrlTO;
import com.example.backendjava.service.utils.ArrayUtil;
import com.example.backendjava.service.utils.DBUtil;
import com.example.backendjava.service.utils.StopStem;
import com.example.backendjava.service.utils.StopWatch;
import com.example.backendjava.service.utils.StringUtil;
import com.example.backendjava.service.utils.DateUtil;


import static com.example.backendjava.service.utils.Logger.*;

public class Indexer extends Base {

    private String proc_name;

    private StopWatch timer_overall;
    private StopWatch timer;

    private DBUtil db;
    private Connection conn;
    private ArrayList<Object> data;
    private String insert_query;

    public Indexer() {
        timer_overall = new StopWatch();
        timer = new StopWatch();
        db = new DBUtil();
    }

//    private void buildUrl(String m_build_update_type) {
//        ArrayList<String> links = null;
//        if(m_build_update_type.equals(ConstantsDB.buildUpdateTypeFull)) {
//            links = Spider.getAllUrlList(Constants.base_url); // for init case
//        } else {
//            links = SearchEngine.getNewUrl(); // for new links added cases
//        }
//        buildUrl(links);
//    }

    private void buildUrl() {
        proc_name = "buildUrl";
        printStart(proc_name);
        timer.start();

        ArrayList<String> links = Spider.getAllUrlList(Constants.base_url);

        try {
            conn = db.getConnection();
//            ArrayList<String> links =
            for(String link: links) {
                data = new ArrayList<Object>();
                data.add(link);
                db.genericInsertUpdateDelete(conn, ConstantsDB.insertUrl, data);
            }
            conn.commit();
            conn.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }

        timer.stop();
        timer.printElapseTimeInSecond();
        printDone();
    }

    private void updateUrlInitContent() {
        proc_name = "updateUrlInitContent";
        printStart(proc_name);
        timer.start();

        ArrayList<String> links = SearchEngine.getFullUrlList(false);

        try {
            conn = db.getConnection();
            for(String link: links) {
                URL url = new URL(link);
                HttpURLConnection httpCon = (HttpURLConnection) url.openConnection();
//                String strLastModifiedDate = new Date(httpCon.getLastModified()).toString();
                Date web_date = new Date(httpCon.getLastModified());
                String strLastModifiedDate =  DateUtil.getFormattedDate(web_date);
                int content_length = httpCon.getContentLength();

                Document doc = Jsoup.connect(link).get();
                String title = doc.title();
                String raw = doc.body().text();

                data = new ArrayList<Object>();
                data.add(title);
                data.add(strLastModifiedDate);
                data.add(raw);
                data.add(content_length);
                data.add(link);
                db.genericInsertUpdateDelete(conn, ConstantsDB.updateInitiallRawContent, data);
            }
            conn.commit();
            conn.close();
        } catch(IOException e) {
            e.printStackTrace();
        } catch(SQLException e) {
            e.printStackTrace();
        }

        timer.stop();
        timer.printElapseTimeInSecond();
        printDone();
    }

    private void normalizeRawTitle() {
        normalizeRawData(ConstantsDB.dataTypeTitle);
    }

    private void normalizeRawContent() {
        normalizeRawData(ConstantsDB.dataTypeContent);
    }

    private void normalizeRawData(String m_data_type) {

        if(m_data_type.equals(ConstantsDB.dataTypeTitle)) {
            proc_name = "normalizeRawTitle";
        } else if(m_data_type.equals(ConstantsDB.dataTypeContent)) {
            proc_name = "normalizeRawContent";
        }

        printStart(proc_name);
        timer.start();

        ArrayList<String> srcs = null;
        if(m_data_type.equals(ConstantsDB.dataTypeTitle)) {
            srcs = SearchEngine.getSrcWithPageId(ConstantsDB.scopeAllRawTitle);
        } else if(m_data_type.equals(ConstantsDB.dataTypeContent)) {
            srcs = SearchEngine.getSrcWithPageId(ConstantsDB.scopeAllRawContent);
        }
//        ArrayUtil.printArrayList(srcs);

        try {
            conn = db.getConnection();
            for(String src: srcs) {
                String page_id = src.substring(0, src.indexOf(":"));
                String raw = src.substring(src.indexOf(":")+1);
                raw = raw.toLowerCase();
                raw = StringUtil.replaceSpecialCharacterToSpace(raw);
//                printKVPair(pageId, raw);

                data = new ArrayList<Object>();
                data.add(raw);
                data.add(page_id);

                String query = null;
                if(m_data_type.equals(ConstantsDB.dataTypeTitle)) {
                    query = ConstantsDB.updateInitiallClearTitle;
                } else if(m_data_type.equals(ConstantsDB.dataTypeContent)) {
                    query = ConstantsDB.updateInitiallClearContent;
                }
                db.genericInsertUpdateDelete(conn, query, data);
            }
            conn.commit();
            conn.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }

        timer.stop();
        timer.printElapseTimeInSecond();
        printDone();
    }

    private void updateUrlInitStemTitle() {
        updateUrlInitStem(ConstantsDB.dataTypeTitle);
    }

    private void updateUrlInitStemContent() {
        updateUrlInitStem(ConstantsDB.dataTypeContent);
    }

    private void updateUrlInitStem(String m_data_type) {

        if(m_data_type.equals(ConstantsDB.dataTypeTitle)) {
            proc_name = "updateUrlInitStemTitle";
        } else if(m_data_type.equals(ConstantsDB.dataTypeContent)) {
            proc_name = "updateUrlInitStemContent";
        }

        printStart(proc_name);
        timer.start();

        try {

            ArrayList<String> srcs = null;

            if(m_data_type.equals(ConstantsDB.dataTypeTitle)) {
                srcs = SearchEngine.getSrcWithPageId(ConstantsDB.scopeAllClearTitle);
            } else if(m_data_type.equals(ConstantsDB.dataTypeContent)) {
                srcs = SearchEngine.getSrcWithPageId(ConstantsDB.scopeAllClearContent);
            }

            conn = db.getConnection();

            for(String cContent: srcs) {

                String pageId = cContent.substring(0, cContent.indexOf(":"));
                cContent = cContent.substring(cContent.indexOf(":")+1);

                String nContent = null;

                StringTokenizer st = new StringTokenizer(cContent, " ");
                while(st.hasMoreTokens()) {
                    String term = st.nextToken().strip();
                    if(term.length()>0) {
                        StopStem ss = new StopStem();
                        if(!ss.isStopWord(term)) {
                            term = ss.stem(term);
                            if(nContent==null) {
                                nContent = term;
                            } else {
                                nContent += " " +term;
                            }

                            data = new ArrayList<Object>();
                            data.add(nContent);
                            data.add(pageId);

                            String query = null;
                            if(m_data_type.equals(ConstantsDB.dataTypeTitle)) {
                                query = ConstantsDB.updateInitiallStemTitle;
                            } else if(m_data_type.equals(ConstantsDB.dataTypeContent)) {
                                query = ConstantsDB.updateInitiallStemContent;
                            }

                            db.genericInsertUpdateDelete(conn, query, data);
                        }
                    }
                }
//                printKVPair(pageId, nContent);
            }

            conn.commit();
            conn.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }

        timer.stop();
        timer.printElapseTimeInSecond();
        printDone();
    }

    private void buildTerm() {
        buildTermOrStem(ConstantsDB.indexTypeTerm);
    }

    private void buildStem() {
        buildTermOrStem(ConstantsDB.indexTypeStem);
    }

    private void buildTermOrStem(String m_term_stem) {

        if(m_term_stem.equals(ConstantsDB.indexTypeTerm)) {
            proc_name = "buildTerm";
        } else if(m_term_stem.equals(ConstantsDB.indexTypeStem)) {
            proc_name = "buildStem";
        }

        printStart(proc_name);
        timer.start();

        ArrayList<String> source_list = null;

        if(m_term_stem.equals(ConstantsDB.indexTypeTerm)) {
            insert_query = ConstantsDB.insertTerm;
            source_list = SearchEngine.getSrcWithPageId(ConstantsDB.scopeAllClearTitleAndContent);
        } else if(m_term_stem.equals(ConstantsDB.indexTypeStem)) {
            insert_query = ConstantsDB.insertStem;
            source_list = SearchEngine.getSrcWithPageId(ConstantsDB.scopeAllStemTitleAndContent);
        }

        Set<String> uniques = new LinkedHashSet<String>();

        try {
            conn = db.getConnection();
//            ArrayList<String> sContents = SearchEngine.getAllUrlClearContentWithPageId();
            for(String sContent: source_list) {
//                String pageId = sContent.substring(0, sContent.indexOf(":"));
                sContent = sContent.substring(sContent.indexOf(":")+1);

                StringTokenizer st = new StringTokenizer(sContent, " ");
                while(st.hasMoreTokens()) {
                    String term = st.nextToken().strip();
                    if(term.length()>0) {
                        uniques.add(term);
                    }
                }
            }

//            ArrayUtil.countStringTermFrequency(uniques);
            for(String stem: uniques) {
//                System.out.println(stem);
                data = new ArrayList<Object>();
                data.add(stem);
                db.genericInsertUpdateDelete(conn, insert_query, data);
                conn.commit();
            }

            conn.close();

        } catch(SQLException e) {
            e.printStackTrace();
        }

        printObject("Total unique [" + m_term_stem + "]: " + uniques.size());

        timer.stop();
        timer.printElapseTimeInSecond();
        printDone();
    }

    private void buildClearTitleToken() {
        buildToken(ConstantsDB.tokenTypeClearTitle);
    }

    private void buildClearContentToken() {
        buildToken(ConstantsDB.tokenTypeClearContent);
    }

    private void buildStemTitleToken() {
        buildToken(ConstantsDB.tokenTypeStemTitle);
    }

    private void buildStemContentToken() {
        buildToken(ConstantsDB.tokenTypeStemContent);
    }

    private void buildToken(String m_token_type) {

        int pos_type = -1;

        if(m_token_type == ConstantsDB.tokenTypeClearTitle) {
            proc_name = "buildClearTitleToken";
            pos_type = ConstantsDB.dsTypeTitle;
        } else if(m_token_type == ConstantsDB.tokenTypeClearContent) {
            proc_name = "buildClearContentToken";
            pos_type = ConstantsDB.dsTypeContent;
        } else if(m_token_type == ConstantsDB.tokenTypeStemTitle) {
            proc_name = "buildStemTitleToken";
            pos_type = ConstantsDB.dsTypeTitle;
        } else if(m_token_type == ConstantsDB.tokenTypeStemContent) {
            proc_name = "buildStemContentToken";
            pos_type = ConstantsDB.dsTypeContent;
        }

        printStart(proc_name);
        timer.start();

        try {
            ArrayList<String> idatas = null;

            if(m_token_type == ConstantsDB.tokenTypeClearTitle) {
                idatas = SearchEngine.getSrcWithPageId(ConstantsDB.scopeAllClearTitle);
                insert_query = ConstantsDB.insertRawToken;
            } else if(m_token_type == ConstantsDB.tokenTypeClearContent) {
                idatas = SearchEngine.getSrcWithPageId(ConstantsDB.scopeAllClearContent);
                insert_query = ConstantsDB.insertRawToken;
            } else if(m_token_type == ConstantsDB.tokenTypeStemTitle) {
                idatas = SearchEngine.getSrcWithPageId(ConstantsDB.scopeAllStemTitle);
                insert_query = ConstantsDB.insertStemToken;
            } else if(m_token_type == ConstantsDB.tokenTypeStemContent) {
                idatas = SearchEngine.getSrcWithPageId(ConstantsDB.scopeAllStemContent);
                insert_query = ConstantsDB.insertStemToken;
            }

            for(String idata: idatas) {

                Integer pageId = Integer.parseInt(idata.substring(0, idata.indexOf(":")));
                String src = idata.substring(idata.indexOf(":")+1);

                //            printKVPair(pageId, clearContent);
                Set<String> tpSet = ArrayUtil.getTermPositionMap(src);
                //            if(pageId==18) { ArrayUtil.printSet(tpSet); } // for testing

                conn = db.getConnection();
                for(String tp: tpSet) {
                    String term = tp.substring(0, tp.indexOf("-"));
                    String pos = tp.substring(tp.indexOf("-")+1);

                    Integer itemId = -1;
                    if(m_token_type == ConstantsDB.tokenTypeClearTitle) {
                        itemId = SearchEngine.getItemIdByItemName(ConstantsDB.indexTypeTerm, term);
                    } else if(m_token_type == ConstantsDB.tokenTypeClearContent) {
                        itemId = SearchEngine.getItemIdByItemName(ConstantsDB.indexTypeTerm, term);
                    } else if(m_token_type == ConstantsDB.tokenTypeStemTitle) {
                        itemId = SearchEngine.getItemIdByItemName(ConstantsDB.indexTypeStem, term);
                    } else if(m_token_type == ConstantsDB.tokenTypeStemContent) {
                        itemId = SearchEngine.getItemIdByItemName(ConstantsDB.indexTypeStem, term);
                    }
//                    if(pageId==1) { printObject(pageId+"|"+termId+"|"+pos_type+"|"+pos); }
//                    if(itemId==-1) { printObject(pageId+"|"+itemId+"|"+pos_type+"|"+pos); }

                    data = new ArrayList<Object>();
                    data.add(pageId);
                    data.add(itemId);
                    data.add(pos_type);
                    data.add(pos);

                    db.genericInsertUpdateDelete(conn, insert_query, data);
                }
                conn.commit();
                conn.close();
            }

        } catch(SQLException e) {
            e.printStackTrace();
        }

        timer.stop();
        timer.printElapseTimeInSecond();
        printDone();
    }

    private void buildUrlInverted() {
        proc_name = "buildUrlInverted";
        printStart(proc_name);
        timer.start();

        try {
            ArrayList<String> srcs = SearchEngine.getFullUrlList(true);
            ArrayList<String> childs = null;

            conn = db.getConnection();

            for(String src: srcs) {

                Integer parentPageId = Integer.parseInt(src.substring(0, src.indexOf(":")));
                String parentUrl = src.substring(src.indexOf(":")+1);

                childs = Spider.getUrlChildLinks(parentUrl);
                for(String childUrl: childs) {
                    Integer childPageId = SearchEngine.getPageIdByUrl(childUrl);

                    // "insert into url_inverted(parent_page_id, child_page_id) values(?, ?);";
                    data = new ArrayList<Object>();
                    data.add(parentPageId);
                    data.add(childPageId);

                    db.genericInsertUpdateDelete(conn, ConstantsDB.insertUrlInverted, data);
                }
            }

            conn.commit();
            conn.close();

        } catch(SQLException e) {
            e.printStackTrace();
        }

        timer.stop();
        timer.printElapseTimeInSecond();
        printDone();
    }

    private void buildUrlForward() {
        proc_name = "buildUrlForward";
        printStart(proc_name);
        timer.start();

        try {

            conn = db.getConnection();
            db.genericInsertUpdateDelete(conn, ConstantsDB.insertSelectUrlForward, null);
            conn.commit();
            conn.close();

        } catch(SQLException e) {
            e.printStackTrace();
        }

        timer.stop();
        timer.printElapseTimeInSecond();
        printDone();
    }

    private void buildMaxTfTitle() {
        buildMaxTf(ConstantsDB.dsTypeTitle);
    }

    private void buildMaxTfContent() {
        buildMaxTf(ConstantsDB.dsTypeContent);
    }

    private void buildMaxTf(int m_src_type) {

        if(m_src_type == ConstantsDB.dsTypeTitle) {
            proc_name = "buildTitleMaxTF";
        } else if(m_src_type == ConstantsDB.dsTypeContent) {
            proc_name = "buildContentMaxTF";
        } else {
            printHelloWorld();
        }

        printStart(proc_name);
        timer.start();

        try {
            ArrayList<Integer> pageIds = SearchEngine.getAllPageId();
//            printKVPair("pageIds.size()", pageIds.size());
//            ArrayUtil.printArrayList(pageIds);

            conn = db.getConnection();

            for(int pageId: pageIds) {
                int maxTf = SearchEngine.getMaxTfByPageId(pageId, m_src_type);

                // "insert into max_tf(page_id, max_tF, type) values(?, ?, ?);";
                data = new ArrayList<Object>();
                data.add(pageId);
                data.add(maxTf);
                data.add(m_src_type);
                db.genericInsertUpdateDelete(conn, ConstantsDB.insertMaxTF, data);
            }

            conn.commit();
            conn.close();

        } catch(SQLException e) {
            e.printStackTrace();
        }

        timer.stop();
        timer.printElapseTimeInSecond();
        printDone();
    }

    public void reBuildAllIndexes() {

        proc_name = "reBuildAllIndexes";
        printStart(proc_name);
        timer_overall.start();

        initAllDbTable();

        buildUrl(); // ok!~
        updateUrlInitContent(); // ok!~
        normalizeRawTitle(); // ok!~
        normalizeRawContent();
        updateUrlInitStemTitle(); // ok!~
        updateUrlInitStemContent(); // ok!~

        buildTerm(); // ok!~
        buildStem(); // ok!~

        buildClearTitleToken(); // ok!~
        buildClearContentToken(); // ok!~

        buildStemTitleToken(); // ok!~
        buildStemContentToken(); // ok!~

        buildMaxTfTitle(); // ok!~
        buildMaxTfContent(); // ok!~

        buildUrlInverted(); // ok!~
        buildUrlForward(); // ok!~

        timer_overall.stop();
        timer_overall.printOverallElapseTimeInSecond();
    }

    public void checkAndUpdateIndex() {

        proc_name = "checkAndUpdateIndex";
        printStart(proc_name);
        timer_overall.start();

        SearchEngine.fullRecraw();

        ArrayList<String> new_urls = SearchEngine.getNewUrl();
//      ArrayUtil.printArrayList(new_urls);

        ArrayList<String> removed_urls = SearchEngine.getRemovedUrl();
//      ArrayUtil.printArrayList(removed_urls);

        ArrayList<String> modified_urls = SearchEngine.getModifiedUrl();
//      ArrayUtil.printArrayList(rmodified_urls);

        ArrayList<String> changeList = new ArrayList<String>();
        changeList.addAll(new_urls);
        changeList.addAll(removed_urls);
        changeList.addAll(modified_urls);
        ArrayUtil.printArrayList(changeList);

        // Rebuild all index if: New Page(s) or Removed Page(s) or Modified Page(s) found
        try {
            if(changeList.size()>0) {
                reBuildAllIndexes();

                // Update Change History
                conn = db.getConnection();

                for(String list: changeList) {
                    data = new ArrayList<Object>();
                    StringTokenizer st = new StringTokenizer(list, "|");
                    while(st.hasMoreTokens()) {
                        String col = st.nextToken();
                        data.add(col);
                        //                    System.out.println("["+col+"]");
                    }

                    if(data.size()>0) {
                        Date d = new Date();
                        String log_date = DateUtil.getFormattedDate(d);
                        data.add(0, log_date);
//                        ArrayUtil.printArrayList(data);

                        db.genericInsertUpdateDelete(conn, ConstantsDB.insertHistory, data);
                        conn.commit();
                    }
                }
                conn.close();
            } else {
                printObject("No any kind of update found.");
                // Do Nothing
            }
        } catch(SQLException e) {
            e.printStackTrace();
        }

        timer_overall.stop();
        timer_overall.printOverallElapseTimeInSecond();
    }

    private void initAllDbTable() {
        try {
            db = new DBUtil();
            conn = db.getConnection();

            db.genericInsertUpdateDelete(conn, ConstantsDB.dropUrl, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.dropTerm, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.dropStem, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.dropRawToken, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.dropStemToken, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.dropMaxTf, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.dropUrlInverted, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.dropUrlForward, null);

            db.genericInsertUpdateDelete(conn, ConstantsDB.createUrl, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.createTerm, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.createStem, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.createRawToken, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.createStemToken, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.createMaxTf, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.createUrlInverted, null);
            db.genericInsertUpdateDelete(conn, ConstantsDB.createUrlForward, null);

            conn.commit();
            conn.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        Indexer idxr = new Indexer();

        idxr.initAllDbTable();

        idxr.reBuildAllIndexes();
        idxr.checkAndUpdateIndex();

        Toolkit.getDefaultToolkit().beep();
    }

}
