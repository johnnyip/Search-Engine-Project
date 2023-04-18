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
    
    public void buildUrl() {
        proc_name = "buildUrl";
        printStart(proc_name);
        timer.start();
        
        try {
            conn = db.getConnection();
            ArrayList<String> links = Spider.getAllUrlList(Constants.base_url);
            for(String link: links) {
                data = new ArrayList<Object>();
                data.add(link);
                db.genericInsertUpdate(conn, ConstantsDB.insertUrl, data);
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
    
    public void updateUrlInitContent() {
        proc_name = "updateUrlInitContent";
        printStart(proc_name);
        timer.start();
        ArrayList<String> links = SearchEngine.getFullUrlList(false);
        
        try {
            conn = db.getConnection();
            for(String link: links) {
                URL url = new URL(link);
                HttpURLConnection httpCon = (HttpURLConnection) url.openConnection();
                String strLastModifiedDate = new Date(httpCon.getLastModified()).toString();
                
                Document doc = Jsoup.connect(link).get();
                String title = doc.title();
                String raw = doc.body().text();
                
                data = new ArrayList<Object>();
                data.add(title);
                data.add(strLastModifiedDate);
                data.add(raw);
                data.add(link);
                db.genericInsertUpdate(conn, ConstantsDB.updateInitiallRawContent, data);
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
    
    public void normalizeRawTitle() {
        normalizeRawData(ConstantsDB.dataTypeTitle);
    }
    
    public void normalizeRawContent() {
        normalizeRawData(ConstantsDB.dataTypeContent);
    }
    
    public void normalizeRawData(String m_data_type) {
        
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
                db.genericInsertUpdate(conn, query, data);
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
    
    public void updateUrlInitStemTitle() {
        updateUrlInitStem(ConstantsDB.dataTypeTitle);
    }
    
    public void updateUrlInitStemContent() {
        updateUrlInitStem(ConstantsDB.dataTypeContent);
    }
    
    public void updateUrlInitStem(String m_data_type) {
        
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
                            
                            db.genericInsertUpdate(conn, query, data);
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
    
    public void buildTerm() {
        buildTermOrStem(ConstantsDB.indexTypeTerm);
    }
    
    public void buildStem() {
        buildTermOrStem(ConstantsDB.indexTypeStem);
    }
    
    public void buildTermOrStem(String m_term_stem) {
        
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
            
//            ArrayUtil.countStringTermFrequency(uniqueTerms);
            for(String stem: uniques) {
//                System.out.println(stem);
                data = new ArrayList<Object>();
                data.add(stem);
                db.genericInsertUpdate(conn, insert_query, data);
            }
            conn.commit();
            conn.close();
        } catch(SQLException e) {
            e.printStackTrace();
        }
        
        printObject("Total unique [" + m_term_stem + "]: " + uniques.size());
        
        timer.stop();
        timer.printElapseTimeInSecond();
        printDone();
    }
    
    public void buildClearTitleToken() {
        buildToken(ConstantsDB.tokenTypeClearTitle);
    }
    
    public void buildClearContentToken() {
        buildToken(ConstantsDB.tokenTypeClearContent);
    }
    
    public void buildStemTitleToken() {
        buildToken(ConstantsDB.tokenTypeStemTitle);
    }
    
    public void buildStemContentToken() {
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
                  
                    db.genericInsertUpdate(conn, insert_query, data);
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
    
    public void buildUrlInverted() {
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
                    
                    db.genericInsertUpdate(conn, ConstantsDB.insertUrlInverted, data);
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
    
    public void buildUrlForward() {
        proc_name = "buildUrlForward";
        printStart(proc_name);
        timer.start();
        
        try {
            
            conn = db.getConnection();
            db.genericInsertUpdate(conn, ConstantsDB.insertSelectUrlForward, null);
            conn.commit();
            conn.close();
            
        } catch(SQLException e) {
            e.printStackTrace();
        }
        
        timer.stop();
        timer.printElapseTimeInSecond();
        printDone();
    }
    
    public void buildMaxTF(int m_src_type) {
        
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
                db.genericInsertUpdate(conn, ConstantsDB.insertMaxTF, data);
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
        
        timer_overall.start();
        
        buildUrl(); // ok!~
        updateUrlInitContent(); // ok!~
        normalizeRawData(ConstantsDB.dataTypeTitle); // ok!~
        normalizeRawData(ConstantsDB.dataTypeContent); // ok!~
        updateUrlInitStemTitle(); // ok!~
        updateUrlInitStemContent(); // ok!~
        
        buildTerm(); // ok!~
        buildStem(); // ok!~
        
        buildClearTitleToken(); // ok!~
        buildClearContentToken(); // ok!~
        
        buildStemTitleToken(); // ok!~
        buildStemContentToken(); // ok!~
        
        buildMaxTF(ConstantsDB.dsTypeTitle); // ok!~
        buildMaxTF(ConstantsDB.dsTypeContent); // ok!~
            
        buildUrlInverted(); // ok!~
        buildUrlForward(); // ok!~
        
        
        // Below Index Change to DB VIEW
//        buildStemPosition();
//        buildStemInverted();
//        buildStemForward();
//        buildStemDF();
        
        timer_overall.stop();
        timer_overall.printOverallElapseTimeInSecond();
    }

    public static void main(String[] args) {
        Indexer idxr = new Indexer();
        idxr.reBuildAllIndexes();
        
        Toolkit.getDefaultToolkit().beep();
    }

}

